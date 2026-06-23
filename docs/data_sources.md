# Data Sources

## Overview

This project uses latest available historical market data to calculate portfolio risk metrics, benchmark indicators, stress-test outputs, and machine learning-based risk classifications.

The application retrieves market data programmatically using Python and processes it inside the Streamlit app and model training script.

## Primary Data Source

The primary data source used in this project is:

**Yahoo Finance market data accessed through the `yfinance` Python library**

The project uses `yfinance` to download historical daily market data for:

* User-selected stock tickers
* SPY benchmark
* QQQ benchmark
* VIX volatility proxy

The data is used for educational portfolio analytics and machine learning model development.

## Data Collection Method

Market data is collected using Python through the `yfinance.download()` function.

In the Streamlit app, data is retrieved based on:

* User-entered ticker symbols
* Selected historical period
* Daily price interval
* Benchmark ticker list

The application currently supports these historical periods:

```text
6mo
1y
2y
5y
```

The app uses daily data frequency:

```text
1d
```

## Portfolio Ticker Data

Users can enter custom stock tickers in the Streamlit sidebar.

Example default tickers:

```text
AAPL, MSFT, NVDA, JPM, TSLA
```

For each selected ticker, the app retrieves:

* Date
* Open price
* High price
* Low price
* Close price
* Volume
* Ticker symbol

These fields are used to calculate return, volatility, drawdown, trend, and risk contribution metrics.

## Benchmark Data

The project uses benchmark tickers to provide broader market context.

## SPY

```text
SPY
```

SPY is used as a broad U.S. equity market benchmark proxy. In this project, it helps compare the selected portfolio against a general S&P 500-style market benchmark.

SPY is used to calculate:

* Benchmark total return
* Benchmark 20-day return
* Benchmark annualized volatility
* Benchmark drawdown
* Portfolio vs market comparison

## QQQ

```text
QQQ
```

QQQ is used as a technology-heavy Nasdaq 100-style benchmark proxy. It helps compare the selected portfolio against a growth and technology-oriented market benchmark.

QQQ is used to calculate:

* Technology-heavy benchmark return
* Short-term momentum
* Benchmark drawdown
* Portfolio vs QQQ indexed performance

## VIX Volatility Proxy

```text
^VIX
```

The VIX is used as a market volatility and fear proxy.

In this project, VIX helps generate a simplified market risk signal:

* Calm Market
* Cautious Market
* High-Risk Market

The VIX is used to calculate:

* Latest volatility level
* 20-day VIX change
* Market risk condition
* Benchmark risk context

## Data Used in the Streamlit App

The Streamlit application retrieves data dynamically when the app runs.

The app uses this data for:

* Portfolio risk snapshot
* Market overview
* Portfolio overview
* ML risk model input features
* Risk contribution analysis
* Drawdown analysis
* Stress testing
* Downloadable risk metrics

## Data Used in Model Training

The machine learning model is trained using historical market data for a selected group of stocks and benchmark tickers.

The model training script is located at:

```text
model/train_risk_model.py
```

The training process downloads five years of daily historical data for multiple stocks.

Training tickers used include:

```text
AAPL
MSFT
NVDA
GOOGL
AMZN
META
TSLA
JPM
BAC
XOM
CVX
UNH
JNJ
PFE
WMT
HD
PG
KO
MCD
DIS
```

Benchmark tickers used during model training:

```text
SPY
QQQ
^VIX
```

## Data Fields

The main raw fields used are:

| Field  | Description                             |
| ------ | --------------------------------------- |
| Date   | Trading date                            |
| Open   | Opening price                           |
| High   | Highest price during the trading period |
| Low    | Lowest price during the trading period  |
| Close  | Closing price                           |
| Volume | Number of shares traded                 |
| Ticker | Security ticker symbol                  |

## Engineered Data Fields

The project creates additional analytical fields from raw market data.

Key engineered fields include:

| Field                     | Description                                        |
| ------------------------- | -------------------------------------------------- |
| Daily Return              | Daily percentage change in closing price           |
| 5-Day Return              | Return over the previous 5 trading days            |
| 20-Day Return             | Return over the previous 20 trading days           |
| 20-Day Volatility         | Annualized volatility using recent 20-day returns  |
| 60-Day Volatility         | Annualized volatility using recent 60-day returns  |
| Drawdown                  | Decline from previous peak value                   |
| Maximum Drawdown          | Largest observed drawdown over the selected period |
| 20-Day Moving Average Gap | Difference between price and 20-day moving average |
| 50-Day Moving Average Gap | Difference between price and 50-day moving average |
| Volume Change             | Percentage change in trading volume                |
| SPY 20-Day Return         | Broad market short-term return                     |
| SPY 20-Day Volatility     | Broad market short-term volatility                 |
| QQQ 20-Day Return         | Technology-heavy benchmark short-term return       |
| VIX Level                 | Latest volatility proxy level                      |
| VIX 20-Day Change         | Change in VIX over the previous 20 trading days    |

## Data Storage

The project does not permanently store all raw downloaded market data in GitHub.

Instead, the data is pulled dynamically when:

* The Streamlit app is running
* The model training script is executed

The model training script can generate a processed training dataset:

```text
data/processed/model_training_dataset.csv
```

This file is excluded from GitHub using `.gitignore` because it can be regenerated.

## Model Output Files

The model training process creates the following output files:

```text
model/risk_model.pkl
model/model_features.json
model/model_performance.csv
```

These files are included in the repository because they are required for the Streamlit application to load and use the trained model.

## Data Refresh Approach

The Streamlit app uses a cached data loading function.

The cache refreshes after a set time interval so the app does not repeatedly download the same data during every interaction.

The current cache duration is:

```text
900 seconds
```

This is equal to:

```text
15 minutes
```

Users can also click the refresh button in the sidebar to clear the cache and request updated market data.

## Data Quality Considerations

The project includes basic data quality handling:

* Removes records with missing closing prices
* Standardizes column names
* Converts date fields into datetime format
* Handles unavailable tickers
* Handles missing benchmark data
* Removes infinite values during model training
* Drops rows with missing model features before training

## Limitations of the Data

The current data source is suitable for educational and portfolio demonstration purposes, but it has limitations.

Key limitations include:

* Data may be delayed or not institutional-grade real-time market data
* Free market data sources may occasionally have missing values
* Ticker availability may vary
* Intraday trading analysis is not included in the current version
* The app does not currently use paid market data feeds
* The app does not include broker account data
* The app does not include full macroeconomic data yet
* Historical market behavior does not guarantee future results

## Why This Data Source Was Selected

This data source was selected because it is:

* Easy to access with Python
* Suitable for beginner-friendly project development
* Useful for stock-level and benchmark analysis
* Compatible with Streamlit
* Sufficient for portfolio demonstration purposes
* Flexible enough to support custom ticker inputs
* Useful for machine learning feature engineering

## Future Data Source Enhancements

Future versions of this project may include:

* Alpha Vantage API
* FRED macroeconomic data
* Interest rate indicators
* Inflation indicators
* Sector ETF benchmarks
* Cryptocurrency benchmarks
* Commodity price indicators
* SQLite database storage
* Scheduled automated refresh
* Streamlit secrets for API keys
* More robust error handling for data outages

## Important Disclaimer

The data used in this project is for educational and portfolio demonstration purposes only. It should not be treated as official financial data, investment advice, or a trading recommendation. Users should verify financial data from official and professional sources before making investment decisions.
