import os
import sys

# Add project root to path to allow importing from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.axiom_data_client import AxiomDataClient, AxiomPortfolio
from core.axiom_strategy import AxiomStrategy

# Set mock env vars for the demonstration if they don't exist
os.environ.setdefault("TIINGO_API_KEY", "3ed8ecf508d0118f2a541d65b0e0712fee9bb279")
os.environ.setdefault("POLYGON_API_KEY", "pCI556WtY6W3UcZjqfGXtvwoYNi54dMl")
os.environ.setdefault("FRED_API_KEY", "210d072100c8c8978c69c4aded11ce6d")

def main():
    # 1. client = AxiomDataClient.from_env()
    print("1. Initializing client...")
    client = AxiomDataClient.from_env()

    # 2. client.health_check()
    print("\n2. Running health check...")
    print(client.health_check())

    # 3. Screen symbols
    print("\n3. Screening stocks...")
    universe = ["AAPL", "MSFT", "NVDA", "BRK-B", "JNJ", "AMZN", "META", "GOOGL"]
    screen_results = client.screen_stocks(universe, filters={"min_roic": 0.15, "max_pe": 35})
    print(screen_results)

    if not screen_results.empty:
        top_ticker = screen_results.iloc[0]["symbol"]
        print(f"\nTop ranked ticker is {top_ticker}")
        
        # 4. Run DCF
        print("\n4. Running DCF...")
        print(client.run_dcf(top_ticker))
        
        # 5. Fetch transcript list then pull most recent transcript
        print("\n5. Fetching transcripts...")
        t_list = client.list_transcripts(top_ticker)
        if not t_list.empty:
            recent = t_list.iloc[0]
            transcript = client.get_transcript(top_ticker, recent["fiscal_year"], recent["fiscal_quarter"])
            print(f"Fetched {len(transcript)} paragraphs from latest transcript.")
            
        # 8. Quote and tech indicators
        print("\n8. Fetching quote and technicals...")
        quote = client.get_quote(top_ticker)
        print(f"Quote: {quote}")
        macd = client.get_technical_indicators(top_ticker, "macd")
        print(f"MACD latest:\n{macd.tail(1) if not macd.empty else 'N/A'}")
        
        # 9. Initialize Portfolio
        print("\n9. Initializing Portfolio...")
        portfolio = AxiomPortfolio(100_000)
        curr_price = quote.get("last_price") or 100.0
        if curr_price:
            portfolio.buy(top_ticker, 10, curr_price)
            print(f"Bought 10 shares of {top_ticker} at {curr_price}")
            
        # 10. Portfolio P&L and Weights
        print("\n10. Portfolio P&L and weights...")
        prices = {top_ticker: curr_price * 1.05} # simulate 5% gain
        print("P&L:\n", portfolio.get_pnl(prices))
        print("Weights:\n", portfolio.get_weights(prices))

    # 6. client.get_macro() 
    print("\n6. Fetching full macro dashboard...")
    macro_df = client.get_macro()
    print(macro_df.tail(1) if not macro_df.empty else "No macro data")

    # 7. client.get_yield_curve()
    print("\n7. Fetching yield curve...")
    yc_df = client.get_yield_curve()
    print(yc_df.tail(1) if not yc_df.empty else "No yield curve data")

if __name__ == "__main__":
    main()
