# App Features

## Overview

The Real-Time Investor Risk Intelligence Platform is an interactive Streamlit application designed to help users analyze portfolio risk using latest available market data, benchmark comparison, stress testing, and machine learning-based risk classification.

The app is built to be more than a static dashboard. It allows users to interact with portfolio inputs, update tickers, adjust weights, compare against benchmarks, review model predictions, and download risk metrics.

## Main Application Features

The application includes the following major features:

* Custom portfolio ticker input
* Portfolio weight adjustment
* Latest available market data retrieval
* Portfolio risk score
* Portfolio risk level
* Market benchmark indicators
* SPY and QQQ comparison
* VIX-style market risk signal
* Portfolio overview charts
* Machine learning risk model tab
* Stock-level ML predictions
* Portfolio-level ML prediction
* Risk contribution analysis
* Drawdown analysis
* Stress testing
* Downloadable risk metrics
* Professional Streamlit user interface

## 1. Portfolio Control Panel

The sidebar acts as the main control panel for the application.

Users can enter custom ticker symbols such as:

```text
AAPL, MSFT, NVDA, JPM, TSLA
```

Users can also select the historical period:

```text
6mo
1y
2y
5y
```

The app uses these inputs to retrieve latest available market data and update all charts, metrics, and model predictions.

## 2. Portfolio Weight Inputs

The sidebar allows users to assign a portfolio weight to each selected ticker.

Example:

```text
AAPL = 20%
MSFT = 20%
NVDA = 20%
JPM = 20%
TSLA = 20%
```

If total weights do not equal 100%, the app normalizes the weights automatically for risk calculations.

This makes the app easier to use because users do not need perfect input values for the analysis to work.

## 3. Refresh Market Data Button

The sidebar includes a refresh button that clears the app cache and reloads market data.

This feature allows users to request updated market data without restarting the application.

The app also uses a cache duration of 15 minutes to avoid unnecessary repeated data downloads.

## 4. Portfolio Risk Snapshot

The Portfolio Risk Snapshot appears at the top of the app.

It displays key portfolio metrics using professional KPI cards.

Metrics include:

* Risk Score
* Risk Level
* Portfolio Return
* Portfolio Volatility
* Estimated Max Drawdown
* Recent 20-Day Return
* Tracked Securities
* Market Signal
* ML Portfolio Risk
* ML Confidence

This section gives users a quick executive-level view of the portfolio’s current risk condition.

## 5. Rule-Based Portfolio Risk Score

The app calculates a rule-based risk score from 0 to 100.

The score uses:

* Portfolio volatility
* Portfolio drawdown
* Recent 20-day return
* Total portfolio return

Risk levels are classified as:

| Score Range | Risk Level  |
| ----------- | ----------- |
| 0 to 34.9   | Low Risk    |
| 35 to 69.9  | Medium Risk |
| 70 to 100   | High Risk   |

This helps users quickly understand whether their portfolio appears relatively stable or elevated in risk.

## 6. Market Overview Tab

The Market Overview tab provides broader market context.

It includes:

* SPY benchmark metrics
* QQQ benchmark metrics
* VIX volatility proxy metrics
* Market risk score
* Market risk level
* Market signal explanation
* SPY vs QQQ indexed performance chart
* Portfolio vs SPY and QQQ comparison chart

This feature helps users understand whether portfolio risk is being influenced by broader market conditions.

## 7. Benchmark Indicators

The app uses three benchmark indicators:

```text
SPY
QQQ
^VIX
```

SPY is used as a broad market benchmark proxy.

QQQ is used as a technology-heavy benchmark proxy.

VIX is used as a market volatility and fear proxy.

The benchmark indicators support market risk classification and portfolio comparison.

## 8. Market Risk Signal

The app generates a simplified market risk signal.

Possible market signals include:

* Calm Market
* Cautious Market
* High-Risk Market

The signal is based on:

* SPY 20-day return
* SPY 20-day volatility
* QQQ 20-day return
* VIX level

This helps users understand whether the broader market environment appears stable or risky.

## 9. Portfolio Overview Tab

The Portfolio Overview tab shows how selected holdings performed over the selected historical period.

It includes:

* Indexed stock price performance chart
* Portfolio holdings summary table
* Latest price
* Portfolio weight
* Total return
* Annualized volatility
* Maximum drawdown
* 20-day return
* Trend status

The indexed chart converts all holdings to a starting value of 100, making it easier to compare stocks with different price levels.

## 10. ML Risk Model Tab

The ML Risk Model tab displays machine learning-based risk classification.

It includes:

* Portfolio ML risk level
* ML confidence
* Model type
* Portfolio probability breakdown
* Stock-level ML risk predictions
* Top model features
* Model methodology explanation

The ML model classifies risk as:

* Low Risk
* Medium Risk
* High Risk

This tab makes the project a solution-based analytics application instead of only a visualization project.

## 11. Stock-Level ML Predictions

For each selected stock, the app displays:

* Ticker
* Portfolio weight
* Predicted risk level
* Confidence
* Probability of each risk class

This helps users identify whether specific holdings are showing higher predicted risk based on the baseline model.

## 12. Portfolio-Level ML Prediction

The app combines stock-level risk probabilities using portfolio weights.

The final portfolio ML risk level is based on the weighted probability of each risk class.

Example:

```text
Portfolio ML Risk = Medium Risk
ML Confidence = 52%
```

This allows the app to summarize multiple stock-level predictions into one portfolio-level model signal.

## 13. Feature Importance Chart

The ML Risk Model tab includes a feature importance chart.

Feature importance helps explain which variables had the most influence on the Random Forest model.

Examples of model features include:

* VIX level
* SPY volatility
* Stock return
* Rolling volatility
* Moving average gap
* Drawdown

This feature improves model transparency and makes the project easier to explain.

## 14. Risk Contributors Tab

The Risk Contributors tab identifies which holdings contribute the most weighted volatility risk.

The app calculates:

```text
Weighted Volatility = Asset Annualized Volatility × Portfolio Weight
```

The tab includes:

* Weighted volatility contribution bar chart
* Top risk contributor insight
* Investor-focused risk recommendations

This helps users understand which holdings are driving portfolio volatility.

## 15. Drawdown Analysis Tab

The Drawdown Analysis tab shows downside risk over time.

It includes:

* Historical drawdown by stock
* Worst drawdown summary
* SPY and QQQ benchmark drawdown context

Drawdown analysis helps users understand how much each holding declined from previous peaks.

This is important because a portfolio can have positive total return while still experiencing large temporary losses.

## 16. Stress Testing Tab

The Stress Testing tab allows users to simulate a downside market shock.

Users can select a shock level from:

```text
1% to 40%
```

The app calculates:

* Scenario shock
* Estimated portfolio impact
* Value after shock
* Holding-level weighted impact

This feature helps users understand potential downside exposure under simplified stress conditions.

## 17. Holding-Level Shock Impact

The stress testing section also displays holding-level weighted impact.

For each ticker, the table shows:

* Ticker
* Weight
* Assumed shock
* Weighted impact

This makes the stress test more transparent and easier to interpret.

## 18. Data & Downloads Tab

The Data & Downloads tab shows the underlying data used in the app.

It includes:

* Raw market data preview
* Benchmark data preview
* Downloadable portfolio risk metrics CSV
* Downloadable benchmark metrics CSV

This feature makes the project more practical and transparent because users can export the calculated metrics.

## 19. Professional UI Design

The app uses custom Streamlit styling to create a more professional appearance.

UI elements include:

* Custom title section
* Subtitle description
* Section cards
* Metric cards
* Risk alert boxes
* Tabs for navigation
* Clean tables
* Interactive Plotly charts

The design is intended to look more like a professional financial analytics product than a basic Streamlit demo.

## 20. Educational Disclaimer

The app includes a clear disclaimer that the project is for educational and portfolio demonstration purposes only.

The platform does not provide:

* Buy recommendations
* Sell recommendations
* Trading signals
* Personalized investment advice
* Broker account integration
* Institutional risk management output

## User Workflow

A typical user workflow is:

1. Open the Streamlit app
2. Enter portfolio ticker symbols
3. Adjust portfolio weights
4. Select historical data period
5. Review portfolio risk snapshot
6. Check market benchmark indicators
7. Compare portfolio vs SPY and QQQ
8. Review ML risk classification
9. Identify top risk contributors
10. Analyze drawdown exposure
11. Run stress test scenarios
12. Download risk metrics if needed

## Value of the App

The app provides value because it combines multiple risk views into one interactive platform.

Users can see:

* What the portfolio risk level is
* Why risk may be elevated
* Which holdings contribute the most risk
* How the portfolio compares with benchmarks
* What the ML model predicts
* What may happen under a downside scenario

## Current App Tabs

The current version includes these tabs:

```text
Market Overview
Portfolio Overview
ML Risk Model
Risk Contributors
Drawdown Analysis
Stress Testing
Data & Downloads
```

## Current Version Features

The current application version includes:

* Version 1.0: Initial working Streamlit app
* Version 1.1: Professional UI upgrade
* Version 1.2: Market benchmark indicators
* Version 2.0: Baseline machine learning risk model
* Version 2.1: ML model connected to Streamlit app

## Future Feature Enhancements

Future versions may include:

* Live deployed Streamlit app
* Sector allocation analysis
* Correlation heatmap
* Portfolio beta calculation
* Sharpe ratio
* Sortino ratio
* Value at Risk
* Conditional Value at Risk
* FRED macroeconomic indicators
* Interest rate indicators
* Inflation indicators
* Saved portfolio templates
* Authentication
* Automated model retraining
* SHAP-based model explanation
* More advanced stress testing
* Portfolio optimization

## Important Disclaimer

This app is for educational and portfolio demonstration purposes only. It is not financial advice, investment advice, or a trading recommendation. The risk metrics and model outputs are simplified analytical indicators and should not be used as the sole basis for investment decisions.
