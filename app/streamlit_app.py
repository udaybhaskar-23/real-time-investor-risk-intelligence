import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Investor Risk Intelligence Platform",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #555;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .section-card {
        padding: 18px;
        border-radius: 14px;
        background-color: #f7f9fc;
        border: 1px solid #e6eaf0;
        margin-bottom: 18px;
    }

    .metric-card {
        padding: 18px;
        border-radius: 14px;
        background-color: #ffffff;
        border: 1px solid #e6eaf0;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.05);
    }

    .metric-label {
        font-size: 14px;
        color: #667085;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }

    .small-note {
        color: #667085;
        font-size: 13px;
    }

    .risk-low {
        padding: 12px;
        border-radius: 10px;
        background-color: #ecfdf3;
        border: 1px solid #abefc6;
        color: #027a48;
        font-weight: 600;
    }

    .risk-medium {
        padding: 12px;
        border-radius: 10px;
        background-color: #fffaeb;
        border: 1px solid #fedf89;
        color: #b54708;
        font-weight: 600;
    }

    .risk-high {
        padding: 12px;
        border-radius: 10px;
        background-color: #fef3f2;
        border: 1px solid #fecdca;
        color: #b42318;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def parse_tickers(ticker_text):
    tickers = [ticker.strip().upper() for ticker in ticker_text.split(",") if ticker.strip()]
    return list(dict.fromkeys(tickers))


@st.cache_data(ttl=900)
def load_market_data(tickers, period="1y"):
    """
    Downloads latest available market data using yfinance.
    Cache refreshes every 15 minutes.
    """
    try:
        raw_data = yf.download(
            tickers=tickers,
            period=period,
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            progress=False
        )

        if raw_data.empty:
            return pd.DataFrame()

        all_data = []

        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    temp = raw_data.copy()
                else:
                    temp = raw_data[ticker].copy()

                temp = temp.reset_index()
                temp["Ticker"] = ticker
                all_data.append(temp)

            except Exception:
                continue

        final_df = pd.concat(all_data, ignore_index=True)
        final_df.columns = [str(col).strip().title().replace(" ", "_") for col in final_df.columns]

        required_columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Ticker"]
        available_columns = [col for col in required_columns if col in final_df.columns]

        final_df = final_df[available_columns].copy()
        final_df["Date"] = pd.to_datetime(final_df["Date"])

        return final_df

    except Exception as error:
        st.error(f"Data loading error: {error}")
        return pd.DataFrame()


def add_risk_features(df):
    featured_data = []

    for ticker in df["Ticker"].unique():
        temp = df[df["Ticker"] == ticker].copy()
        temp = temp.sort_values("Date")

        temp["Daily_Return"] = temp["Close"].pct_change()
        temp["Cumulative_Return"] = (1 + temp["Daily_Return"]).cumprod()
        temp["Price_Index"] = temp["Close"] / temp["Close"].iloc[0] * 100
        temp["Rolling_Max"] = temp["Cumulative_Return"].cummax()
        temp["Drawdown"] = (temp["Cumulative_Return"] - temp["Rolling_Max"]) / temp["Rolling_Max"]
        temp["MA_20"] = temp["Close"].rolling(20).mean()
        temp["MA_50"] = temp["Close"].rolling(50).mean()
        temp["Rolling_Volatility_20D"] = temp["Daily_Return"].rolling(20).std() * np.sqrt(252)
        temp["Volume_Change"] = temp["Volume"].pct_change()

        featured_data.append(temp)

    return pd.concat(featured_data, ignore_index=True)


def calculate_asset_metrics(df):
    metrics = []

    for ticker in df["Ticker"].unique():
        temp = df[df["Ticker"] == ticker].copy()
        temp = temp.sort_values("Date")

        latest_price = temp["Close"].iloc[-1]
        start_price = temp["Close"].iloc[0]
        total_return = (latest_price / start_price) - 1
        annualized_volatility = temp["Daily_Return"].std() * np.sqrt(252)
        max_drawdown = temp["Drawdown"].min()
        recent_20d_return = temp["Close"].pct_change(20).iloc[-1]
        recent_20d_volatility = temp["Rolling_Volatility_20D"].iloc[-1]

        trend_status = "Positive Trend" if recent_20d_return >= 0 else "Negative Trend"

        metrics.append({
            "Ticker": ticker,
            "Latest Price": latest_price,
            "Total Return": total_return,
            "Annualized Volatility": annualized_volatility,
            "Max Drawdown": max_drawdown,
            "20D Return": recent_20d_return,
            "20D Volatility": recent_20d_volatility,
            "Trend Status": trend_status
        })

    return pd.DataFrame(metrics)


def normalize_weights(weights):
    total_weight = sum(weights.values())

    if total_weight <= 0:
        return weights

    return {ticker: weight / total_weight for ticker, weight in weights.items()}


def calculate_portfolio_metrics(metrics_df, weights):
    normalized_weights = normalize_weights(weights)

    temp = metrics_df.copy()
    temp["Weight"] = temp["Ticker"].map(normalized_weights)

    portfolio_return = (temp["Total Return"] * temp["Weight"]).sum()
    portfolio_volatility = (temp["Annualized Volatility"] * temp["Weight"]).sum()
    portfolio_drawdown = (temp["Max Drawdown"] * temp["Weight"]).sum()
    portfolio_20d_return = (temp["20D Return"] * temp["Weight"]).sum()

    return {
        "Portfolio Return": portfolio_return,
        "Portfolio Volatility": portfolio_volatility,
        "Portfolio Drawdown": portfolio_drawdown,
        "Portfolio 20D Return": portfolio_20d_return
    }


def calculate_risk_score(portfolio_metrics):
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
    if pd.isna(value):
        return "N/A"
    return f"{value:.2%}"


def format_currency(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def risk_message(risk_level, risk_score):
    if risk_level == "High Risk":
        css_class = "risk-high"
        message = f"High Risk Alert: Portfolio risk score is {risk_score}/100. Volatility, drawdown, or short-term negative trend is elevated."
    elif risk_level == "Medium Risk":
        css_class = "risk-medium"
        message = f"Medium Risk Signal: Portfolio risk score is {risk_score}/100. Portfolio should be monitored closely."
    else:
        css_class = "risk-low"
        message = f"Low Risk Signal: Portfolio risk score is {risk_score}/100. Portfolio appears relatively stable based on selected metrics."

    st.markdown(
        f"""
        <div class="{css_class}">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def create_recommendations(portfolio_metrics, risk_contribution):
    recommendations = []

    if portfolio_metrics["Portfolio Volatility"] > 0.35:
        recommendations.append("Portfolio volatility is elevated. Review high-volatility holdings and monitor daily price movement.")

    if portfolio_metrics["Portfolio Drawdown"] < -0.25:
        recommendations.append("Portfolio has experienced a meaningful historical drawdown. Review downside exposure and concentration risk.")

    if portfolio_metrics["Portfolio 20D Return"] < 0:
        recommendations.append("Recent 20-day return is negative. Watch for continued downside momentum.")

    top_risk_stock = risk_contribution.sort_values("Weighted Volatility", ascending=False).iloc[0]["Ticker"]
    recommendations.append(f"{top_risk_stock} is currently the largest weighted volatility contributor in this portfolio.")

    recommendations.append("This tool is designed for educational risk monitoring and should not be treated as investment advice.")

    return recommendations


# ---------------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------------
st.sidebar.title("Portfolio Control Panel")

st.sidebar.markdown(
    """
    Use this panel to test different portfolios and monitor risk signals.
    """
)

ticker_input = st.sidebar.text_input(
    "Stock tickers",
    value="AAPL, MSFT, NVDA, JPM, TSLA",
    help="Enter tickers separated by commas."
)

period = st.sidebar.selectbox(
    "Historical data period",
    ["6mo", "1y", "2y", "5y"],
    index=1
)

tickers = parse_tickers(ticker_input)

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
            step=1.0,
            key=f"weight_{ticker}"
        )
        weights[ticker] = weight / 100

total_weight = sum(weights.values())

st.sidebar.markdown("---")
st.sidebar.write(f"Total Weight: **{total_weight:.2%}**")

if total_weight <= 0:
    st.sidebar.error("Total portfolio weight must be greater than 0.")
    st.stop()

if abs(total_weight - 1.0) > 0.01:
    st.sidebar.warning("Weights do not total 100%. The app will normalize weights for calculations.")

if st.sidebar.button("Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()


# ---------------------------------------------------------
# Main Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-title">📊 Real-Time Investor Risk Intelligence Platform</div>
    <div class="subtitle">
        Interactive portfolio risk monitoring using latest available market data, volatility analytics, drawdown signals, and investor-focused risk scoring.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-card">
        <b>Project Purpose:</b> This solution helps investors understand portfolio risk exposure, identify major risk contributors,
        test downside scenarios, and convert market behavior into a clear risk score.
        <br><br>
        <b>Disclaimer:</b> This project is for educational and portfolio demonstration purposes only. It is not financial advice.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Load and Prepare Data
# ---------------------------------------------------------
if not tickers:
    st.warning("Please enter at least one ticker.")
    st.stop()

market_data = load_market_data(tickers, period)

if market_data.empty:
    st.error("No market data found. Please check the ticker symbols.")
    st.stop()

market_data = add_risk_features(market_data)
metrics_df = calculate_asset_metrics(market_data)
portfolio_metrics = calculate_portfolio_metrics(metrics_df, weights)
risk_score, risk_level = calculate_risk_score(portfolio_metrics)

normalized_weights = normalize_weights(weights)

risk_contribution = metrics_df.copy()
risk_contribution["Weight"] = risk_contribution["Ticker"].map(normalized_weights)
risk_contribution["Weighted Volatility"] = risk_contribution["Annualized Volatility"] * risk_contribution["Weight"]


# ---------------------------------------------------------
# Top KPI Section
# ---------------------------------------------------------
st.subheader("Portfolio Risk Snapshot")

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Risk Score", f"{risk_score}/100")

with col2:
    metric_card("Risk Level", risk_level)

with col3:
    metric_card("Portfolio Return", format_percent(portfolio_metrics["Portfolio Return"]))

with col4:
    metric_card("Portfolio Volatility", format_percent(portfolio_metrics["Portfolio Volatility"]))

col5, col6, col7 = st.columns(3)

with col5:
    metric_card("Estimated Max Drawdown", format_percent(portfolio_metrics["Portfolio Drawdown"]))

with col6:
    metric_card("Recent 20-Day Return", format_percent(portfolio_metrics["Portfolio 20D Return"]))

with col7:
    metric_card("Tracked Securities", str(len(tickers)))

risk_message(risk_level, risk_score)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# App Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Portfolio Overview",
        "Risk Contributors",
        "Drawdown Analysis",
        "Stress Testing",
        "Data & Downloads"
    ]
)


# ---------------------------------------------------------
# Tab 1: Portfolio Overview
# ---------------------------------------------------------
with tab1:
    st.subheader("Normalized Price Trend")

    st.markdown(
        """
        This chart converts each stock price to a starting value of 100, making it easier to compare performance across different price levels.
        """
    )

    fig_index = px.line(
        market_data,
        x="Date",
        y="Price_Index",
        color="Ticker",
        title="Indexed Stock Price Performance"
    )
    fig_index.update_layout(yaxis_title="Indexed Price Level", xaxis_title="Date")
    st.plotly_chart(fig_index, use_container_width=True)

    st.subheader("Portfolio Holdings Summary")

    holdings_summary = metrics_df.copy()
    holdings_summary["Weight"] = holdings_summary["Ticker"].map(normalized_weights)

    display_holdings = holdings_summary[
        [
            "Ticker",
            "Weight",
            "Latest Price",
            "Total Return",
            "Annualized Volatility",
            "Max Drawdown",
            "20D Return",
            "Trend Status"
        ]
    ].copy()

    display_holdings["Weight"] = display_holdings["Weight"].map(format_percent)
    display_holdings["Latest Price"] = display_holdings["Latest Price"].map(format_currency)
    display_holdings["Total Return"] = display_holdings["Total Return"].map(format_percent)
    display_holdings["Annualized Volatility"] = display_holdings["Annualized Volatility"].map(format_percent)
    display_holdings["Max Drawdown"] = display_holdings["Max Drawdown"].map(format_percent)
    display_holdings["20D Return"] = display_holdings["20D Return"].map(format_percent)

    st.dataframe(display_holdings, use_container_width=True)


# ---------------------------------------------------------
# Tab 2: Risk Contributors
# ---------------------------------------------------------
with tab2:
    st.subheader("Weighted Volatility Contribution")

    st.markdown(
        """
        This section identifies which holdings are contributing the most to portfolio risk based on position weight and annualized volatility.
        """
    )

    fig_risk = px.bar(
        risk_contribution.sort_values("Weighted Volatility", ascending=False),
        x="Ticker",
        y="Weighted Volatility",
        text_auto=".2%",
        title="Risk Contribution by Holding"
    )
    fig_risk.update_layout(yaxis_title="Weighted Volatility", xaxis_title="Ticker")
    fig_risk.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_risk, use_container_width=True)

    top_risk_stock = risk_contribution.sort_values("Weighted Volatility", ascending=False).iloc[0]

    st.info(
        f"{top_risk_stock['Ticker']} is currently the largest weighted risk contributor, "
        f"with a weighted volatility contribution of {format_percent(top_risk_stock['Weighted Volatility'])}."
    )

    st.subheader("Risk Insights")

    recommendations = create_recommendations(portfolio_metrics, risk_contribution)

    for recommendation in recommendations:
        st.write(f"• {recommendation}")


# ---------------------------------------------------------
# Tab 3: Drawdown Analysis
# ---------------------------------------------------------
with tab3:
    st.subheader("Historical Drawdown by Stock")

    st.markdown(
        """
        Drawdown measures how far an investment has declined from its previous peak.
        Larger negative drawdowns indicate higher downside risk.
        """
    )

    fig_drawdown = px.line(
        market_data,
        x="Date",
        y="Drawdown",
        color="Ticker",
        title="Historical Drawdown"
    )
    fig_drawdown.update_layout(yaxis_title="Drawdown", xaxis_title="Date")
    fig_drawdown.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_drawdown, use_container_width=True)

    worst_drawdown = metrics_df.sort_values("Max Drawdown").iloc[0]

    st.warning(
        f"{worst_drawdown['Ticker']} shows the largest historical drawdown in the selected period: "
        f"{format_percent(worst_drawdown['Max Drawdown'])}."
    )


# ---------------------------------------------------------
# Tab 4: Stress Testing
# ---------------------------------------------------------
with tab4:
    st.subheader("Portfolio Stress Test")

    st.markdown(
        """
        Use this section to simulate a simple market shock and estimate potential short-term portfolio impact.
        This is a simplified scenario tool and does not include hedging, liquidity, or company-specific event risk.
        """
    )

    stress_drop = st.slider(
        "Market shock scenario",
        min_value=1,
        max_value=40,
        value=10,
        step=1,
        format="%d%%"
    )

    estimated_loss = -stress_drop / 100

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        metric_card("Scenario Shock", f"-{stress_drop}%")

    with col_b:
        metric_card("Estimated Portfolio Impact", format_percent(estimated_loss))

    with col_c:
        estimated_value_after_shock = 1 + estimated_loss
        metric_card("Value After Shock", format_percent(estimated_value_after_shock))

    st.markdown(
        f"""
        A **{stress_drop}% downside market shock** would create an estimated portfolio impact of approximately 
        **{format_percent(estimated_loss)}** under this simplified stress scenario.
        """
    )

    st.subheader("Holding-Level Shock Impact")

    shock_table = risk_contribution[["Ticker", "Weight"]].copy()
    shock_table["Assumed Shock"] = estimated_loss
    shock_table["Weighted Impact"] = shock_table["Weight"] * estimated_loss

    display_shock = shock_table.copy()
    display_shock["Weight"] = display_shock["Weight"].map(format_percent)
    display_shock["Assumed Shock"] = display_shock["Assumed Shock"].map(format_percent)
    display_shock["Weighted Impact"] = display_shock["Weighted Impact"].map(format_percent)

    st.dataframe(display_shock, use_container_width=True)


# ---------------------------------------------------------
# Tab 5: Data & Downloads
# ---------------------------------------------------------
with tab5:
    st.subheader("Raw Market Data Preview")

    st.markdown(
        """
        This table shows the latest available market data used by the app.
        """
    )

    latest_rows = market_data.sort_values("Date", ascending=False).head(25)
    st.dataframe(latest_rows, use_container_width=True)

    st.subheader("Download Metrics")

    download_metrics = metrics_df.copy()
    download_metrics["Weight"] = download_metrics["Ticker"].map(normalized_weights)

    csv_data = download_metrics.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Portfolio Risk Metrics CSV",
        data=csv_data,
        file_name="portfolio_risk_metrics.csv",
        mime="text/csv"
    )

    st.markdown(
        f"""
        <div class="small-note">
        Latest app refresh: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(
    "Built with Python, Streamlit, Pandas, yfinance, Plotly, and portfolio risk analytics methodology."
)