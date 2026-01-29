import streamlit as st
import yfinance as yf
from textblob import TextBlob
import pandas as pd
import datetime

st.set_page_config(page_title="AI Market Intel", page_icon="📈", layout="wide")

st.title("🚀 AI Market Intelligence Dashboard")
st.markdown("Analyzing market sentiment using Natural Language Processing.")

st.sidebar.header("Settings")
tickers = st.sidebar.text_input("Enter Tickers (comma separated)", "NVDA, AAPL, TSLA, BTC-USD")
ticker_list = [t.strip() for t in tickers.split(",")]

def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0.1: return "Positive 🚀"
    if score < -0.1: return "Negative 🔻"
    return "Neutral 😐"

def color_sentiment(val):
    if 'Positive' in val: color = '#28a745' # Success Green
    elif 'Negative' in val: color = '#dc3545' # Danger Red
    else: color = '#6c757d' # Secondary Gray
    return f'color: {color}; font-weight: bold'

if st.button("Run Intelligence Report"):
    results = []
    
    for symbol in ticker_list:
        with st.spinner(f"Analyzing {symbol}..."):
            try:
                stock = yf.Ticker(symbol)
                history = stock.history(period="1d")
                if not history.empty:
                    price = history['Close'].iloc[-1]
                    summary = stock.info.get('longBusinessSummary', "No data available.")
                    sentiment = get_sentiment(summary)
                    results.append({"Ticker": symbol, "Price": f"${price:,.2f}", "Sentiment": sentiment})
            except Exception as e:
                st.error(f"Error loading {symbol}: {e}")

    if results:
        df = pd.DataFrame(results)
        
        # Section 1: Top Level Metrics (Full Width)
        st.subheader("📌 Quick Stats")
        m_col1, m_col2, m_col3 = st.columns(3)
        current_hour = datetime.datetime.now().hour
        status = "Open 🟢" if 9 <= current_hour <= 16 else "Closed 🔴"
        m_col1.metric("Market Status (EST)", status)
        m_col2.metric("Assets Analyzed", len(results))
        m_col3.metric("Primary Asset", ticker_list[0])
        
        st.divider()

        # Section 2: Data Table (Full Width for better balance)
        st.subheader("📋 Market Analysis")
        st.dataframe(df.style.applymap(color_sentiment, subset=['Sentiment']), use_container_width=True)

        st.divider()

        # Section 3: Visual Chart
        st.subheader(f"📊 {ticker_list[0]} 7-Day Performance")
        chart_data = yf.Ticker(ticker_list[0]).history(period="7d")
        st.line_chart(chart_data['Close'])
            
        st.success("Analysis Complete!")