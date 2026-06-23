# Limitations and Future Work

## Overview

This document explains the current limitations of the Real-Time Investor Risk Intelligence Platform and outlines future improvements that can make the project more advanced, reliable, and useful.

The current version is a strong educational and portfolio demonstration project. It includes latest available market data, portfolio risk scoring, benchmark comparison, stress testing, and a baseline machine learning risk model. However, it is not intended to be a production-grade financial risk system.

## Current Project Limitations

## 1. Data Source Limitations

The current version uses Yahoo Finance-style market data through the `yfinance` Python library.

This is useful for educational development, but it has limitations:

* Data may be delayed
* Data availability may vary by ticker
* Some tickers may fail temporarily
* Intraday market data is not used in the current version
* The project does not use paid institutional-grade real-time feeds
* The app does not currently validate data against multiple providers

Because of this, the data should be treated as suitable for portfolio demonstration purposes, not professional trading or investment decision-making.

## 2. Real-Time Data Limitation

The project is described as using latest available market data, but it is not a true institutional real-time trading platform.

The app refreshes data using a cached function, and users can manually refresh market data from the sidebar.

Current cache duration:

```text
900 seconds
```

This equals:

```text
15 minutes
```

The current version is better described as:

```text
Latest available market data / near real-time portfolio risk monitoring
```

## 3. Simplified Portfolio Volatility

The current portfolio volatility calculation uses a weighted average of individual asset volatility.

This is simple and easy to explain, but it does not fully account for covariance or correlation between holdings.

A more advanced version should calculate portfolio volatility using a covariance matrix.

Future formula:

```text
Portfolio Variance = Wᵀ × Covariance Matrix × W
Portfolio Volatility = Square Root of Portfolio Variance
```

This would make the risk methodology more accurate.

## 4. Limited Benchmark Coverage

The current version uses:

```text
SPY
QQQ
^VIX
```

These are useful benchmark indicators, but they do not fully represent all market conditions.

The app does not yet include:

* Sector ETFs
* Bond market indicators
* Commodity indicators
* Currency indicators
* Cryptocurrency indicators
* International market benchmarks
* Interest rate indicators
* Inflation indicators

## 5. Limited Macro Risk Context

The current version does not include macroeconomic indicators.

Missing macro indicators include:

* Federal funds rate
* Treasury yields
* Inflation data
* CPI
* Unemployment rate
* GDP growth
* Consumer sentiment
* Credit spreads
* Recession indicators

Adding macroeconomic data would make the platform more useful for financial risk analysis.

## 6. Baseline Machine Learning Model

The current machine learning model is a baseline Random Forest classifier.

It is useful for demonstrating an end-to-end machine learning workflow, but it is not a production-grade financial model.

Current model limitations include:

* Limited training universe
* Limited historical feature set
* Moderate baseline accuracy
* No time-series cross-validation
* No hyperparameter tuning workflow
* No advanced explainability method
* No automated retraining process
* No external validation dataset

## 7. Model Accuracy Limitation

The baseline model achieved approximately:

```text
48.43% accuracy
```

This result is acceptable for a first project version because financial market classification is difficult and noisy.

However, this accuracy is not strong enough for actual investment decision-making.

The model should be presented as:

```text
A baseline educational machine learning risk classification model
```

not as a trading or investment prediction model.

## 8. Simplified Risk Labels

The model target labels are based on future 5-day return thresholds.

Current label logic:

| Future 5-Day Return                            | Risk Label  |
| ---------------------------------------------- | ----------- |
| Less than or equal to -3%                      | High Risk   |
| Greater than -3% and less than or equal to +1% | Medium Risk |
| Greater than +1%                               | Low Risk    |

This is simple and explainable, but it may not capture all dimensions of risk.

Future versions may use more advanced labeling based on:

* Future volatility
* Future drawdown
* Value at Risk
* Benchmark-relative losses
* Multi-factor risk conditions
* Market regime classification

## 9. No Portfolio Optimization

The current app identifies risk but does not recommend an optimized portfolio allocation.

It does not currently calculate:

* Minimum volatility portfolio
* Maximum Sharpe ratio portfolio
* Efficient frontier
* Risk parity allocation
* Diversification optimization

These can be added in future versions.

## 10. No Buy or Sell Recommendations

The application does not provide investment recommendations.

It does not tell users to:

* Buy a stock
* Sell a stock
* Hold a stock
* Rebalance a portfolio
* Time the market

This is intentional. The project is positioned as a risk intelligence and educational analytics platform, not a financial advisory tool.

## 11. Simplified Stress Testing

The current stress test applies a simple percentage shock to the portfolio.

It does not account for:

* Different shock levels by asset
* Sector-specific shocks
* Correlation changes during stress
* Liquidity risk
* Volatility spikes
* Interest rate shocks
* Credit shocks
* Company-specific event risk

Future stress testing can become more advanced by introducing multiple scenario types.

## 12. No Sector Concentration Analysis

The current version does not classify tickers by sector.

Because of this, the app cannot yet show:

* Technology exposure
* Financial sector exposure
* Energy exposure
* Healthcare exposure
* Consumer sector exposure
* Sector concentration risk

Adding sector classification would make the project more useful for investors.

## 13. No Correlation Analysis

The app currently does not include a correlation matrix or heatmap.

Correlation analysis would help users understand whether holdings move together.

Future features may include:

* Stock correlation heatmap
* Portfolio diversification score
* Correlation with SPY
* Correlation with QQQ
* Rolling correlation analysis

## 14. No Value at Risk

The current version does not calculate Value at Risk.

Future versions may include:

* Historical Value at Risk
* Parametric Value at Risk
* Conditional Value at Risk
* Portfolio expected shortfall

These would make the project stronger for risk management roles.

## 15. No Authentication or Saved Portfolios

The current Streamlit app does not include user login or saved portfolio functionality.

Users must manually enter tickers and weights each time.

Future versions may include:

* Saved portfolio templates
* User authentication
* Portfolio history
* Watchlists
* Stored risk reports

## 16. No Database Layer

The current project does not use a database.

Data is either downloaded dynamically or generated during model training.

Future versions may include:

* SQLite database
* PostgreSQL database
* Historical risk score storage
* Daily portfolio snapshot storage
* Model prediction history

## 17. Deployment Not Yet Finalized

The current project runs locally.

A future version should be deployed using Streamlit Community Cloud or another hosting platform.

Deployment would allow users and recruiters to access the app from a live URL.

## 18. No Automated Data Pipeline

The project currently refreshes data manually when the app runs or when the user clicks the refresh button.

A more advanced version could include:

* Scheduled data refresh
* Automated model retraining
* GitHub Actions workflow
* API-based data pipeline
* Data quality checks

## 19. No Advanced Model Explainability

The current app uses Random Forest feature importance.

This is useful, but it is not the most advanced explainability method.

Future versions could include:

* SHAP values
* Local explanation for each prediction
* Feature contribution by stock
* Model confidence monitoring
* Prediction drift detection

## 20. Educational Disclaimer Requirement

Because this project deals with financial data and risk interpretation, it must always include a disclaimer.

The app should clearly state that it is:

* For educational purposes
* For portfolio demonstration
* Not financial advice
* Not a trading recommendation
* Not a substitute for professional investment guidance

## Future Work Roadmap

## Phase 1: Deployment

Deploy the Streamlit app so it can be accessed publicly.

Planned tasks:

* Prepare app for Streamlit Community Cloud
* Confirm `requirements.txt` works
* Test model loading in deployed environment
* Add live app link to README
* Add live app link to portfolio webpage

## Phase 2: README and Wiki Documentation

Create final GitHub documentation.

Planned tasks:

* Write professional README
* Add screenshots
* Add project architecture
* Add model methodology
* Add risk methodology
* Create GitHub Wiki pages
* Add navigation links

## Phase 3: Advanced Risk Metrics

Add more professional finance risk metrics.

Potential additions:

* Sharpe ratio
* Sortino ratio
* Beta vs SPY
* Alpha vs SPY
* Correlation matrix
* Covariance-based portfolio volatility
* Value at Risk
* Conditional Value at Risk
* Maximum drawdown duration

## Phase 4: Macro Risk Indicators

Add macroeconomic indicators using public data sources.

Potential additions:

* Treasury yield
* Federal funds rate
* Inflation
* Unemployment
* GDP growth
* Consumer sentiment
* Recession indicator

## Phase 5: Sector and Concentration Analysis

Add sector classification for selected tickers.

Potential outputs:

* Sector allocation chart
* Sector concentration score
* High concentration alert
* Sector-level risk contribution
* Sector benchmark comparison

## Phase 6: Model Improvement

Improve the machine learning model.

Potential improvements:

* Add more training tickers
* Add sector features
* Add macro features
* Add benchmark-relative features
* Try XGBoost or LightGBM
* Use time-series cross-validation
* Tune hyperparameters
* Track model performance over time
* Add SHAP explainability

## Phase 7: Portfolio Optimization

Add optimization capabilities.

Potential features:

* Minimum volatility portfolio
* Maximum Sharpe ratio portfolio
* Risk parity allocation
* Efficient frontier visualization
* Suggested diversification ranges

## Phase 8: Reporting Features

Add downloadable reports.

Potential outputs:

* Downloadable PDF risk report
* Downloadable CSV metrics
* Portfolio summary export
* ML prediction export
* Stress test report

## Phase 9: Database and History

Add a database layer.

Potential features:

* Store daily risk score
* Store portfolio snapshots
* Track historical ML predictions
* Track user-defined portfolios
* Compare current risk with previous risk

## Phase 10: Portfolio Webpage Integration

Add this project to the personal portfolio website.

Portfolio card should include:

* Project title
* Short business problem
* Tools used
* GitHub link
* Live app link
* Key features
* Project screenshot

## Final Project Positioning

This project should be positioned as:

```text
An interactive financial risk intelligence platform that combines latest available market data, benchmark indicators, stress testing, and a baseline machine learning model to help investors understand portfolio risk.
```

## Important Disclaimer

This project is for educational and portfolio demonstration purposes only. It is not financial advice, investment advice, or a trading recommendation. The limitations listed in this document should be considered when interpreting the project outputs.
