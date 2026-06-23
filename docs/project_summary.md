# Project Summary

## Project Title

**Real-Time Investor Risk Intelligence Platform**

## Project Overview

The Real-Time Investor Risk Intelligence Platform is an interactive financial analytics solution designed to help investors monitor portfolio risk using the latest available market data, benchmark indicators, stress testing, and a baseline machine learning risk classification model.

Unlike a traditional dashboard that only displays stock prices and historical returns, this project focuses on converting market behavior into practical risk intelligence. The application allows users to enter stock tickers, assign portfolio weights, compare portfolio performance against market benchmarks, monitor volatility and drawdown risk, and view machine learning-based risk classifications.

The final solution is built as a Streamlit web application and structured as a professional portfolio project with source code, model files, screenshots, and documentation hosted on GitHub.

## Business Objective

The objective of this project is to provide a simple but practical risk monitoring tool that helps investors answer the following questions:

* Is my portfolio currently low risk, medium risk, or high risk?
* Which holdings are contributing the most to portfolio volatility?
* How does my portfolio compare against broader market benchmarks such as SPY and QQQ?
* Are current market conditions calm, cautious, or high risk?
* What could happen to the portfolio under a downside stress scenario?
* What does the machine learning model classify as the current portfolio risk level?

## Problem Being Solved

Investors often track stock prices, returns, and market news separately, but they may not have a simple tool that combines these signals into one portfolio risk view.

This project solves that problem by combining:

* Market data
* Portfolio weights
* Volatility analytics
* Drawdown analysis
* Benchmark comparison
* Stress testing
* Machine learning classification

The platform helps convert raw market movement into a more understandable risk signal.

## Solution Summary

The solution includes the following major components:

1. **Interactive Streamlit App**
   Users can input ticker symbols, adjust portfolio weights, refresh market data, and explore risk metrics interactively.

2. **Portfolio Risk Score**
   The app calculates a portfolio-level risk score using return, volatility, drawdown, and short-term trend behavior.

3. **Market Benchmark Indicators**
   The platform uses SPY, QQQ, and VIX-style volatility context to compare the selected portfolio against broader market conditions.

4. **Risk Contribution Analysis**
   The app identifies which holdings contribute the most weighted volatility risk.

5. **Drawdown Analysis**
   Historical drawdowns are calculated to show downside exposure for each selected security.

6. **Stress Testing**
   Users can simulate market shock scenarios and estimate possible portfolio impact.

7. **Machine Learning Risk Model**
   A baseline Random Forest classification model predicts Low Risk, Medium Risk, or High Risk using historical return, volatility, drawdown, moving average, volume, and benchmark features.

## Tools and Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* yfinance
* Plotly
* Scikit-learn
* Joblib
* GitHub
* VS Code

## Key Features

* Latest available market data retrieval
* Custom portfolio ticker input
* Portfolio weight adjustment
* Portfolio risk score
* Risk level classification
* SPY and QQQ benchmark comparison
* VIX-style market risk signal
* Historical drawdown charts
* Weighted volatility contribution chart
* Stress testing slider
* Downloadable risk metrics
* Baseline machine learning risk prediction
* Stock-level ML predictions
* Portfolio-level ML risk prediction
* Model confidence and feature importance view

## Project Deliverables

The project includes:

* Streamlit application code
* Machine learning training script
* Trained risk classification model
* Model feature documentation
* Model performance report
* Application screenshots
* GitHub README
* GitHub Wiki documentation
* Portfolio webpage project summary

## Current Version

The current project version includes:

* Version 1.0: Initial working Streamlit app
* Version 1.1: Professional UI upgrade
* Version 1.2: Market benchmark indicators
* Version 2.0: Baseline ML risk classification model
* Version 2.1: ML model connected to the Streamlit app

## Important Disclaimer

This project is created for educational and portfolio demonstration purposes only. It is not financial advice, investment advice, or a trading recommendation. The risk scores and machine learning predictions are simplified analytical outputs and should not be used as the sole basis for investment decisions.
