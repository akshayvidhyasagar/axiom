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
    client = AxiomDataClient.from_env()
    portfolio = AxiomPortfolio(100_000)

    universe = ['AAPL','MSFT','NVDA','AMZN','META','GOOGL',
                'BRK-B','JNJ','JPM','XOM','PG','V','UNH','HD','COST']

    strategy = AxiomStrategy(client, portfolio, universe)

    print("Running backtest 2020-01-01 to 2024-12-31 (quarterly rebalance)...")
    results = strategy.run_backtest(
        start='2020-01-01',
        end='2024-12-31',
        rebalance_frequency='quarterly'
    )

    # Print metrics (exclude large objects)
    metrics = {k: v for k, v in results.items() 
               if k not in ('portfolio_value_series', 'trades')}
    print("\nPerformance Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    print("\nPortfolio Value Series:")
    print(results['portfolio_value_series'])

    print(f"\nTotal Trades Executed: {len(results['trades'])}")
    print("\nSample Trades (first 10):")
    print(results['trades'].head(10).to_string())

if __name__ == "__main__":
    main()
