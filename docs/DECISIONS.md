# AXIOM — Architectural Decision Records

> Each ADR documents a decision that shapes the system. Once accepted, an ADR is immutable — supersede it with a new ADR, don't edit it.

---

## ADR-001: Use Qlib as the backtest and factor framework

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** AXIOM needs a factor evaluation, model training, and backtesting framework. Options considered: Zipline (abandoned upstream), Backtrader (no ML pipeline), QuantConnect (cloud-locked), Qlib (Microsoft, active, ML-native).  
**Decision:** Adopt Microsoft Qlib as the core framework. All factors will be implemented as `ExpressionOps`, all models as Qlib-compatible trainers, and all backtests via Qlib's `backtest` module.  
**Consequences:** Locked to Qlib's data format (requires `qlib.init()` data prep). Gains: built-in Alpha158 baseline, IC/ICIR evaluation, TopkDropout strategy, and a large research community.

---

## ADR-002: Deprecate prototype backtest in favour of Qlib pipeline

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** The current `scripts/axiom_backtest.py` and `core/axiom_strategy.py` implement a prototype strategy based on DCF scoring + macro regime detection using the `defeatbeta-api` data layer. This prototype was used for initial exploration and debugging (2026-05–04 sessions). It is not the target architecture.  
**Decision:** Mark `scripts/axiom_backtest.py` as DEPRECATED. The prototype code in `core/` will remain for reference but will not be part of the AXIOM evaluation pipeline. The target backtest entry point is `backtest/run_axiom.py` (Phase 6).  
**Consequences:** Prototype results (e.g., "198% return, 8 trades") must not appear in the benchmark table. Only Qlib-pipeline results are valid for the benchmark.

---

## ADR-003: Regime detection via HMM, not rule-based thresholds

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** The prototype uses a hand-coded macro regime classifier (`detect_macro_regime` in `axiom_strategy.py`) with hard thresholds on GDP growth, CPI, HY spread, and yield curve. This produces a deterministic 4-state classification that doesn't learn from data.  
**Decision:** Replace with a Gaussian HMM trained on [VIX, yield curve slope, equity breadth] that classifies into 3 states (Bull/Bear/Sideways). States are labeled post-hoc by average market return.  
**Consequences:** Requires `hmmlearn` dependency. States are data-driven and may not map 1:1 to intuitive labels until post-hoc labeling is applied. The prototype's 4-state model (`goldilocks`, `risk_on`, `risk_off`, `stagflation`) is abandoned.

---

## ADR-004: Free data sources only — no paid API dependencies

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** The prototype relies on `defeatbeta-api` (DuckDB-based, free), FRED (free), and fallback to Tiingo/Polygon (API-key-gated, rate-limited). For the target AXIOM system, all data must be reproducible by anyone cloning the repo.  
**Decision:** Use only free data sources: `yfinance` for OHLCV/options, `sec-edgar-downloader` for earnings, FINRA CSV for short interest, FRED API for macro. No Tiingo, no Polygon, no Bloomberg.  
**Consequences:** Options data quality may be lower than commercial feeds. Earnings data requires parsing SEC filings rather than using a pre-built API. This is acceptable for a research project.

---

## ADR-005: Point-in-time data discipline for all backtests

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** During prototype debugging (2026-05-03/04), a critical bug was discovered: the DCF valuation engine used current (2024+) financial data when computing fair values for historical rebalance dates (e.g., 2020-Q1). This introduced severe lookahead bias, producing unrealistic 305% returns driven entirely by NVDA's price trajectory.  
**Decision:** All data access in backtests must be point-in-time (PIT). For the prototype, this was patched via method-mocking on the `defeatbeta-api` Ticker class. For the target Qlib system, Qlib's built-in PIT data handling will be used, supplemented by explicit `at_date` filtering on custom data fetchers.  
**Consequences:** Backtest performance will be lower but realistic. Any new data source added to AXIOM must document its PIT boundary (when data becomes available after the fact).

---

## ADR-006: Threshold-based signal selection, not rank-based top-N

**Date:** 2026-05-04  
**Status:** Accepted  
**Context:** The prototype's signal generator was found to produce exactly 2 BUY signals every quarter, regardless of market conditions. Root cause: implicit `.head(2)` / `nlargest(2)` caps in the scoring pipeline. This made the strategy deterministic and non-adaptive.  
**Decision:** Signal selection must be threshold-based (e.g., `raw_score >= 0.65`) so that the number of BUY signals varies with market conditions. For the target Qlib system, this maps to TopkDropout with a configurable k, but the principle remains: the count of selected signals must vary across time periods.  
**Consequences:** Some rebalance periods may produce 0 BUY signals (cash position), others may produce 10+. Position sizing must handle variable portfolio sizes.
