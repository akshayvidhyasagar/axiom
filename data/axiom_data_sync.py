import os
import pandas as pd
import yfinance as yf
import requests
import io
import time

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tables = pd.read_html(io.StringIO(response.text))
    df = tables[0]
    tickers = df['Symbol'].tolist()
    # Replace dots with hyphens for yfinance (e.g., BRK.B -> BRK-B)
    tickers = [ticker.replace('.', '-') for ticker in tickers]
    return tickers

def fetch_data():
    start_date = '2015-01-01'
    end_date = '2024-12-31'
    
    # Resolve paths relative to this script to ensure they are always correct
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'data', 'raw', 'ohlcv')
    failed_log = os.path.join(project_root, 'data', 'raw', 'failed_tickers.txt')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Fetching S&P 500 tickers from Wikipedia...")
    try:
        tickers = get_sp500_tickers()
    except Exception as e:
        print(f"Failed to fetch tickers from Wikipedia: {e}")
        return
        
    total = len(tickers)
    print(f"Found {total} tickers. Starting download...")
    
    failed_tickers = []
    
    # Use a shared session with a User-Agent to help avoid Yahoo Finance rate limits
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for i, ticker in enumerate(tickers):
        csv_path = os.path.join(output_dir, f"{ticker}.csv")
        
        # 6. Skip tickers that already have a CSV file
        if os.path.exists(csv_path):
            if (i + 1) % 25 == 0:
                print(f"Progress: {i + 1}/{total} (Skipped {ticker})")
            continue
            
        # 2. Use yfinance to download daily OHLCV data with retries
        success = False
        for attempt in range(3):
            try:
                df = yf.download(ticker, start=start_date, end=end_date, session=session, progress=False)
                if df is not None and not df.empty:
                    success = True
                    break
            except Exception:
                pass
            # Backoff for rate limits or transient errors
            time.sleep(2 * (2 ** attempt)) # wait 2s, 4s, 8s
            
        if not success or df is None or df.empty:
            failed_tickers.append(ticker)
            continue
            
        # Add a slight delay to respect rate limits globally
        time.sleep(0.5)
        
        try:
            # Flatten columns if multiindex (yfinance > 0.2.x behavior)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            df = df.reset_index()
            
            # Ensure column names are strings and lowercase
            df.columns = df.columns.astype(str).str.lower()
            
            # Format date as YYYY-MM-DD
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                
            # 3. Save each ticker as a CSV with columns: date, open, high, low, close, volume
            required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            
            # Check if we have all required columns
            available_cols = [c for c in required_cols if c in df.columns]
            if len(available_cols) < len(required_cols):
                failed_tickers.append(ticker)
                continue
                
            df = df[required_cols]
            
            df.to_csv(csv_path, index=False)
            
        except Exception:
            # 4. Handle delisted/missing tickers silently with try/except
            failed_tickers.append(ticker)
            
        # 5. Print progress every 25 tickers
        if (i + 1) % 25 == 0:
            print(f"Progress: {i + 1}/{total}")
            
    # Write failed tickers to log
    if failed_tickers:
        with open(failed_log, 'a') as f:
            for t in failed_tickers:
                f.write(t + '\n')
        print(f"Finished. {len(failed_tickers)} failed tickers logged to {failed_log}.")
    else:
        print("Finished successfully with no failed tickers.")

if __name__ == '__main__':
    fetch_data()
