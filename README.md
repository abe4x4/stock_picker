# Stock Screener Application

## Overview
This Python application is a stock screener designed to identify potential trading opportunities based on specific technical and fundamental criteria. It fetches real-time and historical stock data using the `yfinance` library and performs a basic web search for news using `requests` and `BeautifulSoup` to determine if there's a news catalyst for the stock's momentum.

The application is built with extensibility in mind, allowing users to easily customize the screening criteria through a dedicated configuration file (`config.py`).

## Features
- **Customizable Screening Criteria**: Easily adjust parameters such as minimum price increase, volume surge multiplier, price range, and maximum float.
- **Real-time Data Fetching**: Utilizes `yfinance` to get up-to-date stock prices, volumes, and company information.
- **Volume Surge Detection**: Identifies stocks experiencing significantly higher trading volume compared to their average.
- **Price Momentum Analysis**: Screens for stocks that have shown a significant price increase on the current day.
- **Price Range Filtering**: Filters stocks based on a specified price range, useful for focusing on penny stocks or specific market segments.
- **Float-based Filtering**: Helps identify stocks with a low number of outstanding shares, which can be more volatile and prone to large price swings.
- **Basic News Catalyst Search**: Performs a web search for news related to the screened stocks and checks for predefined keywords to identify potential news-driven momentum. (Note: This is a simplified approach; advanced NLP would be required for true sentiment analysis and precise news correlation).
- **Extensively Commented Code**: The codebase is thoroughly commented to aid beginners in understanding the logic and flow of the application.

## Getting Started

### Prerequisites
- Python 3.8+ installed on your system.
- Internet connection to fetch stock data and news.

### Installation
1.  **Clone the repository (or download the files):**
    ```bash
    git clone <YOUR_GITHUB_REPO_URL_HERE>
    cd stock_screener_app
    ```
    *(Note: You will replace `<YOUR_GITHUB_REPO_URL_HERE>` with the actual URL after the repository is created and pushed.)*

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
All customizable screening criteria are located in `config.py`. Open this file and modify the values to suit your preferences:

- `MIN_PRICE_INCREASE_PERCENT`: Minimum daily price increase (e.g., `0.10` for 10%).
- `MIN_VOLUME_MULTIPLIER`: Minimum multiple of average daily volume (e.g., `5` for 5x average).
- `MIN_STOCK_PRICE`: Minimum stock price.
- `MAX_STOCK_PRICE`: Maximum stock price.
- `MAX_FLOAT_MILLIONS`: Maximum float in millions of shares.
- `NEWS_SEARCH_DAYS_BACK`: How many days back to consider news as relevant (currently not fully implemented in basic news search).
- `NEWS_KEYWORDS`: A list of keywords to look for in news headlines.
- `MAX_WORKERS`: Number of concurrent threads to use for fetching stock data and news. A higher number will speed up the screening but increases the risk of hitting API rate limits. Adjust this value based on your internet connection and the generosity of the data providers (Yahoo Finance, Google News).
- `RATE_LIMIT_DELAY`: Minimum delay (in seconds) between consecutive requests to external APIs. This helps prevent hitting rate limits. Adjust this value if you continue to experience "Too Many Requests" errors.

## Usage

To run the stock screener, simply execute the `main.py` script from your activated virtual environment:

```bash
python main.py
```

The script will now automatically fetch a comprehensive list of US stock ticker symbols from NASDAQ's FTP server and iterate through them concurrently, applying the defined screening criteria. It will print detailed results for each stock, indicating whether it met each criterion. Finally, it will list all stocks that met all the specified criteria.

**Reporting:** After each run, a text file will be generated in a subfolder named `results/`. The filename will include the search date and time (e.g., `stock_screener_report_YYYYMMDD_HHMMSS.txt`). This file will contain:
- The total number of stocks checked.
- The total time taken for the screening.
- A list of all stocks that matched the search criteria, including their Name, Symbol, Price, Volume, and Percentage of Increase.

**Note on Performance and Rate Limiting:** By utilizing concurrent processing and a rate-limiting mechanism, the screening time has been significantly reduced while aiming to prevent "Too Many Requests" errors. However, screening a large number of stocks (potentially thousands) still takes time. If you continue to encounter rate limiting, consider increasing `RATE_LIMIT_DELAY` or decreasing `MAX_WORKERS` in `config.py`.

## Future Enhancements / To-Do List

- **More Robust News Analysis**: Implement more sophisticated news scraping and natural language processing (NLP) to better correlate news with stock momentum and sentiment analysis.
- **Integration with Financial News APIs**: Utilize dedicated financial news APIs (e.g., NewsAPI, Alpha Vantage) for more reliable and structured news data, rather than basic web scraping.
- **User Input for Tickers**: Allow users to input a list of tickers or load them from a file instead of hardcoding them in `main.py`.
- **Database Integration**: Store screening results in a database (e.g., SQLite) for historical tracking and analysis.
- **Graphical User Interface (GUI)**: Develop a simple GUI using libraries like Tkinter, PyQt, or Streamlit for a more user-friendly experience.
- **Backtesting Capability**: Add functionality to backtest screening strategies against historical data.
- **Alerts/Notifications**: Implement email or push notification alerts for when stocks meet the criteria.
- **Error Handling and Logging**: Improve error handling and add comprehensive logging for better debugging and monitoring.
- **Concurrency/Parallelism**: Optimize screening for a large number of tickers by processing them concurrently.
- **More Advanced Technical Indicators**: Incorporate additional technical indicators (e.g., RSI, MACD, Bollinger Bands) into the screening criteria.
- **Fundamental Data Integration**: Include more fundamental analysis data points (e.g., P/E ratio, EPS, revenue growth) from financial APIs.
