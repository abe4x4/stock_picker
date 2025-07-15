# main.py
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# Import configuration settings from config.py
from config import (
    MIN_PRICE_INCREASE_PERCENT,
    MIN_VOLUME_MULTIPLIER,
    MIN_STOCK_PRICE,
    MAX_STOCK_PRICE,
    MAX_FLOAT_MILLIONS,
    NEWS_SEARCH_DAYS_BACK,
    NEWS_KEYWORDS
)

def get_stock_data(ticker_symbol):
    """
    Fetches historical and current stock data for a given ticker symbol using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL", "MSFT").

    Returns:
        tuple: A tuple containing:
            - ticker (yfinance.Ticker object): The yfinance Ticker object for the symbol.
            - history (pandas.DataFrame): Historical data for the last 2 days.
            - info (dict): Dictionary of various stock information.
            Returns (None, None, None) if data cannot be fetched.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Fetch history for the last 2 days to calculate daily change
        history = ticker.history(period="2d")
        info = ticker.info
        return ticker, history, info
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None, None, None

def check_price_increase(history):
    """
    Checks if the stock price increased by at least MIN_PRICE_INCREASE_PERCENT today.

    Args:
        history (pandas.DataFrame): Historical data for the last 2 days.

    Returns:
        bool: True if the price increased by the required percentage, False otherwise.
    """
    if history.empty or len(history) < 2:
        return False

    # Get closing price of yesterday and today
    yesterday_close = history['Close'].iloc[0]
    today_close = history['Close'].iloc[1]

    if yesterday_close == 0: # Avoid division by zero
        return False

    price_increase_percent = (today_close - yesterday_close) / yesterday_close
    return price_increase_percent >= MIN_PRICE_INCREASE_PERCENT

def check_volume_surge(history):
    """
    Checks if today's trading volume is at least MIN_VOLUME_MULTIPLIER times its average.

    Args:
        history (pandas.DataFrame): Historical data for the last 2 days.

    Returns:
        bool: True if the volume surged, False otherwise.
    """
    if history.empty or len(history) < 2:
        return False

    today_volume = history['Volume'].iloc[1]

    # Calculate average daily volume over a longer period (e.g., 30 days)
    # Fetching 30 days history for average volume calculation
    try:
        long_history = yf.Ticker(history.index.name).history(period="30d")
        if long_history.empty:
            return False
        average_volume = long_history['Volume'].mean()
    except Exception as e:
        print(f"Error fetching long history for volume check: {e}")
        return False

    if average_volume == 0: # Avoid division by zero
        return False

    return today_volume >= (average_volume * MIN_VOLUME_MULTIPLIER)

def check_price_range(info):
    """
    Checks if the current stock price is within the defined MIN_STOCK_PRICE and MAX_STOCK_PRICE range.

    Args:
        info (dict): Dictionary of various stock information.

    Returns:
        bool: True if the price is within range, False otherwise.
    """
    current_price = info.get('currentPrice')
    if current_price is None:
        return False
    return MIN_STOCK_PRICE <= current_price <= MAX_STOCK_PRICE

def check_float(info):
    """
    Checks if the stock's float (shares outstanding) is under MAX_FLOAT_MILLIONS.

    Args:
        info (dict): Dictionary of various stock information.

    Returns:
        bool: True if the float is within the limit, False otherwise.
    """
    # yfinance 'sharesOutstanding' is typically the total shares, not just float.
    # For a more precise float, a dedicated financial data API might be needed.
    # For this exercise, we'll use 'sharesOutstanding' as a proxy.
    shares_outstanding = info.get('sharesOutstanding')
    if shares_outstanding is None:
        return False

    # Convert shares outstanding to millions
    shares_outstanding_millions = shares_outstanding / 1_000_000
    return shares_outstanding_millions <= MAX_FLOAT_MILLIONS

def search_news(ticker_symbol):
    """
    Performs a basic web search for news related to the ticker symbol
    and checks if any NEWS_KEYWORDS are present in the headlines.
    This is a simplified approach and may not always find direct causal news.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        bool: True if relevant news is found, False otherwise.
        list: A list of relevant news headlines found.
    """
    search_query = f"{ticker_symbol} stock news"
    # Using Google News as a source for a basic search
    url = f"https://news.google.com/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"

    try:
        headers = {'User-Agent': 'Mozilla/5.0'} # Some sites block requests without a User-Agent
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        found_headlines = []
        # Google News uses 'h3' tags for headlines
        for article in soup.find_all('h3'):
            headline = article.get_text().lower()
            # Check if any keyword is in the headline
            if any(keyword in headline for keyword in NEWS_KEYWORDS):
                # Check if the news is recent (within NEWS_SEARCH_DAYS_BACK)
                # This part is tricky with basic scraping as dates might not be easily parsable
                # For simplicity, we'll assume top results are recent.
                # A more robust solution would parse the date from the article.
                found_headlines.append(article.get_text())
        return bool(found_headlines), found_headlines
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news for {ticker_symbol}: {e}")
        return False, []
    except Exception as e:
        print(f"An unexpected error occurred during news search for {ticker_symbol}: {e}")
        return False, []

def screen_stock(ticker_symbol):
    """
    Screens a single stock against all defined criteria.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        tuple: A tuple containing:
            - bool: True if the stock meets all criteria, False otherwise.
            - dict: A dictionary of the stock's data and screening results.
    """
    print(f"--- Screening {ticker_symbol} ---")
    ticker, history, info = get_stock_data(ticker_symbol)

    if ticker is None or history is None or history.empty or info is None:
        print(f"Could not retrieve complete data for {ticker_symbol}. Skipping.")
        return False, {}

    # Check each criterion
    price_increase_met = check_price_increase(history)
    print(f"Price increase (>= {MIN_PRICE_INCREASE_PERCENT*100:.0f}%): {price_increase_met}")

    volume_surge_met = check_volume_surge(history)
    print(f"Volume surge (>= {MIN_VOLUME_MULTIPLIER}x avg): {volume_surge_met}")

    price_range_met = check_price_range(info)
    current_price = info.get('currentPrice', 'N/A')
    print(f"Price in range (${MIN_STOCK_PRICE:.2f}-${MAX_STOCK_PRICE:.2f}): {price_range_met} (Current: ${current_price})")

    float_met = check_float(info)
    shares_outstanding_millions = info.get('sharesOutstanding', 0) / 1_000_000
    print(f"Float (<= {MAX_FLOAT_MILLIONS}M): {float_met} (Current: {shares_outstanding_millions:.2f}M)")

    news_found, relevant_headlines = search_news(ticker_symbol)
    print(f"Relevant news found: {news_found}")
    if relevant_headlines:
        print("  Relevant Headlines:")
        for headline in relevant_headlines:
            print(f"    - {headline}")

    # Aggregate results
    all_criteria_met = (
        price_increase_met and
        volume_surge_met and
        price_range_met and
        float_met and
        news_found
    )

    results = {
        "ticker": ticker_symbol,
        "price_increase_met": price_increase_met,
        "volume_surge_met": volume_surge_met,
        "price_range_met": price_range_met,
        "float_met": float_met,
        "news_found": news_found,
        "relevant_headlines": relevant_headlines,
        "current_price": current_price,
        "shares_outstanding_millions": shares_outstanding_millions
    }

    print(f"--- {ticker_symbol} meets all criteria: {all_criteria_met} ---")
    print() # Add an extra newline for formatting, similar to original intent
    return all_criteria_met, results

def main():
    """
    Main function to run the stock screener.
    It takes a list of ticker symbols to screen.
    """
    # Example list of ticker symbols to screen.
    # In a real application, this list could be loaded from a file,
    # an API, or user input.
    # For demonstration, let's use a few common tickers and some
    # that might fit the criteria for penny stocks or small caps.
    # NOTE: Finding stocks that meet ALL criteria, especially news,
    # with a simple web scrape can be challenging and might require
    # running the screener multiple times or on different days.
    ticker_list = [
        "AMC", "GME", "SNDL", "NOK", "BB", # Example meme stocks / low float
        "PLTR", "SOFI", "RIVN", # Other potentially volatile stocks
        "GOOGL", "MSFT", "AAPL", # Large cap for comparison (unlikely to meet criteria)
        "SPCE", "SENS", "SAVA", # More speculative examples
        "MVIS", "NIO", "TLRY", "WISH", "ZYNE" # Additional examples
    ]

    # You can also add a single ticker for testing:
    # ticker_list = ["AMC"]

    qualified_stocks = []

    print("Starting stock screening process...")
    print() # Add an extra newline for formatting, similar to original intent
    for ticker_symbol in ticker_list:
        meets_criteria, stock_data = screen_stock(ticker_symbol)
        if meets_criteria:
            qualified_stocks.append(stock_data)
        # Be respectful to APIs and websites, add a small delay between requests
        time.sleep(2)

    print()
    print("--- Screening Complete ---")
    if qualified_stocks:
        print() # Add an extra newline for formatting
        print("Qualified Stocks:")
        for stock in qualified_stocks:
            print(f"  Ticker: {stock['ticker']}")
            print(f"    Current Price: ${stock['current_price']:.2f}")
            print(f"    Shares Outstanding (M): {stock['shares_outstanding_millions']:.2f}")
            if stock['relevant_headlines']:
                print("    Relevant News Headlines:")
                for headline in stock['relevant_headlines']:
                    print(f"      - {headline}")
            print("-" * 30)
    else:
        print("No stocks met all the specified criteria today.")

if __name__ == "__main__":
    main()
