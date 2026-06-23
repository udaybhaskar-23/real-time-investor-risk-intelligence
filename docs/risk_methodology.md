# Risk Methodology

## Overview

This document explains the risk methodology used in the Real-Time Investor Risk Intelligence Platform.

The project uses a combination of rule-based risk scoring, portfolio analytics, benchmark comparison, drawdown analysis, volatility analysis, stress testing, and machine learning classification to help users understand portfolio risk.

The methodology is designed for educational and portfolio demonstration purposes. It is not intended to replace professional risk management systems or investment advisory tools.

## Risk Methodology Objectives

The main objectives of the risk methodology are to:

* Measure portfolio return and volatility
* Estimate downside exposure using drawdown analysis
* Identify which holdings contribute the most portfolio risk
* Compare portfolio behavior against broader market benchmarks
* Detect market risk conditions using SPY, QQQ, and VIX-style signals
* Simulate downside shock scenarios
* Classify portfolio risk using a baseline machine learning model
* Present risk insights in a simple, investor-friendly way

## Core Risk Metrics

## 1. Daily Return

Daily return measures the percentage change in a security’s closing price from one trading day to the next.

Formula:

```text
Daily Return = (Current Close Price / Previous Close Price) - 1
```

Daily returns are used as the foundation for volatility, cumulative return, drawdown, and machine learning features.

## 2. Total Return

Total return measures the percentage gain or loss over the selected historical period.

Formula:

```text
Total Return = (Latest Close Price / Starting Close Price) - 1
```

This helps users understand how much each holding has gained or lost during the selected time window.

## 3. Portfolio Return

Portfolio return is calculated as a weighted average of individual holding returns.

Formula:

```text
Portfolio Return = Sum(Individual Asset Return × Portfolio Weight)
```

If user-entered weights do not equal 100%, the application normalizes the weights before calculating portfolio metrics.

## 4. Annualized Volatility

Volatility measures the degree of price movement or uncertainty in returns.

The app calculates annualized volatility from daily returns.

Formula:

```text
Annualized Volatility = Standard Deviation of Daily Returns × Square Root of 252
```

The number 252 is used because there are approximately 252 trading days in a year.

Higher volatility generally indicates higher uncertainty and higher risk.

## 5. Portfolio Volatility

Portfolio volatility is estimated using a weighted average of individual annualized volatility values.

Formula:

```text
Portfolio Volatility = Sum(Individual Asset Volatility × Portfolio Weight)
```

This is a simplified portfolio volatility approach. It does not fully account for covariance between securities in the current version.

## 6. Cumulative Return

Cumulative return tracks how an investment grows or declines over time.

Formula:

```text
Cumulative Return = Cumulative Product of (1 + Daily Return)
```

Cumulative return is used to calculate drawdown and indexed performance charts.

## 7. Drawdown

Drawdown measures how far an investment has declined from its previous peak.

Formula:

```text
Drawdown = (Current Cumulative Return - Previous Peak Cumulative Return) / Previous Peak Cumulative Return
```

Drawdown is important because it shows downside exposure, not just average performance.

## 8. Maximum Drawdown

Maximum drawdown is the largest observed decline from a previous peak during the selected period.

Formula:

```text
Maximum Drawdown = Minimum Drawdown Value During the Selected Period
```

A more negative maximum drawdown indicates greater downside risk.

## 9. Recent 20-Day Return

The 20-day return measures recent short-term momentum.

Formula:

```text
20-Day Return = (Current Close Price / Close Price 20 Trading Days Ago) - 1
```

This metric is used to understand whether a holding or benchmark has positive or negative short-term trend behavior.

## 10. Recent 20-Day Volatility

Recent 20-day volatility measures short-term price uncertainty.

Formula:

```text
20-Day Volatility = Standard Deviation of Recent 20 Daily Returns × Square Root of 252
```

This helps identify whether risk has recently increased.

## Portfolio Weighting Methodology

The app allows users to enter portfolio weights manually.

Example:

```text
AAPL = 20%
MSFT = 20%
NVDA = 20%
JPM = 20%
TSLA = 20%
```

If the total weight is not exactly 100%, the app normalizes the weights.

Example:

```text
If total entered weight = 120%
Normalized Weight = Individual Weight / Total Entered Weight
```

This prevents calculation errors and allows the app to continue functioning even when user inputs are not perfect.

## Portfolio Risk Score Methodology

The application includes a rule-based portfolio risk score ranging from:

```text
0 to 100
```

A higher score indicates higher estimated risk.

The score is based on four components:

1. Portfolio volatility
2. Portfolio drawdown
3. Recent 20-day return trend
4. Total portfolio return

## Risk Score Components

## 1. Volatility Score

The volatility score measures how high the portfolio volatility is relative to a selected threshold.

Higher volatility increases the risk score.

Simplified logic:

```text
Volatility Score = Min(Portfolio Volatility / 50%, 1) × 35
```

Maximum contribution:

```text
35 points
```

## 2. Drawdown Score

The drawdown score measures how severe the portfolio’s historical decline has been.

Larger negative drawdowns increase the risk score.

Simplified logic:

```text
Drawdown Score = Min(Absolute Portfolio Drawdown / 40%, 1) × 35
```

Maximum contribution:

```text
35 points
```

## 3. Trend Score

The trend score uses recent 20-day portfolio return.

Logic:

```text
If 20-day return < -5% → 20 points
If 20-day return < 0%  → 10 points
If 20-day return >= 0% → 3 points
```

Maximum contribution:

```text
20 points
```

## 4. Return Score

The return score adds risk points if total portfolio return is negative.

Logic:

```text
If total portfolio return < 0% → 10 points
If total portfolio return >= 0% → 2 points
```

Maximum contribution:

```text
10 points
```

## Final Risk Score

The total risk score is calculated as:

```text
Risk Score = Volatility Score + Drawdown Score + Trend Score + Return Score
```

The score is capped at:

```text
100
```

## Risk Level Classification

The rule-based risk score is converted into a simple risk level:

| Risk Score Range | Risk Level  |
| ---------------- | ----------- |
| 0 to 34.9        | Low Risk    |
| 35 to 69.9       | Medium Risk |
| 70 to 100        | High Risk   |

## Risk Contribution Methodology

The app identifies which holdings contribute the most risk using weighted volatility.

Formula:

```text
Weighted Volatility Contribution = Asset Annualized Volatility × Asset Portfolio Weight
```

This helps users identify which stock is contributing the most to portfolio volatility.

Example:

```text
If NVDA has high volatility and a large portfolio weight, it may become the top risk contributor.
```

## Benchmark Methodology

The project uses benchmark indicators to provide market context.

Benchmarks used:

```text
SPY
QQQ
^VIX
```

## SPY Benchmark

SPY is used as a broad market proxy.

It helps answer:

* Is the portfolio outperforming or underperforming the broad market?
* Is the broad market showing negative momentum?
* Is broad market volatility elevated?

## QQQ Benchmark

QQQ is used as a technology-heavy benchmark proxy.

It helps answer:

* Is the portfolio behaving like a growth or technology-heavy portfolio?
* Is tech-heavy market risk increasing?
* Is QQQ showing negative short-term momentum?

## VIX Volatility Proxy

VIX is used as a market volatility and fear proxy.

It helps identify whether market conditions appear:

* Calm
* Cautious
* High risk

## Market Risk Signal Methodology

The app creates a simplified market risk signal using SPY, QQQ, and VIX behavior.

The market signal is based on:

* SPY 20-day return
* SPY 20-day volatility
* QQQ 20-day return
* Latest VIX level

## Market Signal Logic

Risk points are added when benchmark conditions weaken.

Examples:

```text
SPY declines more than 5% over 20 days → Add risk points
SPY has negative 20-day return → Add risk points
SPY 20-day volatility is elevated → Add risk points
QQQ declines more than 5% over 20 days → Add risk points
VIX above 20 → Add caution points
VIX above 30 → Add high-risk points
```

## Market Signal Categories

| Market Risk Score | Market Signal    |
| ----------------- | ---------------- |
| 0 to 29           | Calm Market      |
| 30 to 64          | Cautious Market  |
| 65 to 100         | High-Risk Market |

## Indexed Performance Methodology

The app converts each selected asset and benchmark into an indexed value starting at 100.

Formula:

```text
Price Index = Current Close Price / Starting Close Price × 100
```

This makes securities with different price levels easier to compare visually.

Example:

```text
A stock priced at $50 and a stock priced at $500 can both be compared from a starting index level of 100.
```

## Drawdown Methodology

Drawdown charts are created for each selected holding and benchmark.

The app calculates:

* Cumulative return
* Rolling peak value
* Drawdown from peak

This helps users understand downside exposure over time.

Drawdown is especially useful because a portfolio can show positive total return while still having experienced severe declines during the selected period.

## Stress Testing Methodology

The stress testing module allows users to simulate a downside market shock.

The current version supports market shock scenarios from:

```text
1% to 40%
```

The simplified impact is calculated as:

```text
Estimated Portfolio Impact = -Selected Shock Percentage
```

Holding-level weighted impact is calculated as:

```text
Weighted Impact = Portfolio Weight × Assumed Shock
```

## Stress Testing Example

If the user selects a 10% market shock:

```text
Scenario Shock = -10%
Estimated Portfolio Impact = -10%
```

For a holding with a 20% weight:

```text
Holding Weighted Impact = 20% × -10% = -2%
```

## Machine Learning Risk Methodology

The project includes a baseline Random Forest classification model.

The model predicts:

```text
Low Risk
Medium Risk
High Risk
```

The model is trained using historical stock and benchmark data.

## ML Target Label Methodology

The model label is based on future 5-day return behavior.

Label rules:

| Future 5-Day Return                            | Risk Label  |
| ---------------------------------------------- | ----------- |
| Less than or equal to -3%                      | High Risk   |
| Greater than -3% and less than or equal to +1% | Medium Risk |
| Greater than +1%                               | Low Risk    |

## ML Feature Categories

The model uses features from several categories.

## Stock Return Features

* Daily return
* 5-day return
* 20-day return

## Stock Volatility Features

* 20-day volatility
* 60-day volatility

## Drawdown Features

* 60-day maximum drawdown

## Trend Features

* 20-day moving average gap
* 50-day moving average gap

## Volume Features

* 20-day volume change

## Benchmark Features

* SPY 20-day return
* SPY 20-day volatility
* QQQ 20-day return
* VIX level
* VIX 20-day change

## ML Prediction Output

The app displays:

* Portfolio ML risk level
* ML confidence score
* Portfolio probability breakdown
* Stock-level ML risk predictions
* Feature importance chart
* Model methodology explanation

## Model Confidence

Model confidence is calculated from the predicted class probability.

Example:

```text
If the model predicts Medium Risk with 62% probability, the confidence is 62%.
```

## Portfolio-Level ML Prediction

The app creates a portfolio-level ML risk signal by combining stock-level prediction probabilities using portfolio weights.

Simplified logic:

```text
Portfolio Probability = Sum(Stock Risk Probability × Stock Weight)
```

The final portfolio ML risk level is the class with the highest weighted probability.

## Why Use Both Rule-Based and ML Risk Scores?

The project uses both approaches because they serve different purposes.

## Rule-Based Risk Score

The rule-based score is:

* Easy to explain
* Transparent
* Based on clear risk logic
* Useful for quick interpretation

## Machine Learning Risk Model

The ML model is:

* Data-driven
* Learns patterns from historical market behavior
* Uses multiple features at once
* Provides probability-based classification

Together, they create a stronger risk intelligence solution.

## Methodology Limitations

The current methodology has limitations:

* Portfolio volatility is simplified and does not fully account for covariance
* Free market data may be delayed or incomplete
* The ML model is a baseline model
* Model accuracy is not high enough for investment use
* Historical data does not guarantee future outcomes
* The app does not provide buy, sell, or hold recommendations
* Stress testing is simplified
* Macroeconomic indicators are not included yet
* Transaction costs and taxes are not included
* Sector concentration is not included yet

## Future Methodology Improvements

Future versions may include:

* Covariance-based portfolio volatility
* Value at Risk
* Conditional Value at Risk
* Sharpe ratio
* Sortino ratio
* Beta vs benchmark
* Correlation heatmap
* Sector concentration analysis
* Macro indicators from FRED
* Advanced stress testing
* SHAP model explanation
* Model retraining workflow
* Time-series cross-validation
* Portfolio optimization

## Important Disclaimer

This risk methodology is designed for educational and portfolio demonstration purposes only. It is not financial advice, investment advice, or a trading recommendation. Risk scores and model predictions should be interpreted as simplified analytical indicators, not as investment decisions.
