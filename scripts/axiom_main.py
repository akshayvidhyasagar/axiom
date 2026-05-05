import os
import sys
import json

# Add project root to path to allow importing from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.axiom_data_client import AxiomDataClient, AxiomPortfolio
from core.axiom_strategy import AxiomStrategy

def load_env(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

def main():
    load_env()
    print("1 & 2. Initializing Axiom Core Components...")
    client = AxiomDataClient.from_env()
    portfolio = AxiomPortfolio(initial_cash=100_000)
    
    universe = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META", 
        "GOOGL", "BRK-B", "JNJ", "JPM", "XOM", 
        "PG", "V", "UNH", "HD", "COST"
    ]
    strategy = AxiomStrategy(client, portfolio, universe)
    
    print("\n3. Detecting Macro Regime...")
    regime = strategy.detect_macro_regime()
    print(f"Current Regime: {regime.upper()}")
    
    print("\n4. Generating Fundamental & DCF Signals (Multi-threaded)...")
    signals = strategy.generate_signals()
    print(f"Generated signals for {len(signals)} tickers.")
    if not signals.empty:
        print(signals[['symbol', 'raw_score', 'signal']].head(3))
        
    print("\nFull Signal Table:")
    print(strategy.signals.to_string())
        
    print("\n5. Building Portfolio...")
    trades = strategy.build_portfolio(target_positions=5, position_size_pct=0.15)
    print(f"Executed {len(trades)} trades.")
    
    print("\n6. Generating Investment Report...")
    report_path = strategy.generate_report('axiom_report.html')
    print(f"Report saved to: {report_path}")
    
    print("\n7. Final Portfolio Status")
    current_prices = {sym: client.get_quote(sym).get('last_price', 0) for sym in portfolio.positions.keys()}
    print(f"Total Value: ${portfolio.get_portfolio_value(current_prices):,.2f}")
    print(portfolio.get_positions())

if __name__ == "__main__":
    main()
