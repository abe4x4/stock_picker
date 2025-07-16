# config.py

# --- Stock Screening Criteria ---
# These values can be adjusted to customize the stock screening process.

# Minimum percentage increase in stock price for the current day.
# For example, 0.10 means a 10% increase.
MIN_PRICE_INCREASE_PERCENT = 0.10

# Minimum multiple of average daily trading volume for the current day's volume.
# For example, 5 means the current volume must be at least 5 times the average.
MIN_VOLUME_MULTIPLIER = 5

# Minimum stock price in USD.
MIN_STOCK_PRICE = 2.00

# Maximum stock price in USD.
MAX_STOCK_PRICE = 20.00

# Maximum float (number of shares available for trading) in millions.
# For example, 20 means 20 million shares.
MAX_FLOAT_MILLIONS = 20

# --- News Search Configuration ---
# These settings are for the news search functionality.

# Number of days back to search for news.
NEWS_SEARCH_DAYS_BACK = 1

# Keywords to look for in news headlines to indicate significant momentum.
# This is a basic approach; more advanced NLP would be needed for true sentiment analysis.
NEWS_KEYWORDS = ["earnings", "breakthrough", "acquisition", "partnership", "fda", "approval", "contract", "innovation", "growth", "expansion"]

# --- Performance Configuration ---
# Number of concurrent workers (threads) to use for screening stocks.
# Adjust based on your internet connection speed and API rate limits.
# A higher number means faster screening but increases the risk of being rate-limited.
MAX_WORKERS = 10 # For example, 10 concurrent requests

# --- API Keys (if applicable) ---
# If you were using a paid API for more robust news or financial data,
# you would store your API keys here. For this basic version, no API keys are needed.
# EXAMPLE:
# NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"
# FINANCIAL_DATA_API_KEY = "YOUR_FINANCIAL_DATA_API_KEY_HERE"