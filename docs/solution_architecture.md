# Solution Architecture

## Overview

The Real-Time Investor Risk Intelligence Platform is designed as an end-to-end financial analytics solution that combines market data collection, data transformation, portfolio risk analytics, benchmark comparison, machine learning classification, and interactive visualization.

The architecture follows a simple but professional workflow:

1. Collect latest available market data
2. Clean and prepare the data
3. Engineer risk-related features
4. Calculate portfolio and benchmark metrics
5. Generate portfolio risk scores
6. Apply machine learning risk classification
7. Display insights through an interactive Streamlit application
8. Document results and methodology in GitHub

## Architecture Diagram

```text
User Inputs
   |
   |-- Stock Tickers
   |-- Portfolio Weights
   |-- Historical Period
   |
   v
Streamlit Application
   |
   v
Market Data Retrieval
   |
   |-- Selected Portfolio Tickers
   |-- SPY Benchmark
   |-- QQQ Benchmark
   |-- VIX Volatility Proxy
   |
   v
Data Processing Layer
   |
   |-- Date Formatting
   |-- Price Cleaning
   |-- Return Calculation
   |-- Volatility Calculation
   |-- Drawdown Calculation
   |-- Moving Average Features
   |
   v
Risk Analytics Layer
   |
   |-- Portfolio Return
   |-- Portfolio Volatility
   |-- Max Drawdown
   |-- Weighted Risk Contribution
   |-- Market Risk Signal
   |-- Stress Test Impact
   |
   v
Machine Learning Layer
   |
   |-- Feature Engineering
   |-- Random Forest Risk Classification
   |-- Stock-Level Predictions
   |-- Portfolio-Level ML Risk Signal
   |-- Model Confidence
   |-- Feature Importance
   |
   v
Interactive Output
   |
   |-- Market Overview
   |-- Portfolio Overview
   |-- ML Risk Model
   |-- Risk Contributors
   |-- Drawdown Analysis
   |-- Stress Testing
   |-- Data Downloads
```

## Main Components

## 1. User Input Layer

The app begins with user-defined portfolio inputs through the Streamlit sidebar.

Users can provide:

* Stock ticker symbols
* Portfolio weights
* Historical data period
* Refresh request for updated market data

Example default portfolio:

```text
AAPL, MSFT, NVDA, JPM, TSLA
```

The user can adjust each holding’s weight. If the total weight does not equal 100%, the application normalizes the weights for calculation purposes.

## 2. Data Collection Layer

The application uses the `yfinance` Python library to retrieve latest available historical market data.

The data collection layer retrieves:

* Portfolio holdings selected by the user
* SPY as the S&P 500 market benchmark proxy
* QQQ as the Nasdaq 100 / technology-heavy benchmark proxy
* VIX as the market volatility and fear proxy

Data fields used include:

* Date
* Open price
* High price
* Low price
* Close price
* Volume
* Ticker symbol

## 3. Data Processing Layer

After data is collected, the application prepares it for analytics.

Processing steps include:

* Resetting and standardizing date fields
* Cleaning ticker-level market data
* Converting dates into datetime format
* Removing missing close prices
* Sorting records by ticker and date
* Creating return and risk metrics
* Creating benchmark comparison features

This layer ensures that portfolio analytics and machine learning predictions are calculated from consistent and clean input data.

## 4. Feature Engineering Layer

The platform creates multiple risk-related features from raw market data.

Key engineered features include:

* Daily return
* 5-day return
* 20-day return
* 20-day annualized volatility
* 60-day annualized volatility
* 60-day maximum drawdown
* 20-day moving average gap
* 50-day moving average gap
* 20-day volume change
* SPY 20-day return
* SPY 20-day volatility
* QQQ 20-day return
* VIX level
* VIX 20-day change

These features are used both for risk analytics and for the machine learning model.

## 5. Portfolio Risk Analytics Layer

This layer calculates the core risk metrics shown in the application.

Portfolio-level metrics include:

* Portfolio return
* Portfolio volatility
* Estimated maximum drawdown
* Recent 20-day portfolio return
* Portfolio risk score
* Portfolio risk level

Stock-level metrics include:

* Latest price
* Total return
* Annualized volatility
* Maximum drawdown
* 20-day return
* 20-day volatility
* Trend status

The portfolio metrics are calculated using the user’s normalized portfolio weights.

## 6. Risk Scoring Layer

The application includes a rule-based portfolio risk score.

The score ranges from:

```text
0 to 100
```

The score is based on:

* Portfolio volatility
* Portfolio drawdown
* Recent 20-day trend
* Total portfolio return

The output risk levels are:

* Low Risk
* Medium Risk
* High Risk

This rule-based score gives users a quick summary of portfolio risk before viewing deeper details.

## 7. Benchmark and Market Signal Layer

The platform includes benchmark comparison to give portfolio results broader market context.

Benchmark indicators include:

* SPY return and volatility
* QQQ return and momentum
* VIX level and volatility condition

The app creates a market risk signal:

* Calm Market
* Cautious Market
* High-Risk Market

This helps users understand whether portfolio risk is being influenced by broader market conditions.

## 8. Machine Learning Layer

The project includes a baseline machine learning model built using a Random Forest classifier.

The model predicts:

* Low Risk
* Medium Risk
* High Risk

The model uses historical stock and benchmark features to classify current risk conditions.

Model outputs include:

* Stock-level ML risk prediction
* Portfolio-level ML risk prediction
* Model confidence
* Risk probability breakdown
* Top feature importances

The trained model is saved as:

```text
model/risk_model.pkl
```

Additional model files include:

```text
model/model_features.json
model/model_performance.csv
model/train_risk_model.py
```

## 9. Stress Testing Layer

The stress testing module allows users to simulate a downside market shock.

Users can test market drops from:

```text
1% to 40%
```

The app estimates:

* Scenario shock
* Estimated portfolio impact
* Value after shock
* Holding-level weighted impact

This feature helps users understand how portfolio value may react under simplified downside scenarios.

## 10. Visualization Layer

The interactive visualization layer is built with Streamlit and Plotly.

The application includes these tabs:

1. Market Overview
2. Portfolio Overview
3. ML Risk Model
4. Risk Contributors
5. Drawdown Analysis
6. Stress Testing
7. Data & Downloads

Visual outputs include:

* KPI cards
* Benchmark tables
* Indexed performance charts
* Portfolio vs benchmark comparison
* Risk contribution bar charts
* Drawdown line charts
* ML probability charts
* Feature importance charts
* Downloadable metrics tables

## 11. Output and Documentation Layer

The project is documented in GitHub using:

* README file
* Docs folder
* GitHub Wiki
* Screenshots
* Model documentation
* Risk methodology explanation
* Portfolio webpage summary

Key documentation files include:

```text
docs/project_summary.md
docs/business_problem.md
docs/solution_architecture.md
docs/data_sources.md
docs/risk_methodology.md
docs/model_documentation.md
docs/app_features.md
docs/limitations_future_work.md
```

## Repository Structure

```text
real-time-investor-risk-intelligence/
│
├── app/
│   └── streamlit_app.py
│
├── assets/
│   └── screenshots/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── project_summary.md
│   ├── business_problem.md
│   ├── solution_architecture.md
│   ├── data_sources.md
│   ├── risk_methodology.md
│   ├── model_documentation.md
│   ├── app_features.md
│   └── limitations_future_work.md
│
├── model/
│   ├── train_risk_model.py
│   ├── risk_model.pkl
│   ├── model_features.json
│   └── model_performance.csv
│
├── notebooks/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Data Flow Summary

The data flow can be summarized as:

```text
Market Data → Feature Engineering → Risk Metrics → ML Prediction → Streamlit App → User Insights
```

## Design Reasoning

This architecture was selected because it is:

* Beginner-friendly
* Easy to explain
* Suitable for GitHub portfolio presentation
* Interactive instead of static
* Expandable for future features
* Useful for investor-focused risk monitoring
* Strong enough to demonstrate Python, analytics, machine learning, and application development skills

## Future Architecture Enhancements

Future versions of the architecture may include:

* Streamlit Cloud deployment
* API key-based data sources
* FRED macroeconomic indicators
* SQLite database storage
* Portfolio optimization module
* Authentication for saved portfolios
* Automated scheduled data refresh
* More advanced model evaluation
* Explainable AI using SHAP
* Sector-level and asset-class-level risk analytics

## Important Disclaimer

This architecture supports an educational portfolio project. The application is not intended to provide financial advice, investment advice, or trading recommendations.
