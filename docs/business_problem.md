# Business Problem

## Background

Investors, financial analysts, and portfolio managers often monitor multiple sources of information before making portfolio decisions. These sources may include stock prices, market indexes, volatility indicators, earnings news, economic signals, analyst commentary, and portfolio allocation reports.

However, many investors do not have a single simple tool that combines these signals into a practical portfolio risk view.

Most beginner-level dashboards show information such as:

* Stock price trends
* Daily returns
* Volume movement
* Historical performance
* Basic comparison charts

While these are useful, they do not directly answer the most important investor risk questions.

## Core Business Problem

The main problem this project addresses is:

**Investors need a simple, interactive, and data-driven way to monitor portfolio risk using current market data, benchmark comparison, volatility signals, drawdown analysis, and machine learning-based risk classification.**

Without a structured risk monitoring tool, investors may struggle to understand:

* Whether their portfolio is currently low risk, medium risk, or high risk
* Which holdings are contributing the most risk
* How their portfolio compares with broader market benchmarks
* Whether the market environment is calm, cautious, or high risk
* How much downside impact a market shock could create
* Whether short-term risk signals are increasing

## Why This Problem Matters

Financial markets can change quickly. A portfolio that looks stable based on long-term historical returns may still carry short-term risk due to volatility, concentration, market weakness, or benchmark deterioration.

Investors may face several challenges:

1. **Fragmented Information**
   Market data, portfolio holdings, volatility indicators, and benchmark signals are often reviewed separately.

2. **Limited Risk Visibility**
   A price chart can show movement, but it does not clearly explain downside risk, drawdown exposure, or volatility contribution.

3. **Benchmark Blind Spots**
   A portfolio may appear to perform well in isolation, but it may be underperforming or taking more risk compared with SPY or QQQ.

4. **Concentration Risk**
   Investors may unknowingly hold a portfolio where one or two securities contribute most of the volatility.

5. **Lack of Scenario Testing**
   Many investors do not test what could happen if the market drops by 5%, 10%, 20%, or more.

6. **No Simple Risk Classification**
   Investors may see multiple charts and numbers but still not have a clear risk label such as Low Risk, Medium Risk, or High Risk.

## Target Users

This project is designed for:

* Individual investors
* Beginner investors learning portfolio risk
* Financial analyst portfolio projects
* Data analyst portfolio reviewers
* Business stakeholders who need simplified risk insights
* Hiring managers evaluating applied analytics and machine learning skills

## Business Questions

The project is designed to answer the following business questions:

1. What is the current risk level of the selected portfolio?
2. What is the portfolio risk score based on return, volatility, drawdown, and trend behavior?
3. Which stock contributes the most weighted volatility risk?
4. How does the portfolio compare against SPY and QQQ?
5. What does the VIX-style signal suggest about broader market conditions?
6. Which holdings have experienced the largest drawdowns?
7. What is the estimated portfolio impact under a downside stress scenario?
8. What does the baseline machine learning model classify as the current risk level?
9. How confident is the model in the risk classification?
10. Which features are most important to the model prediction?

## Business Impact

A risk intelligence platform like this can help users:

* Monitor portfolio risk more clearly
* Identify high-risk holdings
* Understand downside exposure
* Compare portfolio performance with market benchmarks
* View market risk signals in one place
* Perform basic stress testing
* Interpret machine learning-based risk classification
* Make more informed educational analysis decisions

## Proposed Solution

The proposed solution is an interactive Streamlit application that combines market data, portfolio analytics, benchmark indicators, stress testing, and machine learning classification.

The app allows users to:

* Enter custom stock tickers
* Assign portfolio weights
* Pull latest available market data
* Calculate return, volatility, and drawdown metrics
* Compare portfolio performance against SPY and QQQ
* Monitor VIX-style market risk conditions
* Identify weighted volatility contributors
* Run downside stress-test scenarios
* View machine learning-based risk predictions
* Download portfolio risk metrics

## Solution Value

This project provides value because it transforms raw financial data into a clear risk-monitoring experience.

Instead of only showing what happened in the market, the solution helps explain:

* What the risk level is
* Why the risk level may be elevated
* Which holdings are driving risk
* How the portfolio compares with the market
* What could happen under downside scenarios
* What the machine learning model predicts

## Scope of the Project

This project focuses on educational portfolio risk intelligence. It does not attempt to predict exact stock prices or provide buy/sell recommendations.

The scope includes:

* Latest available historical market data
* Portfolio-level risk analytics
* Stock-level risk metrics
* Benchmark comparison
* VIX-style risk context
* Simple stress testing
* Baseline machine learning classification
* Professional GitHub documentation

## Out of Scope

The following items are not included in the current version:

* Real-time institutional-grade market feeds
* Broker account integration
* Automated trading
* Buy/sell recommendations
* Options pricing
* Tax optimization
* Full portfolio optimization
* Personalized financial advice

## Important Disclaimer

This project is for educational and portfolio demonstration purposes only. It is not financial advice, investment advice, or a trading recommendation. The outputs should be interpreted as analytical risk indicators, not as instructions to buy, sell, or hold any security.
