import yfinance as yf
from textblob import TextBlob

stocks = ["NVDA", "AAPL", "TSLA", "MSFT"]

def analyze_sentiment(text):
    
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1: return "🌟 POSITIVE"
    if score < -0.1: return "⚠️ NEGATIVE"
    return "😐 NEUTRAL"

print(f"{'Ticker':<10} | {'Price':<10} | {'Market Sentiment'}")
print("-" * 45)

for symbol in stocks:
    ticker = yf.Ticker(symbol)
    
    # Get current price
    price = ticker.history(period='1d')['Close'].iloc[-1]
    
    # Get the company's recent business summary (our data for sentiment)
    summary = ticker.info.get('longBusinessSummary', 'No data')
    sentiment = analyze_sentiment(summary)
    
    print(f"{symbol:<10} | ${price:<9.2f} | {sentiment}")