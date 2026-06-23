import os
import json
import joblib
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split


warnings.filterwarnings("ignore")


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)


# ---------------------------------------------------------
# Training Configuration
# ---------------------------------------------------------
TRAINING_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
    "META", "TSLA", "JPM", "BAC", "XOM",
    "CVX", "UNH", "JNJ", "PFE", "WMT",
    "HD", "PG", "KO", "MCD", "DIS"
]

BENCHMARK_TICKERS = ["SPY", "QQQ", "^VIX"]

PERIOD = "5y"
INTERVAL = "1d"
RANDOM_STATE = 42


FEATURE_COLUMNS = [
    "daily_return",
    "return_5d",
    "return_20d",
    "volatility_20d",
    "volatility_60d",
    "max_drawdown_60d",
    "ma_20_gap",
    "ma_50_gap",
    "volume_change_20d",
    "spy_return_20d",
    "spy_volatility_20d",
    "qqq_return_20d",
    "vix_level",
    "vix_change_20d"
]


# ---------------------------------------------------------
# Data Download Functions
# ---------------------------------------------------------
def download_single_ticker(ticker, period=PERIOD, interval=INTERVAL):
    """
    Downloads historical daily data for one ticker.
    Handles yfinance column format safely.
    """
    try:
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            print(f"Warning: No data found for {ticker}")
            return pd.DataFrame()

        # Fix yfinance MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        # Standardize column names
        df.columns = [str(col).strip().title().replace(" ", "_") for col in df.columns]

        # Handle Date or Datetime column
        if "Datetime" in df.columns and "Date" not in df.columns:
            df = df.rename(columns={"Datetime": "Date"})

        if "Date" not in df.columns:
            print(f"Warning: Date column not found for {ticker}. Columns found: {df.columns.tolist()}")
            return pd.DataFrame()

        df["Ticker"] = ticker

        required_columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Ticker"]

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Warning: Missing columns for {ticker}: {missing_columns}")
            return pd.DataFrame()

        df = df[required_columns].copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.dropna(subset=["Close"])

        return df

    except Exception as error:
        print(f"Error downloading {ticker}: {error}")
        return pd.DataFrame()


def download_training_data(tickers):
    """
    Downloads data for multiple tickers and combines it into one dataset.
    """
    all_data = []

    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        ticker_data = download_single_ticker(ticker)

        if not ticker_data.empty:
            all_data.append(ticker_data)

    if not all_data:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)


# ---------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------
def create_benchmark_features(benchmark_data):
    """
    Creates SPY, QQQ, and VIX benchmark features.
    These features help the model understand broader market conditions.
    """
    benchmark_features = pd.DataFrame()

    for ticker in benchmark_data["Ticker"].unique():
        temp = benchmark_data[benchmark_data["Ticker"] == ticker].copy()
        temp = temp.sort_values("Date")

        temp["daily_return"] = temp["Close"].pct_change()
        temp["return_20d"] = temp["Close"].pct_change(20)
        temp["volatility_20d"] = temp["daily_return"].rolling(20).std() * np.sqrt(252)
        temp["vix_change_20d"] = temp["Close"].pct_change(20)

        if ticker == "SPY":
            selected = temp[["Date", "return_20d", "volatility_20d"]].copy()
            selected = selected.rename(
                columns={
                    "return_20d": "spy_return_20d",
                    "volatility_20d": "spy_volatility_20d"
                }
            )

        elif ticker == "QQQ":
            selected = temp[["Date", "return_20d"]].copy()
            selected = selected.rename(columns={"return_20d": "qqq_return_20d"})

        elif ticker == "^VIX":
            selected = temp[["Date", "Close", "vix_change_20d"]].copy()
            selected = selected.rename(columns={"Close": "vix_level"})

        else:
            continue

        if benchmark_features.empty:
            benchmark_features = selected
        else:
            benchmark_features = benchmark_features.merge(selected, on="Date", how="outer")

    benchmark_features = benchmark_features.sort_values("Date")
    benchmark_features = benchmark_features.ffill()

    return benchmark_features


def create_stock_features(stock_data, benchmark_features):
    """
    Creates technical and risk-related features for each stock.
    """
    feature_data = []

    for ticker in stock_data["Ticker"].unique():
        temp = stock_data[stock_data["Ticker"] == ticker].copy()
        temp = temp.sort_values("Date")

        temp["daily_return"] = temp["Close"].pct_change()
        temp["return_5d"] = temp["Close"].pct_change(5)
        temp["return_20d"] = temp["Close"].pct_change(20)

        temp["volatility_20d"] = temp["daily_return"].rolling(20).std() * np.sqrt(252)
        temp["volatility_60d"] = temp["daily_return"].rolling(60).std() * np.sqrt(252)

        temp["rolling_max_60d"] = temp["Close"].rolling(60).max()
        temp["drawdown_60d"] = (temp["Close"] - temp["rolling_max_60d"]) / temp["rolling_max_60d"]
        temp["max_drawdown_60d"] = temp["drawdown_60d"].rolling(60).min()

        temp["ma_20"] = temp["Close"].rolling(20).mean()
        temp["ma_50"] = temp["Close"].rolling(50).mean()

        temp["ma_20_gap"] = (temp["Close"] - temp["ma_20"]) / temp["ma_20"]
        temp["ma_50_gap"] = (temp["Close"] - temp["ma_50"]) / temp["ma_50"]

        temp["volume_change_20d"] = temp["Volume"].pct_change(20)

        # Future return is used only for creating the training label.
        # It will not be used as a prediction feature.
        temp["future_5d_return"] = temp["Close"].shift(-5) / temp["Close"] - 1

        temp = temp.merge(benchmark_features, on="Date", how="left")

        feature_data.append(temp)

    full_features = pd.concat(feature_data, ignore_index=True)
    full_features = full_features.sort_values(["Ticker", "Date"])

    return full_features


# ---------------------------------------------------------
# Risk Label Creation
# ---------------------------------------------------------
def assign_risk_label(future_5d_return):
    """
    Creates the target label for the model.

    High Risk:
        Future 5-day return is less than or equal to -3%.

    Medium Risk:
        Future 5-day return is between -3% and +1%.

    Low Risk:
        Future 5-day return is above +1%.
    """
    if future_5d_return <= -0.03:
        return "High Risk"
    elif future_5d_return <= 0.01:
        return "Medium Risk"
    else:
        return "Low Risk"


def prepare_model_dataset(feature_df):
    """
    Cleans the feature dataset and prepares X and y for model training.
    """
    model_df = feature_df.copy()

    model_df["risk_label"] = model_df["future_5d_return"].apply(assign_risk_label)

    selected_columns = ["Date", "Ticker", "risk_label", "future_5d_return"] + FEATURE_COLUMNS
    model_df = model_df[selected_columns].copy()

    model_df = model_df.replace([np.inf, -np.inf], np.nan)
    model_df = model_df.dropna()

    return model_df


# ---------------------------------------------------------
# Model Training
# ---------------------------------------------------------
def train_model(model_df):
    """
    Trains a Random Forest classification model.
    """
    X = model_df[FEATURE_COLUMNS]
    y = model_df["risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_STATE
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report_dict = classification_report(y_test, predictions, output_dict=True)
    report_text = classification_report(y_test, predictions)

    return model, accuracy, report_dict, report_text


def save_model_outputs(model, accuracy, report_dict, report_text, model_df):
    """
    Saves the trained model and model documentation files.
    """
    model_package = {
        "model": model,
        "features": FEATURE_COLUMNS,
        "model_type": "RandomForestClassifier",
        "target": "risk_label",
        "labels": ["Low Risk", "Medium Risk", "High Risk"],
        "training_tickers": TRAINING_TICKERS,
        "benchmark_tickers": BENCHMARK_TICKERS,
        "period": PERIOD,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_label_method": {
            "High Risk": "Future 5-day return <= -3%",
            "Medium Risk": "Future 5-day return > -3% and <= +1%",
            "Low Risk": "Future 5-day return > +1%"
        }
    }

    model_path = os.path.join(MODEL_DIR, "risk_model.pkl")
    joblib.dump(model_package, model_path)

    feature_doc = {
        "features": FEATURE_COLUMNS,
        "description": {
            "daily_return": "Daily stock return.",
            "return_5d": "Stock return over the past 5 trading days.",
            "return_20d": "Stock return over the past 20 trading days.",
            "volatility_20d": "Annualized volatility using the past 20 trading days.",
            "volatility_60d": "Annualized volatility using the past 60 trading days.",
            "max_drawdown_60d": "Largest rolling 60-day drawdown.",
            "ma_20_gap": "Percentage difference between close price and 20-day moving average.",
            "ma_50_gap": "Percentage difference between close price and 50-day moving average.",
            "volume_change_20d": "Volume percentage change over 20 trading days.",
            "spy_return_20d": "SPY 20-day return as broad market context.",
            "spy_volatility_20d": "SPY 20-day annualized volatility.",
            "qqq_return_20d": "QQQ 20-day return as technology-heavy market context.",
            "vix_level": "Latest VIX level.",
            "vix_change_20d": "VIX percentage change over 20 trading days."
        }
    }

    feature_path = os.path.join(MODEL_DIR, "model_features.json")

    with open(feature_path, "w") as file:
        json.dump(feature_doc, file, indent=4)

    performance_df = pd.DataFrame(report_dict).transpose()
    performance_df["accuracy_overall"] = accuracy

    performance_path = os.path.join(MODEL_DIR, "model_performance.csv")
    performance_df.to_csv(performance_path)

    training_data_path = os.path.join(DATA_PROCESSED_DIR, "model_training_dataset.csv")
    model_df.to_csv(training_data_path, index=False)

    print("\nModel training completed successfully.")
    print(f"Model saved to: {model_path}")
    print(f"Feature documentation saved to: {feature_path}")
    print(f"Performance report saved to: {performance_path}")
    print(f"Training dataset saved to: {training_data_path}")

    print("\nModel Accuracy:")
    print(f"{accuracy:.2%}")

    print("\nClassification Report:")
    print(report_text)


# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
def main():
    print("Starting risk model training process...\n")

    print("Downloading stock training data...")
    stock_data = download_training_data(TRAINING_TICKERS)

    print("\nDownloading benchmark data...")
    benchmark_data = download_training_data(BENCHMARK_TICKERS)

    if stock_data.empty:
        raise ValueError("No stock data was downloaded. Model cannot be trained.")

    if benchmark_data.empty:
        raise ValueError("No benchmark data was downloaded. Model cannot be trained.")

    print("\nCreating benchmark features...")
    benchmark_features = create_benchmark_features(benchmark_data)

    print("Creating stock risk features...")
    feature_df = create_stock_features(stock_data, benchmark_features)

    print("Preparing model dataset...")
    model_df = prepare_model_dataset(feature_df)

    if model_df.empty:
        raise ValueError("Model dataset is empty after cleaning.")

    print(f"\nTraining rows: {len(model_df):,}")
    print("Risk label distribution:")
    print(model_df["risk_label"].value_counts())

    print("\nTraining Random Forest risk classification model...")
    model, accuracy, report_dict, report_text = train_model(model_df)

    save_model_outputs(model, accuracy, report_dict, report_text, model_df)


if __name__ == "__main__":
    main()