import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Investor Risk Intelligence Platform",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
@st.cache_data(ttl=900)
def load_market_data(tickers, period="1y"):
    """
    Downloads market data using yfinance.
    Cache refreshes every 15 minutes.
    """
    try:
        data = yf.download(
            tickers=tickers,
            period=period,
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            progress=False
        )

        if data.empty:
            return pd.DataFrame()

        all_data = []

        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    temp = data.copy()
                else:
                    temp = data[ticker].copy()

                temp = temp.reset_index()
                temp["Ticker"] = ticker
                all_data.append(temp)

            except Exception:
                continue

        final_df = pd.concat(all_data, ignore_index=True)
        final_df.columns = [str(col).title().replace(" ", "_") for col in final_df.columns]

        return final_df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def calculate_risk_metrics(df):
    """
    Calculates return, volatility, drawdown, and simple risk metrics.
    """
    metrics = []

    for ticker in df["Ticker"].unique():
        temp = df[df["Ticker"] == ticker].copy()
        temp = temp.sort_values("Date")

        temp["Daily_Return"] = temp["Close"].pct_change()
        temp["Cumulative_Return"] = (1 + temp["Daily_Return"]).cumprod()
        temp["Rolling_Max"] = temp["Cumulative_Return"].cummax()
        temp["Drawdown"] = (temp["Cumulative_Return"] - temp["Rolling_Max"]) / temp["Rolling_Max"]

        latest_price = temp["Close"].iloc[-1]
        total_return = (temp["Close"].iloc[-1] / temp["Close"].iloc[0]) - 1
        volatility = temp["Daily_Return"].std() * np.sqrt(252)
        max_drawdown = temp["Drawdown"].min()

        recent_return_20d = temp["Close"].pct_change(20).iloc[-1]
        recent_volatility_20d = temp["Daily_Return"].rolling(20).std().iloc[-1] * np.sqrt(252)

        metrics.append({
            "Ticker": ticker,
            "Latest Price": latest_price,
            "Total Return": total_return,
            "Annualized Volatility": volatility,
            "Max Drawdown": max_drawdown,
            "20D Return": recent_return_20d,
            "20D Volatility": recent_volatility_20d
        })

    return pd.DataFrame(metrics)


def calculate_portfolio_metrics(metrics_df, weights):
    """
    Calculates portfolio-level weighted risk metrics.
    """
    metrics_df = metrics_df.copy()
    metrics_df["Weight"] = metrics_df["Ticker"].map(weights)

    portfolio_return = (metrics_df["Total Return"] * metrics_df["Weight"]).sum()
    portfolio_volatility = (metrics_df["Annualized Volatility"] * metrics_df["Weight"]).sum()
    portfolio_drawdown = (metrics_df["Max Drawdown"] * metrics_df["Weight"]).sum()
    portfolio_20d_return = (metrics_df["20D Return"] * metrics_df["Weight"]).sum()

    return {
        "Portfolio Return": portfolio_return,
        "Portfolio Volatility": portfolio_volatility,
        "Portfolio Drawdown": portfolio_drawdown,
        "Portfolio 20D Return": portfolio_20d_return
    }


def calculate_risk_score(portfolio_metrics):
    """
    Creates a simple 0-100 portfolio risk score.
    Higher score = higher risk.
    """
    volatility_score = min(portfolio_metrics["Portfolio Volatility"] / 0.50, 1) * 35
    drawdown_score = min(abs(portfolio_metrics["Portfolio Drawdown"]) / 0.40, 1) * 35

    if portfolio_metrics["Portfolio 20D Return"] < -0.05:
        trend_score = 20
    elif portfolio_metrics["Portfolio 20D Return"] < 0:
        trend_score = 10
    else:
        trend_score = 3

    return_score = 10 if portfolio_metrics["Portfolio Return"] < 0 else 2

    risk_score = volatility_score + drawdown_score + trend_score + return_score
    risk_score = round(min(risk_score, 100), 1)

    if risk_score < 35:
        risk_level = "Low Risk"
    elif risk_score < 70:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return risk_score, risk_level


def format_percent(value):
    return f"{value:.2%}"


# ---------------------------------------------------------
# App Title
# ---------------------------------------------------------
st.title("📊 Real-Time Investor Risk Intelligence Platform")

st.markdown(
    """
    This interactive app helps investors analyze portfolio risk using recent market data, 
    risk metrics, drawdown analysis, volatility signals, and a simple risk scoring model.

    **Disclaimer:** This project is for educational and portfolio demonstration purposes only. 
    It is not financial advice.
    """
)


# ---------------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------------
st.sidebar.header("Portfolio Inputs")

default_tickers = "AAPL, MSFT, NVDA, JPM, TSLA"
ticker_input = st.sidebar.text_input(
    "Enter stock tickers separated by commas",
    value=default_tickers
)

period = st.sidebar.selectbox(
    "Select historical data period",
    ["6mo", "1y", "2y", "5y"],
    index=1
)

tickers = [ticker.strip().upper() for ticker in ticker_input.split(",") if ticker.strip()]

st.sidebar.markdown("---")
st.sidebar.subheader("Portfolio Weights")

weights = {}
if tickers:
    equal_weight = round(100 / len(tickers), 2)

    for ticker in tickers:
        weight = st.sidebar.number_input(
            f"{ticker} Weight (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(equal_weight),
            step=1.0
        )
        weights[ticker] = weight / 100

total_weight = sum(weights.values())

if abs(total_weight - 1.0) > 0.01:
    st.sidebar.warning(f"Total weight is {total_weight:.2%}. Please make it close to 100%.")


# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
if not tickers:
    st.warning("Please enter at least one ticker.")
    st.stop()

market_data = load_market_data(tickers, period)

if market_data.empty:
    st.error("No market data found. Please check the ticker symbols.")
    st.stop()


# ---------------------------------------------------------
# Calculate Metrics
# ---------------------------------------------------------
metrics_df = calculate_risk_metrics(market_data)
portfolio_metrics = calculate_portfolio_metrics(metrics_df, weights)
risk_score, risk_level = calculate_risk_score(portfolio_metrics)


# ---------------------------------------------------------
# Executive Summary
# ---------------------------------------------------------
st.header("1. Portfolio Risk Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Risk Score", f"{risk_score}/100")
col2.metric("Risk Level", risk_level)
col3.metric("Portfolio Return", format_percent(portfolio_metrics["Portfolio Return"]))
col4.metric("Portfolio Volatility", format_percent(portfolio_metrics["Portfolio Volatility"]))

col5, col6 = st.columns(2)
col5.metric("Estimated Max Drawdown", format_percent(portfolio_metrics["Portfolio Drawdown"]))
col6.metric("Recent 20-Day Return", format_percent(portfolio_metrics["Portfolio 20D Return"]))


if risk_level == "High Risk":
    st.error("High risk warning: Portfolio shows elevated volatility, drawdown, or negative recent trend.")
elif risk_level == "Medium Risk":
    st.warning("Medium risk signal: Portfolio should be monitored closely.")
else:
    st.success("Low risk signal: Portfolio appears relatively stable based on selected metrics.")


# ---------------------------------------------------------
# Price Trend Chart
# ---------------------------------------------------------
st.header("2. Stock Price Trend")

fig_price = px.line(
    market_data,
    x="Date",
    y="Close",
    color="Ticker",
    title="Adjusted Closing Price Trend"
)

st.plotly_chart(fig_price, use_container_width=True)


# ---------------------------------------------------------
# Risk Metrics Table
# ---------------------------------------------------------
st.header("3. Individual Stock Risk Metrics")

display_metrics = metrics_df.copy()
display_metrics["Latest Price"] = display_metrics["Latest Price"].map("${:,.2f}".format)
display_metrics["Total Return"] = display_metrics["Total Return"].map(format_percent)
display_metrics["Annualized Volatility"] = display_metrics["Annualized Volatility"].map(format_percent)
display_metrics["Max Drawdown"] = display_metrics["Max Drawdown"].map(format_percent)
display_metrics["20D Return"] = display_metrics["20D Return"].map(format_percent)
display_metrics["20D Volatility"] = display_metrics["20D Volatility"].map(format_percent)

st.dataframe(display_metrics, use_container_width=True)


# ---------------------------------------------------------
# Risk Contribution Chart
# ---------------------------------------------------------
st.header("4. Risk Contribution by Stock")

risk_contribution = metrics_df.copy()
risk_contribution["Weight"] = risk_contribution["Ticker"].map(weights)
risk_contribution["Weighted Volatility"] = (
    risk_contribution["Annualized Volatility"] * risk_contribution["Weight"]
)

fig_risk = px.bar(
    risk_contribution,
    x="Ticker",
    y="Weighted Volatility",
    title="Weighted Volatility Contribution by Stock",
    text_auto=".2%"
)

st.plotly_chart(fig_risk, use_container_width=True)


# ---------------------------------------------------------
# Drawdown Chart
# ---------------------------------------------------------
st.header("5. Drawdown Analysis")

drawdown_data = []

for ticker in market_data["Ticker"].unique():
    temp = market_data[market_data["Ticker"] == ticker].copy()
    temp = temp.sort_values("Date")
    temp["Daily_Return"] = temp["Close"].pct_change()
    temp["Cumulative_Return"] = (1 + temp["Daily_Return"]).cumprod()
    temp["Rolling_Max"] = temp["Cumulative_Return"].cummax()
    temp["Drawdown"] = (temp["Cumulative_Return"] - temp["Rolling_Max"]) / temp["Rolling_Max"]
    drawdown_data.append(temp[["Date", "Ticker", "Drawdown"]])

drawdown_df = pd.concat(drawdown_data)

fig_drawdown = px.line(
    drawdown_df,
    x="Date",
    y="Drawdown",
    color="Ticker",
    title="Historical Drawdown by Stock"
)

fig_drawdown.update_yaxes(tickformat=".0%")
st.plotly_chart(fig_drawdown, use_container_width=True)


# ---------------------------------------------------------
# Stress Testing
# ---------------------------------------------------------
st.header("6. Basic Stress Test")

stress_drop = st.slider(
    "Assume market drops by:",
    min_value=1,
    max_value=30,
    value=10,
    step=1
)

estimated_loss = -stress_drop / 100

st.metric(
    "Estimated Portfolio Impact",
    format_percent(estimated_loss)
)

st.markdown(
    f"""
    If the selected portfolio experiences a **{stress_drop}% market shock**, 
    the estimated short-term portfolio impact would be approximately 
    **{format_percent(estimated_loss)}** before considering hedging, rebalancing, or company-specific differences.
    """
)


# ---------------------------------------------------------
# Educational Recommendations
# ---------------------------------------------------------
st.header("7. Risk Insights & Educational Recommendations")

recommendations = []

if portfolio_metrics["Portfolio Volatility"] > 0.35:
    recommendations.append("Portfolio volatility is elevated. Consider monitoring high-volatility holdings closely.")

if portfolio_metrics["Portfolio Drawdown"] < -0.25:
    recommendations.append("Portfolio has experienced a meaningful historical drawdown. Review downside exposure.")

if portfolio_metrics["Portfolio 20D Return"] < 0:
    recommendations.append("Recent 20-day performance is negative. Watch for continued downside momentum.")

top_risk_stock = risk_contribution.sort_values("Weighted Volatility", ascending=False).iloc[0]["Ticker"]
recommendations.append(f"{top_risk_stock} currently contributes the highest weighted volatility risk.")

for rec in recommendations:
    st.info(rec)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(
    "Built as a portfolio project using Python, Streamlit, yfinance, Pandas, Plotly, and risk analytics methodology."
)
