import os
import sys

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
    strategy.detect_macro_regime()
    strategy.generate_signals()

    # Rebuild portfolio state to match previous run
    # Using a try/except or default values in case get_quote fails due to mocks
    try:
        nvda_quote = client.get_quote('NVDA')
        nvda_price = nvda_quote.get('last_price', 198.45)
        v_quote = client.get_quote('V')
        v_price = v_quote.get('last_price', 328.03)
    except:
        nvda_price = 198.45
        v_price = 328.03

    portfolio.buy('NVDA', 75, nvda_price)
    portfolio.buy('V', 45, v_price)

    path = strategy.generate_report('axiom_report.html')
    print(f"Report saved to: {path}")

if __name__ == "__main__":
    main()
