import pandas as pd
import yfinance as yf
import os
import argparse
from datetime import date, timedelta
from typing import Union
import traceback
import sys


def get_ticker_info(ticker_symbol):
    """Fetches ticker information from yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    return ticker.info


def get_stock_history(ticker_symbol, start_date, end_date):
    """Fetches historical stock data from yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    # auto_adjust=False is required to get 'Stock Splits'
    return ticker.history(start=start_date, end=end_date, auto_adjust=False)


def get_start_date(output_csv, transactions_df, ticker_symbol):
    """
    Determines the start date for fetching data.
    If existing data is found, it returns the day after the last entry.
    Otherwise, it returns the earliest transaction date for the ticker.
    """
    if os.path.exists(output_csv):
        try:
            existing_df = pd.read_csv(output_csv, parse_dates=['Date'])
            if not existing_df.empty:
                last_date = existing_df['Date'].max().date()
                print(f"Existing data found for {ticker_symbol} up to {last_date}.")
                return last_date + timedelta(days=1)
        except (pd.errors.EmptyDataError, KeyError, FileNotFoundError):
            print(f"Warning: {output_csv} is empty or invalid. Will download from the beginning.")

    return transactions_df[transactions_df['symbol'] == ticker_symbol]['date'].min().date()


def update_stock_data(ticker_symbol, start_date, resources_path):
    """
    Fetches and saves stock data for a given ticker and start date.
    
    Args:
        ticker_symbol (str): The stock ticker symbol
        start_date (str or date): Start date for fetching data. Can be a string in 'YYYY-MM-DD' format or a date object
        resources_path (str): Path to the resources directory where CSV files will be saved. 
                             Relative paths will be resolved relative to the current working directory.
    """
    # Create resources directory if it doesn't exist
    if not os.path.exists(resources_path):
        os.makedirs(resources_path)
    
    output_csv = os.path.join(resources_path, f"{ticker_symbol}.csv")
    today = date.today()
    
    # Parse start_date if it's a string, otherwise use as-is (for backward compatibility)
    if isinstance(start_date, str):
        try:
            start_date = pd.to_datetime(start_date).date()
        except ValueError as e:
            print(f"Invalid date format for {ticker_symbol}. Expected 'YYYY-MM-DD' format. Error: {e}\n")
            return
    elif not isinstance(start_date, date):
        print(f"Invalid start_date type for {ticker_symbol}. Expected string or date object.\n")
        return

    if start_date >= today:
        print(f"Stock {ticker_symbol} is already up to date. Skipping.\n")
        return

    print(f"Fetching data for {ticker_symbol} from {start_date} to {today}...")

    try:
        history_df = get_stock_history(ticker_symbol, start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))



        if history_df.empty:
            print(f"No new data found for {ticker_symbol}.\n")
            return

        info = get_ticker_info(ticker_symbol)
        currency = info.get('currency', 'N/A')
        print(f"Currency for {ticker_symbol}: {currency}")

        history_df['Currency'] = currency
        # Ensure Dividends column exists and fill missing with 0
        if 'Dividends' not in history_df.columns:
            history_df['Dividends'] = 0.0
        else:
            history_df['Dividends'] = history_df['Dividends'].fillna(0.0)
        output_df = history_df[['Close', 'Dividends', 'Stock Splits', 'Currency']]

        should_write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0
        write_df_to_csv(output_df, output_csv, mode='a', header=should_write_header, date_format='%Y-%m-%d')

        print(f"Successfully updated {ticker_symbol}.csv\n")

    except Exception as e:
        print(f"Could not download data for {ticker_symbol}. Error: {e}\n")
        traceback.print_exc()


def write_df_to_csv(df, *args, **kwargs):
    return df.to_csv(*args, **kwargs)


def download_stock_history(resources_path: str):
    """
    Downloads and updates daily stock price history for tickers in transactions.csv.
    
    Args:
        resources_path: Path to the resources directory.
    """
    transactions_file = os.path.join(resources_path, 'transactions.csv')

    if not os.path.exists(resources_path):
        os.makedirs(resources_path)

    try:
        transactions_df = pd.read_csv(transactions_file, parse_dates=['date'])
    except FileNotFoundError:
        print(f"Error: The file {transactions_file} was not found.")
        return

    unique_tickers = transactions_df['symbol'].unique()
    
    # Ensure EURUSD=X is always included for currency conversion
    if 'EURUSD=X' not in unique_tickers:
        unique_tickers = list(unique_tickers) + ['EURUSD=X']
        print("Added EURUSD=X to download list for currency conversion.")
    
    print(f"Found {len(unique_tickers)} unique tickers. Processing...\n")

    for ticker_symbol in unique_tickers:
        print(f"-- Processing {ticker_symbol} --")
        output_csv = os.path.join(resources_path, f"{ticker_symbol}.csv")
        
        # For EURUSD=X, use a default start date if not in transactions
        if ticker_symbol == 'EURUSD=X' and ticker_symbol not in transactions_df['symbol'].values:
            # Use a reasonable default start date (e.g., 2 years ago)
            default_start_date = date.today() - timedelta(days=730)
            start_date = get_start_date(output_csv, transactions_df, ticker_symbol) if os.path.exists(output_csv) else default_start_date
        else:
            start_date = get_start_date(output_csv, transactions_df, ticker_symbol)
        
        update_stock_data(ticker_symbol, start_date, resources_path)


def main():
    """CLI entry point for the stock history downloader."""
    parser = argparse.ArgumentParser(description="Download historical stock data for portfolio tickers")
    parser.add_argument(
        "--resources-path", 
        type=str, 
        required=True,
        help="Path to the resources directory containing transactions.csv"
    )
    
    args = parser.parse_args()
    download_stock_history(args.resources_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())