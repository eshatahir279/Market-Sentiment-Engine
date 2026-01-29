import yfinance as yf

# Let's try a different ticker just in case
symbol = "AAPL" 

try:
    print(f"Searching for {symbol}...")
    ticker = yf.Ticker(symbol)
    
    # This is a more stable way to get the price
    todays_data = ticker.history(period='1d')
    
    if not todays_data.empty:
        price = todays_data['Close'].iloc[-1]
        print(f"Connection Successful!")
        print(f"The current price of {symbol} is: ${price:.2f}")
    else:
        print("Could not find data. Are you connected to the internet?")

except Exception as e:
    print(f"An error occurred: {e}")