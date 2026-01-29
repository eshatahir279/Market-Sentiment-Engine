import yfinance as yf
from textblob import TextBlob
import datetime

class MarketIntel:
    def __init__(self, tickers):
        self.tickers = tickers
        self.report_data = []

    def get_sentiment(self, text):
        
        analysis = TextBlob(text)
        
        score = analysis.sentiment.polarity
        if score > 0.15: return "Bullish 🚀"
        if score < -0.15: return "Bearish 🔻"
        return "Neutral 😐"

    def run_analysis(self):
        print(f"--- Market Intelligence Report: {datetime.date.today()} ---")
        for symbol in self.tickers:
            try:
                stock = yf.Ticker(symbol)
                
                price = stock.history(period="1d")['Close'].iloc[-1]
                summary = stock.info.get('longBusinessSummary', "No summary available.")
                
                sentiment = self.get_sentiment(summary)
                
                result = f"[{symbol}] Price: ${price:.2f} | Outlook: {sentiment}"
                print(result)
                self.report_data.append(result)
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")

    def save_report(self):
        # We add encoding="utf-8" here to handle the emojis!
        with open("market_report.txt", "w", encoding="utf-8") as f:
            f.write(f"Report Generated: {datetime.datetime.now()}\n")
            f.writelines("\n".join(self.report_data))
        print("\n✅ Professional report saved to 'market_report.txt'")


if __name__ == "__main__":
    
    my_portfolio = ["NVDA", "AAPL", "TSLA", "GOOGL", "MSFT"]
    
    bot = MarketIntel(my_portfolio)
    bot.run_analysis()
    bot.save_report()