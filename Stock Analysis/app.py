import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Performance Dashboard")

st.title("📈 Stock Performance & Risk Analysis Dashboard")

# User Input
ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

period = st.selectbox(
    "Select Time Period",
    ["6mo", "1y", "2y", "5y"]
)

# Download Data
data = yf.download(
    ticker,
    period=period
)

if len(data) > 0:

    st.subheader("Stock Price Data")
    st.dataframe(data.tail())

    # Closing Price Chart
    st.subheader("Closing Price Trend")

    fig, ax = plt.subplots()

    ax.plot(
        data.index,
        data["Close"]
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    st.pyplot(fig)

    # Returns
    data["Returns"] = (
        data["Close"]
        .pct_change()
    )

    annual_return = (
        data["Returns"].mean()
        * 252
        * 100
    )

    volatility = (
        data["Returns"].std()
        * np.sqrt(252)
        * 100
    )

    # Moving Averages
    data["MA20"] = (
        data["Close"]
        .rolling(20)
        .mean()
    )

    data["MA50"] = (
        data["Close"]
        .rolling(50)
        .mean()
    )

    st.subheader("Key Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Annual Return (%)",
        round(float(annual_return),2)
    )

    col2.metric(
        "Volatility (%)",
        round(float(volatility),2)
    )

    # Moving Average Chart

    st.subheader("Moving Average Analysis")

    fig2, ax2 = plt.subplots()

    ax2.plot(
        data.index,
        data["Close"],
        label="Close Price"
    )

    ax2.plot(
        data.index,
        data["MA20"],
        label="20 Day MA"
    )

    ax2.plot(
        data.index,
        data["MA50"],
        label="50 Day MA"
    )

    ax2.legend()

    st.pyplot(fig2)

    # Company Information

    stock = yf.Ticker(ticker)

    info = stock.info

    st.subheader("Company Information")

    st.write(
        "Sector:",
        info.get("sector","N/A")
    )

    st.write(
        "Market Cap:",
        info.get("marketCap","N/A")
    )

    st.write(
        "P/E Ratio:",
        info.get("trailingPE","N/A")
    )

    