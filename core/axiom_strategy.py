import math
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pandas as pd

from .axiom_data_client import AxiomDataClient, AxiomPortfolio

# Module-level helpers and constants
sigmoid = lambda x: 1 / (1 + math.exp(-x))
SECTOR_DEFENSIVES = frozenset(['Utilities', 'Consumer Defensive', 'Healthcare'])
SECTOR_CYCLICALS = frozenset(['Technology', 'Consumer Cyclical', 'Basic Materials'])

class AxiomStrategy:
    def __init__(self, client: AxiomDataClient, portfolio: AxiomPortfolio, universe: list[str]):
        """Initializes the strategy with a data client, portfolio simulator, and universe."""
        self.client = client
        self.portfolio = portfolio
        self.universe = universe
        self.signals = pd.DataFrame()
        self.macro_regime = 'risk_on'
        self.logger = logging.getLogger("AxiomStrategy")

    def detect_macro_regime(self) -> str:
        """Classifies current macro environment using FRED data into one of four regimes."""
        try:
            macro_df = self.client.get_macro(['real_gdp', 'cpi', 'fed_funds_rate', 'hy_credit_spread', 'treasury_10y', 'yield_spread_10y2y'])
            if macro_df.empty:
                self.macro_regime = 'risk_on'
                return self.macro_regime

            latest = macro_df.iloc[-1]
            gdp_series = macro_df['real_gdp'].dropna()
            
            if len(gdp_series) >= 2:
                gdp_growth = (gdp_series.iloc[-1] - gdp_series.iloc[-2]) / gdp_series.iloc[-2] * 100
            else:
                gdp_growth = 0.0

            cpi = latest.get('cpi', 0)
            hy_spread = latest.get('hy_credit_spread', 0)
            yield_spread = latest.get('yield_spread_10y2y', 0)

            if gdp_growth > 0 and cpi < 3.0 and hy_spread < 4.0:
                self.macro_regime = 'goldilocks'
            elif gdp_growth > 0 and hy_spread < 5.0:
                self.macro_regime = 'risk_on'
            elif cpi > 4.0 and gdp_growth < 1.0:
                self.macro_regime = 'stagflation'
            elif hy_spread > 5.0 or yield_spread < 0:
                self.macro_regime = 'risk_off'
            else:
                self.macro_regime = 'risk_on'
                
            return self.macro_regime
        except Exception as e:
            self.logger.warning(f"Macro regime detection failed, defaulting to risk_on: {str(e)}")
            self.macro_regime = 'risk_on'
            return self.macro_regime

    def generate_signals(self, at_date: str = None) -> pd.DataFrame:
        """Generates BUY / HOLD / SELL signals for all tickers in universe using fundamentals + DCF + macro regime."""
        results = []

        def process_ticker(sym):
            print(f" > Analyzing {sym}...")
            try:
                funds = self.client.get_fundamentals(sym, at_date=at_date)
                dcf = self.client.run_dcf(sym, at_date=at_date)
                info = self.client.get_ticker_info(sym)

                if not funds or not dcf:
                    return None

                roic = funds.get('roic') or 0
                fcf_margin = funds.get('fcf_margin') or 0
                rev_growth = funds.get('revenue_growth_yoy') or 0
                upside_pct = dcf.get('upside_pct') or 0
                sector = info.get('sector', 'Unknown')

                roic_score = min(roic / 0.15, 2.0) / 2.0
                fcf_score = min(fcf_margin / 0.15, 2.0) / 2.0
                growth_score = min(rev_growth / 0.10, 2.0) / 2.0
                valuation_score = sigmoid(upside_pct / 20.0)

                macro_adj = 1.0
                if self.macro_regime == 'goldilocks':
                    pass
                elif self.macro_regime == 'risk_on':
                    if sector in SECTOR_DEFENSIVES: macro_adj = 0.8
                elif self.macro_regime == 'risk_off':
                    if sector in SECTOR_CYCLICALS: macro_adj = 0.4
                    elif sector in SECTOR_DEFENSIVES: macro_adj = 0.9
                elif self.macro_regime == 'stagflation':
                    if rev_growth > 0.15: macro_adj = 0.5

                raw_score = (
                    0.25 * roic_score +
                    0.20 * fcf_score +
                    0.20 * growth_score +
                    0.20 * valuation_score +
                    0.15 * macro_adj
                )

                if raw_score >= 0.65: signal = 'BUY'
                elif raw_score >= 0.40: signal = 'HOLD'
                else: signal = 'SELL'

                self.logger.debug(f"[{sym}] ROIC:{roic_score:.2f} FCF:{fcf_score:.2f} Growth:{growth_score:.2f} Val:{valuation_score:.2f} Macro:{macro_adj:.2f} -> Score:{raw_score:.3f} ({signal})")
                
                # Print to console for immediate visibility during backtest
                if raw_score >= 0.60:  # Show near-misses and hits
                    print(f"   ! {sym}: {raw_score:.3f} ({signal}) | Upside: {upside_pct:.1f}%")

                return {
                    'symbol': sym,
                    'roic': roic,
                    'fcf_margin': fcf_margin,
                    'revenue_growth_yoy': rev_growth,
                    'upside_pct': upside_pct,
                    'raw_score': raw_score,
                    'signal': signal,
                    'sector': sector,
                    'macro_regime': self.macro_regime
                }
            except Exception as e:
                self.logger.warning(f"Signal generation failed for {sym}: {str(e)}")
                return None

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_ticker, s): s for s in self.universe}
            completed = 0
            for future in as_completed(futures):
                res = future.result()
                completed += 1
                if res:
                    results.append(res)
                print(f"[{completed}/{len(self.universe)}] Processed {futures[future]}")

        if results:
            self.signals = pd.DataFrame(results).sort_values('raw_score', ascending=False)
        else:
            self.signals = pd.DataFrame(columns=[
                'symbol', 'roic', 'fcf_margin', 'revenue_growth_yoy', 'upside_pct', 
                'raw_score', 'signal', 'sector', 'macro_regime'
            ])

        return self.signals

    def build_portfolio(self, target_positions: int = 5, position_size_pct: float = 0.15) -> pd.DataFrame:
        """Constructs a portfolio from BUY signals using equal-weight or conviction-weighted sizing."""
        if self.signals.empty:
            return pd.DataFrame()

        # Removed .head(target_positions) to allow threshold-based selection
        buy_signals = self.signals[self.signals['signal'] == 'BUY']
        
        current_prices = {}
        for sym in buy_signals['symbol']:
            q = self.client.get_quote(sym)
            if q and q.get('last_price'):
                current_prices[sym] = q['last_price']

        port_val = self.portfolio.get_portfolio_value(current_prices)
        trades = []

        for _, row in buy_signals.iterrows():
            sym = row['symbol']
            price = current_prices.get(sym)
            if not price: 
                continue

            target_alloc = port_val * position_size_pct
            shares = math.floor(target_alloc / price)

            if shares > 0 and self.portfolio.cash >= shares * price:
                self.portfolio.buy(sym, shares, price)
                trades.append({
                    'symbol': sym,
                    'signal': row['signal'],
                    'raw_score': row['raw_score'],
                    'shares_bought': shares,
                    'price': price,
                    'allocation_value': shares * price,
                    'weight_pct': (shares * price) / port_val if port_val > 0 else 0
                })

        return pd.DataFrame(trades)

    def rebalance(self, target_positions: int = 5, position_size_pct: float = 0.15, at_date: str = None) -> pd.DataFrame:
        """Rebalances existing portfolio to align with latest signals."""
        self.generate_signals(at_date=at_date)

        current_prices = {}
        for sym in self.universe:
            q = self.client.get_quote(sym)
            if q and q.get('last_price'):
                current_prices[sym] = q['last_price']

        positions = self.portfolio.get_positions()
        actions = []

        # Sell logic
        if not positions.empty:
            for _, row in positions.iterrows():
                sym = row['symbol']
                sig_row = self.signals[self.signals['symbol'] == sym]
                signal = sig_row.iloc[0]['signal'] if not sig_row.empty else 'SELL'

                if signal == 'SELL':
                    shares = row['shares']
                    price = current_prices.get(sym)
                    if price:
                        self.portfolio.sell(sym, shares, price)
                        actions.append({
                            'symbol': sym, 'action': 'SELL', 'shares': shares, 
                            'price': price, 'reason': 'Signal changed to SELL'
                        })

        # Buy logic
        buy_signals = self.signals[self.signals['signal'] == 'BUY']
        held_syms = self.portfolio.get_positions()['symbol'].tolist() if not self.portfolio.get_positions().empty else []
        new_buys = buy_signals[~buy_signals['symbol'].isin(held_syms)]
        
        # Removed slots_available cap to allow threshold-based selection
        buys_to_make = new_buys
        port_val = self.portfolio.get_portfolio_value(current_prices)

        for _, row in buys_to_make.iterrows():
            sym = row['symbol']
            price = current_prices.get(sym)
            if not price: 
                continue

            target_alloc = port_val * position_size_pct
            shares = math.floor(target_alloc / price)

            if shares > 0 and self.portfolio.cash >= shares * price:
                self.portfolio.buy(sym, shares, price)
                actions.append({
                    'symbol': sym, 'action': 'BUY', 'shares': shares, 
                    'price': price, 'reason': 'New BUY signal'
                })

        return pd.DataFrame(actions)

    def run_backtest(self, start: str, end: str, rebalance_frequency: str = 'quarterly') -> dict:
        """Runs a historical backtest of the strategy over a date range."""
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        freq_map = {'monthly': 'ME', 'quarterly': 'QE', 'annually': 'YE'}
        freq = freq_map.get(rebalance_frequency, 'QE')
        dates = pd.date_range(start=start_date, end=end_date, freq=freq)

        port_values = []
        initial_cash = self.portfolio.initial_cash

        benchmark_df = self.client.get_macro(['sp500'])
        if not benchmark_df.empty:
            start_bench = benchmark_df[benchmark_df.index >= start_date]['sp500'].head(1)
            end_bench = benchmark_df[benchmark_df.index <= end_date]['sp500'].tail(1)
            b_start = start_bench.iloc[0] if not start_bench.empty else 1
            b_end = end_bench.iloc[0] if not end_bench.empty else 1
            benchmark_return_pct = (b_end - b_start) / b_start * 100
        else:
            benchmark_return_pct = 0.0

        # Fetch full history for all symbols once to avoid repeated API calls
        full_histories = {}
        for sym in self.universe:
            full_histories[sym] = self.client.get_price_history_local(sym, start, end)

        for dt in dates:
            current_prices = {}
            for sym in self.universe:
                hist = full_histories.get(sym, pd.DataFrame())
                # Slices history to the current backtest date
                period_prices = hist[hist.index <= dt]
                if not period_prices.empty:
                    current_prices[sym] = period_prices.iloc[-1]['close']

            print(f"   [{dt.strftime('%Y-%m-%d')}] Price coverage: {len(current_prices)}/{len(self.universe)} tickers")

            # Mock get_quote to use historical prices temporarily
            original_get_quote = self.client.get_quote
            self.client.get_quote = lambda s: {'last_price': current_prices.get(s)}

            self.detect_macro_regime()
            self.rebalance(at_date=dt.strftime('%Y-%m-%d'))

            if not self.signals.empty:
                buys = len(self.signals[self.signals['signal'] == 'BUY'])
                print(f"   [{dt.strftime('%Y-%m-%d')}] Signals: {buys} BUY, {len(self.signals)-buys} OTHER")

            self.client.get_quote = original_get_quote
            port_values.append(self.portfolio.get_portfolio_value(current_prices))

        pv_series = pd.Series(port_values, index=dates)
        final_value = port_values[-1] if port_values else initial_cash
        total_return_pct = (final_value - initial_cash) / initial_cash * 100
        
        years = (end_date - start_date).days / 365.25
        annualized_return_pct = ((final_value / initial_cash) ** (1/years) - 1) * 100 if years > 0 else 0

        roll_max = pv_series.cummax()
        drawdown = (pv_series - roll_max) / roll_max
        max_drawdown_pct = drawdown.min() * 100 if not drawdown.empty else 0

        returns = pv_series.pct_change().dropna()
        mean_ret = returns.mean()
        std_ret = returns.std()
        periods_per_year = 12 if rebalance_frequency == 'monthly' else 4 if rebalance_frequency == 'quarterly' else 1
        sharpe_ratio = (mean_ret / std_ret * math.sqrt(periods_per_year)) if std_ret > 0 else 0

        win_rate_pct = (returns > 0).mean() * 100 if not returns.empty else 0
        alpha_pct = total_return_pct - benchmark_return_pct

        return {
            'total_return_pct': total_return_pct,
            'annualized_return_pct': annualized_return_pct,
            'max_drawdown_pct': max_drawdown_pct,
            'sharpe_ratio': sharpe_ratio,
            'win_rate_pct': win_rate_pct,
            'benchmark_return_pct': benchmark_return_pct,
            'alpha_pct': alpha_pct,
            'portfolio_value_series': pv_series,
            'trades': self.portfolio.get_transaction_log()
        }

    def generate_report(self, output_path: str = 'axiom_report.html') -> str:
        """Generates a self-contained HTML investment report."""
        
        # 1. Macro Dashboard
        macro_df = self.client.get_macro()
        macro_html = macro_df.tail(1).T.to_html(classes="table table-bordered") if not macro_df.empty else "N/A"

        # 2. Yield Curve
        yc_df = self.client.get_yield_curve()
        yc_ascii = "N/A"
        if not yc_df.empty:
            latest_yc = yc_df.iloc[-1]
            spread = latest_yc.get('DGS10', 0) - latest_yc.get('DGS2', 0)
            shape = "Normal" if spread > 0 else "Inverted" if spread < 0 else "Flat"
            yc_ascii = f"<pre>Shape: {shape} (10Y-2Y Spread: {spread:.2f}%)\n"
            for t in ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1', 'DGS2', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS20', 'DGS30']:
                val = latest_yc.get(t, 0)
                bars = "=" * int(val * 5)
                yc_ascii += f"{t:6} | {bars} {val:.2f}%\n"
            yc_ascii += "</pre>"

        # 3. Signal Table
        def highlight_sig(s):
            color = '#d4edda' if s.signal == 'BUY' else '#fff3cd' if s.signal == 'HOLD' else '#f8d7da'
            return [f'background-color: {color}'] * len(s)

        if not self.signals.empty:
            sig_html = self.signals.style.apply(highlight_sig, axis=1).to_html()
        else:
            sig_html = "No signals generated."

        # 4. Portfolio Positions
        current_prices = {}
        def fetch_quote(s):
            return s, self.client.get_quote(s)
            
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_sym = {executor.submit(fetch_quote, sym): sym for sym in self.universe}
            for future in as_completed(future_to_sym):
                sym, q = future.result()
                if q and q.get('last_price'): 
                    current_prices[sym] = q['last_price']
            
        pnl_df = self.portfolio.get_pnl(current_prices)
        port_val = self.portfolio.get_portfolio_value(current_prices)
        pos_html = pnl_df.to_html(classes="table") if not pnl_df.empty else "No current positions."

        # 5. DCF Summary
        dcf_summary = []
        buys = self.signals[self.signals['signal'] == 'BUY'] if not self.signals.empty else pd.DataFrame()
        for sym in buys['symbol']:
            dcf = self.client.run_dcf(sym)
            if dcf:
                dcf_summary.append({
                    'symbol': sym,
                    'fair_price': dcf.get('fair_price'),
                    'current_price': dcf.get('current_price'),
                    'upside_pct': dcf.get('upside_pct'),
                    'wacc': dcf.get('wacc'),
                    'terminal_growth_rate': dcf.get('terminal_growth_rate')
                })
        dcf_html = pd.DataFrame(dcf_summary).to_html(classes="table") if dcf_summary else "N/A"

        # 6. Deep Dive
        top_ticker_html = "No BUY signals available."
        if not buys.empty:
            top_ticker = buys.iloc[0]['symbol']
            
            # Transcript
            try:
                transcripts_list = self.client.list_transcripts(top_ticker)
                if not transcripts_list.empty:
                    latest = transcripts_list.sort_values('report_date', ascending=False).iloc[0]
                    transcript_df = self.client.get_transcript(
                        top_ticker,
                        int(latest['fiscal_year']),
                        int(latest['fiscal_quarter'])
                    )
                    transcript_rows = transcript_df.head(10)
                    transcript_html = ''.join([
                        f'<p><strong>{row["speaker"]}:</strong> {row["content"][:500]}...</p>'
                        for _, row in transcript_rows.iterrows()
                    ])
                else:
                    transcript_html = '<p>No transcripts available.</p>'
            except Exception as e:
                self.logger.warning(f"Transcript fetch failed for {top_ticker}: {e}")
                transcript_html = '<p>Transcript unavailable.</p>'

            # Income Statement
            try:
                statements = self.client.get_financial_statements(top_ticker, frequency='quarterly')
                income_df = statements['income']
                # Keep only the 4 most recent quarters and the most meaningful rows
                income_subset = income_df.iloc[:, :4] if income_df.shape[1] >= 4 else income_df
                # Convert to HTML table with inline styling
                income_html = income_subset.to_html(
                    classes='income-table',
                    border=0,
                    justify='left'
                )
            except Exception as e:
                self.logger.warning(f"Income statement fetch failed for {top_ticker}: {e}")
                income_html = '<p>Income statement unavailable.</p>'

            # MACD Chart
            svg = "N/A"
            try:
                macd = self.client.get_technical_indicators(top_ticker, "macd")
                if not macd.empty and 'value' in macd.columns:
                    vals = macd['value'].tail(30).tolist()
                    if vals:
                        min_v, max_v = min(vals), max(vals)
                        range_v = max_v - min_v if max_v != min_v else 1
                        points = []
                        w, h = 300, 100
                        for i, v in enumerate(vals):
                            x = (i / max(1, len(vals)-1)) * w
                            y = h - ((v - min_v) / range_v) * h
                            points.append(f"{x},{y}")
                        svg = f'<svg width="{w}" height="{h}" style="border:1px solid #ddd; background:#f9f9f9;"><polyline points="{" ".join(points)}" fill="none" stroke="#007bff" stroke-width="2" /></svg>'
            except: pass
            
            top_ticker_html = f"<h3>{top_ticker}</h3><h4>MACD Sparkline (30d)</h4>{svg}<h4>Earnings Call</h4>{transcript_html}<h3>Quarterly Income Statement (Last 4 Quarters)</h3>{income_html}"

        # Final HTML Assembly
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Axiom Strategy Report</title>
            <style>
                body {{ font-family: -apple-system, system-ui, sans-serif; margin: 40px; color: #333; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; font-size: 14px; }}
                th, td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
                pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .income-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    font-size: 12px; 
                    margin-top: 16px;
                }}
                .income-table th {{ 
                    background: #1a1a2e; 
                    color: #ffffff; 
                    padding: 6px 10px; 
                    text-align: left; 
                }}
                .income-table td {{ 
                    padding: 5px 10px; 
                    border-bottom: 1px solid #e0e0e0; 
                }}
                .income-table tr:nth-child(even) {{ 
                    background: #f9f9f9; 
                }}
            </style>
        </head>
        <body>
            <h1>Axiom Investment Report</h1>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p><strong>Macro Regime:</strong> {self.macro_regime.upper()}</p>
            <p><strong>Portfolio Value:</strong> ${port_val:,.2f}</p>
            
            <h2>1. Macro Dashboard</h2>
            {macro_html}
            
            <h2>2. Yield Curve</h2>
            {yc_ascii}
            
            <h2>3. Signal Table</h2>
            {sig_html}
            
            <h2>4. Portfolio Positions</h2>
            {pos_html}
            
            <h2>5. DCF Summary (BUYs)</h2>
            {dcf_html}
            
            <h2>6. Top Ticker Deep Dive</h2>
            {top_ticker_html}
        </body>
        </html>
        """

        with open(output_path, 'w') as f:
            f.write(html)

        return output_path
