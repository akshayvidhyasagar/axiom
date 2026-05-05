import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date

import requests
import pandas as pd

# Fallback for Ticker if defeatbeta_api is not installed during planning
try:
    from defeatbeta_api.data.ticker import Ticker
except ImportError:
    Ticker = None

FRED_SERIES_MAP = {
    "real_gdp": "GDPC1",
    "cpi": "CPIAUCSL",
    "fed_funds_rate": "FEDFUNDS",
    "treasury_10y": "DGS10",
    "treasury_2y": "DGS2",
    "yield_spread_10y2y": "T10Y2Y",
    "unemployment": "UNRATE",
    "industrial_prod": "INDPRO",
    "m2_money_supply": "M2SL",
    "vix": "VIXCLS",
    "sp500": "SP500",
    "hy_credit_spread": "BAMLH0A0HYM2",
    "usd_eur": "DEXUSEU"
}

class AxiomDataClient:
    def __init__(self, tiingo_api_key: str, polygon_api_key: str, fred_api_key: str):
        self.tiingo_api_key = tiingo_api_key
        self.polygon_api_key = polygon_api_key
        self.fred_api_key = fred_api_key

        self.tiingo_session = requests.Session()
        self.tiingo_session.headers.update({"Authorization": f"Token {tiingo_api_key}"})
        
        self.polygon_session = requests.Session()
        self.polygon_session.params = {"apiKey": polygon_api_key}
        
        self.fred_session = requests.Session()
        self.fred_session.params = {"api_key": fred_api_key, "file_type": "json"}
        
        self.session = requests.Session() # Shared session for direct requests
        self.timeout = 10 # Default timeout in seconds
        
        self._ticker_cache: dict[str, Ticker] = {}
        self.logger = logging.getLogger("AxiomDataClient")

    def _safe_get(self, session: requests.Session, url: str, **kwargs) -> requests.Response:
        """Wrapper for session.get with default timeout."""
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        return session.get(url, **kwargs)

    def get_price_history_local(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """Returns adjusted daily close prices from defeatbeta local DuckDB cache."""
        try:
            t = self._get_ticker(symbol)
            price_df = t.price()
            
            if price_df is None or price_df.empty:
                return pd.DataFrame()
                
            # defeatbeta returns 'report_date' column. Set as index.
            if 'report_date' in price_df.columns:
                price_df['report_date'] = pd.to_datetime(price_df['report_date'])
                # Ensure naive Datetime to match backtest loop (avoid tz-naive vs tz-aware errors)
                if price_df['report_date'].dt.tz is not None:
                    price_df['report_date'] = price_df['report_date'].dt.tz_localize(None)
                price_df = price_df.set_index('report_date')
            elif not isinstance(price_df.index, pd.DatetimeIndex):
                price_df.index = pd.to_datetime(price_df.index)
                if hasattr(price_df.index, 'tz') and price_df.index.tz is not None:
                    price_df.index = price_df.index.tz_localize(None)
            
            # Sort to ensure slice works correctly
            price_df = price_df.sort_index()
            
            # Filter to date range
            # Convert start/end to datetime objects for robust comparison
            s_dt = pd.to_datetime(start)
            e_dt = pd.to_datetime(end)
            price_df = price_df[(price_df.index >= s_dt) & (price_df.index <= e_dt)]
            return price_df
        except Exception as e:
            self.logger.error(f"Local price history failed for {symbol}: {e}")
            return pd.DataFrame()
        
        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s %(name)s — %(message)s",
            level=logging.INFO
        )
        self.logger = logging.getLogger("AxiomDataClient")

    @classmethod
    def from_env(cls) -> "AxiomDataClient":
        tiingo_key = os.environ.get("TIINGO_API_KEY")
        if not tiingo_key:
            raise EnvironmentError("Missing TIINGO_API_KEY environment variable")
            
        polygon_key = os.environ.get("POLYGON_API_KEY")
        if not polygon_key:
            raise EnvironmentError("Missing POLYGON_API_KEY environment variable")
            
        fred_key = os.environ.get("FRED_API_KEY")
        if not fred_key:
            raise EnvironmentError("Missing FRED_API_KEY environment variable")
            
        return cls(tiingo_key, polygon_key, fred_key)

    def _get_ticker(self, symbol: str) -> Ticker:
        if symbol not in self._ticker_cache:
            if Ticker is None:
                raise ImportError("defeatbeta_api is not installed. Please pip install defeatbeta-api.")
            self._ticker_cache[symbol] = Ticker(symbol)
        return self._ticker_cache[symbol]

    def _tiingo_get(self, endpoint: str, params: dict = None) -> any:
        import time
        time.sleep(0.3)
        params = params or {}
        url = f"https://api.tiingo.com{endpoint}"
        try:
            response = self._safe_get(self.tiingo_session, url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Tiingo API Error on {endpoint}: {str(e)}")
            return None

    def _polygon_get(self, endpoint: str, params: dict = None) -> any:
        params = params or {}
        url = f"https://api.polygon.io{endpoint}"
        for attempt in range(2):
            try:
                response = self._safe_get(self.polygon_session, url, params=params)
                if response.status_code == 429:
                    self.logger.warning(f"Polygon 429 Rate Limit on {endpoint}. Retrying in 12s...")
                    time.sleep(12)
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                self.logger.error(f"Polygon API Error on {endpoint}: {str(e)}")
                return None
        return None

    def _fred_get(self, series_id: str, start: str = "2000-01-01", end: str = None) -> pd.DataFrame:
        if end is None:
            end = datetime.today().strftime('%Y-%m-%d')
            
        params = {
            "series_id": series_id,
            "observation_start": start,
            "observation_end": end
        }
        url = "https://api.stlouisfed.org/fred/series/observations"
        for attempt in range(3):
            try:
                response = self._safe_get(self.fred_session, url, params=params)
                response.raise_for_status()
                data = response.json()
                if "observations" not in data:
                    return pd.DataFrame()
                    
                df = pd.DataFrame(data["observations"])
                df = df[df["value"] != "."]
                df["date"] = pd.to_datetime(df["date"])
                df["value"] = df["value"].astype(float)
                df = df.set_index("date")
                return df[["value"]]
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                self.logger.error(f"FRED API Error on {series_id} (Attempt {attempt+1}): {str(e)}")
                return pd.DataFrame()
        return pd.DataFrame()

    def get_price_history(self, symbol: str, start: str, end: str, frequency: str = "daily") -> pd.DataFrame:
        """Returns adjusted OHLCV history. Source: Tiingo primary, Polygon fallback."""
        params = {
            "startDate": start,
            "endDate": end,
            "resampleFreq": frequency
        }
        data = self._tiingo_get(f"/tiingo/daily/{symbol}/prices", params=params)
        
        if data:
            df = pd.DataFrame(data)
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")
                cols = [c for c in ["open", "high", "low", "close", "adjClose", "volume"] if c in df.columns]
                return df[cols]
                
        self.logger.warning(f"Falling back to Polygon for {symbol} price history")
        
        timespan = "day" if frequency == "daily" else frequency.replace("ly", "")
        poly_data = self._polygon_get(f"/v2/aggs/ticker/{symbol}/range/1/{timespan}/{start}/{end}")
        
        if poly_data and "results" in poly_data:
            df = pd.DataFrame(poly_data["results"])
            if not df.empty:
                df["date"] = pd.to_datetime(df["t"], unit="ms")
                df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "vw": "adjClose"})
                df = df.set_index("date")
                cols = [c for c in ["open", "high", "low", "close", "adjClose", "volume"] if c in df.columns]
                return df[cols]
                
        return pd.DataFrame()

    def get_fundamentals(self, symbol: str, at_date: str = None) -> dict:
        """Returns flat fundamental metrics dict. Source: defeatbeta-api."""
        def extract_latest(df):
            if df is None or (hasattr(df, 'empty') and df.empty): return None
            try:
                if isinstance(df, pd.DataFrame):
                    # Filter for report_date <= at_date if provided
                    if at_date and 'report_date' in df.columns:
                        target_dt = pd.to_datetime(at_date)
                        # Ensure report_date is datetime and naive
                        df = df.copy()
                        df['report_date'] = pd.to_datetime(df['report_date'])
                        if df['report_date'].dt.tz is not None:
                            df['report_date'] = df['report_date'].dt.tz_localize(None)
                        df = df[df['report_date'] <= target_dt]
                        if df.empty: return None
                    
                    if 'report_date' in df.columns:
                        df = df.sort_values('report_date')
                    
                    # Drop metadata columns to ensure we pick the actual metric value
                    cols_to_drop = [c for c in ['symbol', 'report_date', 'eps_report_date', 'shares_report_date', 'price_report_date', 'fiscal_quarter'] if c in df.columns]
                    metric_df = df.drop(columns=cols_to_drop)
                    
                    if metric_df.empty: return None
                    
                    last_row = metric_df.iloc[-1].dropna()
                    if last_row.empty: return None
                    
                    return float(last_row.iloc[-1])
                elif isinstance(df, pd.Series):
                    return float(df.dropna().iloc[-1])
            except Exception:
                pass
            return None
            
        try:
            ticker = self._get_ticker(symbol)
            return {
                "ttm_eps": extract_latest(ticker.ttm_eps()),
                "ttm_pe": extract_latest(ticker.ttm_pe()),
                "pb_ratio": extract_latest(ticker.pb_ratio()),
                "ps_ratio": extract_latest(ticker.ps_ratio()),
                "peg_ratio": extract_latest(ticker.peg_ratio()),
                "roe": extract_latest(ticker.roe()),
                "roic": extract_latest(ticker.roic()),
                "roa": extract_latest(ticker.roa()),
                "wacc": extract_latest(ticker.wacc()),
                "gross_margin": extract_latest(ticker.annual_gross_margin()),
                "operating_margin": extract_latest(ticker.annual_operating_margin()),
                "net_margin": extract_latest(ticker.annual_net_margin()),
                "fcf_margin": extract_latest(ticker.annual_fcf_margin()),
                "revenue_growth_yoy": extract_latest(ticker.annual_revenue_yoy_growth()),
                "eps_growth_yoy": extract_latest(ticker.quarterly_eps_yoy_growth()),
                "market_cap": extract_latest(ticker.market_capitalization())
            }
        except Exception as e:
            self.logger.error(f"defeatbeta-api fundamentals error for {symbol}: {str(e)}")
            return {}

    def get_financial_statements(self, symbol: str, frequency: str = "quarterly") -> dict[str, pd.DataFrame]:
        """Returns income, balance_sheet, cash_flow as DataFrames. Source: defeatbeta-api."""
        try:
            ticker = self._get_ticker(symbol)
            if frequency == "quarterly":
                return {
                    "income": ticker.quarterly_income_statement().df(),
                    "balance_sheet": ticker.quarterly_balance_sheet().df(),
                    "cash_flow": ticker.quarterly_cash_flow().df()
                }
            else:
                return {
                    "income": ticker.annual_income_statement().df(),
                    "balance_sheet": ticker.annual_balance_sheet().df(),
                    "cash_flow": ticker.annual_cash_flow().df()
                }
        except Exception as e:
            self.logger.error(f"defeatbeta-api statements error for {symbol}: {str(e)}")
            return {}

    def get_transcript(self, symbol: str, fiscal_year: int, fiscal_quarter: int) -> pd.DataFrame:
        """Returns earnings call transcript. Source: defeatbeta-api."""
        try:
            ticker = self._get_ticker(symbol)
            return ticker.earning_call_transcripts().get_transcript(fiscal_year, fiscal_quarter)
        except Exception as e:
            self.logger.error(f"defeatbeta-api transcript error for {symbol}: {str(e)}")
            return pd.DataFrame()

    def list_transcripts(self, symbol: str) -> pd.DataFrame:
        """Returns all available transcript periods. Source: defeatbeta-api."""
        try:
            ticker = self._get_ticker(symbol)
            return ticker.earning_call_transcripts().get_transcripts_list()
        except Exception as e:
            self.logger.error(f"defeatbeta-api list_transcripts error for {symbol}: {str(e)}")
            return pd.DataFrame()

    def run_dcf(self, symbol: str, output_path: str = None, at_date: str = None) -> dict:
        """Runs automated DCF valuation. Source: defeatbeta-api."""
        try:
            ticker = self._get_ticker(symbol)
            
            # --- PIT Logic: Mock ticker data methods to respect at_date ---
            if at_date:
                target_dt = pd.to_datetime(at_date)
                
                def filter_df(df):
                    if not isinstance(df, pd.DataFrame): return df
                    if 'report_date' not in df.columns: return df
                    df_copy = df.copy()
                    df_copy['report_date'] = pd.to_datetime(df_copy['report_date'])
                    if df_copy['report_date'].dt.tz is not None:
                        df_copy['report_date'] = df_copy['report_date'].dt.tz_localize(None)
                    return df_copy[df_copy['report_date'] <= target_dt]

                # Data methods to wrap
                data_methods = [
                    'wacc', 'annual_revenue_yoy_growth', 'quarterly_ttm_eps_yoy_growth',
                    'ttm_fcf', 'ttm_revenue', 'annual_fcf_margin', 'price', 
                    'market_capitalization'
                ]
                
                originals = {}
                for m_name in data_methods:
                    orig = getattr(ticker, m_name)
                    originals[m_name] = orig
                    # Use default argument to capture current 'orig'
                    setattr(ticker, m_name, lambda o=orig: filter_df(o()))

                # Wrap treasure yield
                orig_ty = ticker.treasure.daily_treasure_yield
                ticker.treasure.daily_treasure_yield = lambda: filter_df(orig_ty())

                # Wrap balance sheet
                orig_qbs = ticker.quarterly_balance_sheet
                def pit_qbs():
                    stmt = orig_qbs()
                    orig_df_method = stmt.df
                    def pit_df():
                        df = orig_df_method()
                        date_cols = [c for c in df.columns if c != 'Breakdown']
                        valid_cols = ['Breakdown'] + [c for c in date_cols if pd.to_datetime(c) <= target_dt]
                        return df[valid_cols]
                    stmt.df = pit_df
                    return stmt
                ticker.quarterly_balance_sheet = pit_qbs
                
                try:
                    data = ticker.dcf_data()
                finally:
                    # Restore original methods
                    for m_name, orig in originals.items():
                        setattr(ticker, m_name, orig)
                    ticker.treasure.daily_treasure_yield = orig_ty
                    ticker.quarterly_balance_sheet = orig_qbs
            else:
                data = ticker.dcf_data()
            # --- End PIT Logic ---

            if not data:
                return {}
            
            dr = data.get("discount_rate", {})
            dt = data.get("dcf_template", {})
            dv = data.get("dcf_value", {})
            
            fair_price = dv.get("fair_price")
            current_price = dv.get("current_price")
            
            # If at_date is provided, use historical price for upside calculation
            if at_date and fair_price:
                # Fetch price history up to at_date to find the closest valid price
                hist = self.get_price_history_local(symbol, "2000-01-01", at_date)
                if not hist.empty:
                    current_price = hist.iloc[-1]['close']

            upside_pct = None
            if fair_price and current_price and current_price > 0:
                upside_pct = round((fair_price - current_price) / current_price * 100, 2)

            return {
                "fair_price": fair_price,
                "current_price": current_price,
                "upside_pct": upside_pct,
                "recommendation": dv.get("recommendation"),
                "wacc": dr.get("wacc"),
                "terminal_growth_rate": dt.get("growth_rate_terminal")
            }
        except Exception as e:
            self.logger.error(f"defeatbeta-api DCF error for {symbol}: {str(e)}")
            return {}

    def get_quote(self, symbol: str) -> dict:
        """Returns latest market quote. Source: Tiingo IEX (Real-time)."""
        # Tiingo IEX is usually free and provides real-time-ish quotes with prevClose
        url = f"https://api.tiingo.com/iex/{symbol}"
        params = {"token": self.tiingo_api_key}
        for attempt in range(3):
            try:
                response = self._safe_get(self.session, url, params=params)
                if response.status_code == 429:
                    time.sleep(1 * (attempt + 1))
                    continue
                response.raise_for_status()
                data = response.json()
                if data and len(data) > 0:
                    quote = data[0]
                    prev_close = quote.get("prevClose")
                    last_price = quote.get("last") or quote.get("tngoLast") or prev_close
                    
                    change_pct = None
                    if last_price and prev_close:
                        change_pct = round(((last_price - prev_close) / prev_close) * 100, 2)
                        
                    return {
                        "symbol": symbol,
                        "last_price": last_price,
                        "bid": quote.get("bidPrice"),
                        "ask": quote.get("askPrice"),
                        "volume": quote.get("volume"),
                        "change_pct": change_pct,
                        "timestamp": quote.get("timestamp")
                    }
            except Exception as e:
                self.logger.error(f"Tiingo Quote Error for {symbol} (Attempt {attempt+1}): {str(e)}")
                time.sleep(0.5)
                
        return {}

    def get_options_chain(self, symbol: str) -> pd.DataFrame:
        """Returns full options chain. Source: Polygon."""
        data = self._polygon_get(f"/v3/snapshot/options/{symbol}")
        if data and "results" in data:
            records = []
            for opt in data["results"]:
                details = opt.get("details", {})
                quote = opt.get("last_quote", {})
                greeks = opt.get("greeks", {})
                records.append({
                    "strike": details.get("strike_price"),
                    "expiry": details.get("expiration_date"),
                    "call_put": details.get("contract_type"),
                    "bid": quote.get("bid"),
                    "ask": quote.get("ask"),
                    "implied_volatility": opt.get("implied_volatility"),
                    "delta": greeks.get("delta"),
                    "gamma": greeks.get("gamma"),
                    "open_interest": opt.get("open_interest")
                })
            return pd.DataFrame(records)
        return pd.DataFrame()

    def get_news(self, symbols: list[str], days_back: int = 7) -> pd.DataFrame:
        """Returns recent news articles for given tickers. Source: Tiingo."""
        start_date = (datetime.now() - pd.Timedelta(days=days_back)).strftime('%Y-%m-%d')
        params = {
            "tickers": ",".join(symbols),
            "startDate": start_date,
            "limit": 100
        }
        data = self._tiingo_get("/tiingo/news", params=params)
        if data:
            df = pd.DataFrame(data)
            if not df.empty:
                df["date"] = pd.to_datetime(df["publishedDate"])
                return df[["date", "title", "description", "url", "source", "tickers"]].sort_values("date", ascending=False)
        return pd.DataFrame()

    def get_ticker_info(self, symbol: str) -> dict:
        """Returns reference data for a ticker. Source: defeatbeta-api."""
        try:
            ticker = self._get_ticker(symbol)
            info_df = ticker.info()
            if not info_df.empty:
                res = info_df.iloc[-1]
                return {
                    "name": res.get("shortName") or res.get("longName"),
                    "sector": res.get("sector"),
                    "industry": res.get("industry"),
                    "shares_outstanding": res.get("sharesOutstanding"),
                    "description": res.get("longBusinessSummary")
                }
        except Exception as e:
            self.logger.error(f"defeatbeta-api info error for {symbol}: {str(e)}")
            
        return {}

    def get_macro(self, series_keys: list[str] = None) -> pd.DataFrame:
        """Returns macro dashboard as wide DataFrame. Source: FRED."""
        keys_to_fetch = series_keys if series_keys is not None else list(FRED_SERIES_MAP.keys())
        dfs = []
        for key in keys_to_fetch:
            if key in FRED_SERIES_MAP:
                df = self._fred_get(FRED_SERIES_MAP[key])
                if not df.empty:
                    df = df.rename(columns={"value": key})
                    dfs.append(df)
                    
        if not dfs:
            return pd.DataFrame()
            
        combined = pd.concat(dfs, axis=1)
        return combined.ffill()

    def get_yield_curve(self) -> pd.DataFrame:
        """Returns historical yield curve term structure. Source: FRED DGS series."""
        tenors = ["DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]
        dfs = []
        for t in tenors:
            df = self._fred_get(t)
            if not df.empty:
                df = df.rename(columns={"value": t})
                dfs.append(df)
                
        if not dfs:
            return pd.DataFrame()
            
        return pd.concat(dfs, axis=1).ffill()

    def screen_stocks(self, symbols: list[str], filters: dict = {}) -> pd.DataFrame:
        """Screens universe by fundamental quality. Source: defeatbeta-api."""
        results = []
        
        def fetch_fundamentals(sym):
            try:
                metrics = self.get_fundamentals(sym)
                metrics["symbol"] = sym
                return metrics
            except Exception:
                self.logger.warning(f"Screening failed for {sym}")
                return None

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_fundamentals, s) for s in symbols]
            for future in as_completed(futures):
                res = future.result()
                if res and res.get("ttm_pe") is not None:
                    results.append(res)
                    
        if not results:
            return pd.DataFrame()
            
        df = pd.DataFrame(results)
        
        if "min_roic" in filters and "roic" in df.columns:
            df = df[df["roic"] >= filters["min_roic"]]
        if "max_pe" in filters and "ttm_pe" in df.columns:
            df = df[df["ttm_pe"] <= filters["max_pe"]]
        if "min_revenue_growth" in filters and "revenue_growth_yoy" in df.columns:
            df = df[df["revenue_growth_yoy"] >= filters["min_revenue_growth"]]
        if "max_pb" in filters and "pb_ratio" in df.columns:
            df = df[df["pb_ratio"] <= filters["max_pb"]]
        if "min_fcf_margin" in filters and "fcf_margin" in df.columns:
            df = df[df["fcf_margin"] >= filters["min_fcf_margin"]]
        if "min_roe" in filters and "roe" in df.columns:
            df = df[df["roe"] >= filters["min_roe"]]
            
        if df.empty:
            return df
            
        def normalize(series: pd.Series) -> pd.Series:
            s_min, s_max = series.min(), series.max()
            if s_min == s_max:
                return pd.Series(0.5, index=series.index)
            return (series - s_min) / (s_max - s_min)
            
        score = pd.Series(0.0, index=df.index)
        
        if "roic" in df.columns:
            score += 0.30 * normalize(df["roic"].fillna(0))
        if "roe" in df.columns:
            score += 0.20 * normalize(df["roe"].fillna(0))
        if "fcf_margin" in df.columns:
            score += 0.20 * normalize(df["fcf_margin"].fillna(0))
        if "revenue_growth_yoy" in df.columns:
            score += 0.15 * normalize(df["revenue_growth_yoy"].fillna(0))
        if "ttm_pe" in df.columns:
            inv_pe = 1.0 / df["ttm_pe"].replace(0, float('nan'))
            score += 0.15 * normalize(inv_pe.fillna(0))
            
        df["axiom_quality_score"] = score
        df = df.sort_values("axiom_quality_score", ascending=False)
        
        cols = ["symbol", "roic", "roe", "fcf_margin", "ttm_pe", "revenue_growth_yoy", "axiom_quality_score"]
        available_cols = [c for c in cols if c in df.columns]
        return df[available_cols]

    def get_market_movers(self, direction: str = "gainers") -> pd.DataFrame:
        """Returns top market gainers or losers. Source: Polygon."""
        endpoint = f"/v2/snapshot/locale/us/markets/stocks/{direction}"
        data = self._polygon_get(endpoint)
        if data and "tickers" in data:
            records = []
            for t in data["tickers"]:
                records.append({
                    "symbol": t.get("ticker"),
                    "name": t.get("ticker"),
                    "last_price": t.get("day", {}).get("c") or t.get("lastTrade", {}).get("p"),
                    "change_pct": t.get("todaysChangePerc"),
                    "volume": t.get("day", {}).get("v")
                })
            return pd.DataFrame(records)
        return pd.DataFrame()

    def get_technical_indicators(self, symbol: str, indicator: str, window: int = 14) -> pd.DataFrame:
        """Returns technical indicator series. Source: Polygon."""
        params = {"window": window}
        data = self._polygon_get(f"/v1/indicators/{indicator}/{symbol}", params=params)
        if data and "results" in data and "values" in data["results"]:
            df = pd.DataFrame(data["results"]["values"])
            if not df.empty:
                df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
                df = df.set_index("date")
                df = df.drop(columns=["timestamp"], errors="ignore")
                return df
        return pd.DataFrame()

    def health_check(self) -> dict[str, bool]:
        """Pings all three external APIs and returns availability status."""
        status = {}
        
        t_data = self._tiingo_get("/tiingo/daily/AAPL")
        status["tiingo"] = t_data is not None
        
        p_data = self._polygon_get("/v3/reference/tickers/AAPL")
        status["polygon"] = p_data is not None
        
        f_data = self._fred_get("GDP", end="2000-01-01")
        status["fred"] = not f_data.empty
        
        try:
            if Ticker is None:
                raise ImportError()
            Ticker("AAPL")
            status["defeatbeta"] = True
        except Exception:
            status["defeatbeta"] = False
            
        return status


class AxiomPortfolio:
    def __init__(self, initial_cash: float = 100_000.0):
        self.initial_cash: float = initial_cash
        self.cash: float = initial_cash
        self.positions: dict[str, dict] = {}
        self.transactions: list[dict] = []

    def buy(self, symbol: str, shares: float, price: float) -> None:
        """Records a buy. Deducts cash. Updates position avg_cost via weighted average."""
        cost = shares * price
        if cost > self.cash:
            raise ValueError(f"Insufficient funds: {cost} > {self.cash}")
            
        self.cash -= cost
        
        if symbol not in self.positions:
            self.positions[symbol] = {"shares": 0.0, "avg_cost": 0.0, "cost_basis": 0.0}
            
        pos = self.positions[symbol]
        total_shares = pos["shares"] + shares
        pos["avg_cost"] = ((pos["shares"] * pos["avg_cost"]) + cost) / total_shares
        pos["shares"] = total_shares
        pos["cost_basis"] = pos["shares"] * pos["avg_cost"]
        
        self.transactions.append({
            "timestamp": datetime.now().isoformat(),
            "action": "BUY",
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "value": cost,
            "cash_after": self.cash
        })

    def sell(self, symbol: str, shares: float, price: float) -> None:
        """Records a sell. Adds cash. Reduces position."""
        if symbol not in self.positions or shares > self.positions[symbol]["shares"]:
            raise ValueError(f"Invalid sell order for {symbol}")
            
        value = shares * price
        self.cash += value
        
        pos = self.positions[symbol]
        pos["shares"] -= shares
        pos["cost_basis"] = pos["shares"] * pos["avg_cost"]
        
        if pos["shares"] == 0:
            del self.positions[symbol]
            
        self.transactions.append({
            "timestamp": datetime.now().isoformat(),
            "action": "SELL",
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "value": value,
            "cash_after": self.cash
        })

    def get_positions(self) -> pd.DataFrame:
        """Returns current positions as DataFrame."""
        if not self.positions:
            return pd.DataFrame(columns=["symbol", "shares", "avg_cost", "cost_basis"])
            
        records = []
        for sym, data in self.positions.items():
            records.append({
                "symbol": sym,
                "shares": data["shares"],
                "avg_cost": data["avg_cost"],
                "cost_basis": data["cost_basis"]
            })
        return pd.DataFrame(records)

    def get_pnl(self, current_prices: dict[str, float]) -> pd.DataFrame:
        """Returns P&L summary given a dict of {symbol: current_price}."""
        if not self.positions:
            return pd.DataFrame(columns=["symbol", "shares", "avg_cost", "current_price", "market_value", "unrealized_pnl", "unrealized_pnl_pct"])
            
        records = []
        for sym, data in self.positions.items():
            curr_price = current_prices.get(sym, data["avg_cost"])
            mv = data["shares"] * curr_price
            pnl = mv - data["cost_basis"]
            pnl_pct = (pnl / data["cost_basis"] * 100) if data["cost_basis"] > 0 else 0.0
            
            records.append({
                "symbol": sym,
                "shares": data["shares"],
                "avg_cost": data["avg_cost"],
                "current_price": curr_price,
                "market_value": mv,
                "unrealized_pnl": pnl,
                "unrealized_pnl_pct": pnl_pct
            })
        return pd.DataFrame(records)

    def get_portfolio_value(self, current_prices: dict[str, float]) -> float:
        """Returns total portfolio value: cash + sum of market values."""
        mv_sum = 0.0
        for sym, data in self.positions.items():
            mv_sum += data["shares"] * current_prices.get(sym, data["avg_cost"])
        return self.cash + mv_sum

    def get_weights(self, current_prices: dict[str, float]) -> pd.DataFrame:
        """Returns portfolio weight allocation."""
        total_val = self.get_portfolio_value(current_prices)
        if total_val == 0:
            return pd.DataFrame(columns=["symbol", "market_value", "weight_pct"])
            
        records = [{
            "symbol": "CASH",
            "market_value": self.cash,
            "weight_pct": self.cash / total_val
        }]
        
        for sym, data in self.positions.items():
            mv = data["shares"] * current_prices.get(sym, data["avg_cost"])
            records.append({
                "symbol": sym,
                "market_value": mv,
                "weight_pct": mv / total_val
            })
        return pd.DataFrame(records)

    def get_transaction_log(self) -> pd.DataFrame:
        """Returns full transaction history."""
        if not self.transactions:
            return pd.DataFrame(columns=["timestamp", "action", "symbol", "shares", "price", "value", "cash_after"])
        return pd.DataFrame(self.transactions)
