# AXIOM — Product Requirements Document

> **AXIOM** — Adaptive Cross-regime Intelligent Order Management

## Core Thesis

A regime-aware, multi-signal equity strategy that extends Microsoft Qlib with alternative data factors, heterogeneous model routing, and realistic execution simulation. Every component is benchmarked against a documented baseline so improvements are provable, not claimed.

---

## Build Phases

### Phase 0 — Environment (3 days)
- [ ] Install Qlib, pull US equity data 2015–2024 via yfinance
- [ ] Run `workflow_config_lightgbm_Alpha158.yaml` end-to-end
- [ ] Record baseline metrics (annualized return, Sharpe, max DD, ICIR)

**Acceptance criteria:** Qlib LightGBM Alpha158 backtest completes without error; baseline metrics logged to `backtest/results/baseline.json`.

**Tools:** `pyqlib`, `lightgbm`, `torch`, `hmmlearn`, `sec-edgar-downloader`, `pandas`, `yfinance`

---

### Phase 1 — AlphaAXIOM Factor Library (2 weeks)
- [ ] Build Factor Group A — Earnings Surprise (SUE, revision momentum)
- [ ] Build Factor Group B — Short Interest (SIR, 14-day delta)
- [ ] Build Factor Group C — Options Signal (IV skew, put/call ratio)
- [ ] Validate each factor: standalone IC and ICIR computed; factors with IC < 0.02 dropped
- [ ] Implement as Qlib-compatible `ExpressionOps` module in `factors/alpha158_ext.py`

**Acceptance criteria:** At least 2 of 3 factor groups pass IC ≥ 0.02 threshold; `factors/factor_validation.py` produces reproducible IC/ICIR report.

**Data sources:**
- Earnings: SEC EDGAR via `sec-edgar-downloader` (free)
- Short interest: FINRA biweekly CSV (free)
- Options: `yfinance` options chain (free)

---

### Phase 2 — Regime Detection (1 week)
- [ ] Engineer features: 20-day VIX rolling mean, 10Y-2Y yield spread (FRED API), NYSE advance-decline ratio
- [ ] Train Gaussian HMM with 3 hidden states via `hmmlearn`
- [ ] Label states post-hoc by average market return during each state period
- [ ] Output daily regime label for routing layer

**Acceptance criteria:** Regime transitions align visually with known market events (2020 COVID crash, 2022 bear market); `regime/hmm_detector.py` produces daily labels.

---

### Phase 3 — Model Routing (2 weeks)
- [ ] Train Bull model: LightGBM with momentum-biased feature weights
- [ ] Train Bear model: LSTM with volatility/short-interest-biased feature weights
- [ ] Train Sideways model: DoubleEnsemble with balanced weighting
- [ ] Implement routing: HMM regime → corresponding model → ranked stock signals

**Acceptance criteria:** Each model individually beats Alpha158 baseline on its "home" regime periods; routing logic is testable in isolation.

---

### Phase 4 — Portfolio Construction (1 week)
- [ ] Replace TopkDropoutStrategy with custom allocator
- [ ] Top 20 signals from active model
- [ ] Sector cap: max 30% exposure to any GICS sector
- [ ] Risk-parity position sizing: w_i = (1/σ_i) / Σ(1/σ_j)
- [ ] Weekly rebalance cadence

**Acceptance criteria:** No single sector exceeds 30% in any rebalance period; position sizes verifiably reflect inverse-volatility weighting.

---

### Phase 5 — Execution Simulation (1 week)
- [ ] Implement Almgren-Chriss market impact model
- [ ] Temporary impact: η × σ × (order_size / ADV)^0.6
- [ ] Permanent impact: γ × σ × (order_size / ADV)
- [ ] Bid-ask spread: spread = α / √(ADV)
- [ ] Document implementation shortfall (idealized vs realistic equity curves)

**Acceptance criteria:** Implementation shortfall is computed and documented; `execution/almgren_chriss.py` is unit-tested.

---

### Phase 6 — Evaluation & Writeup (1 week)
- [ ] Fill benchmark table with final metrics
- [ ] Per-regime performance breakdown
- [ ] Complete README with architecture diagram, benchmark table, methodology
- [ ] Produce `notebooks/results_analysis.ipynb` with reproducible figures

**Acceptance criteria:** Benchmark table has all 5 rows filled; every metric is reproducible from committed code.

---

## Timeline

| Week | Work |
|------|------|
| 1 | Phase 0 + data pipeline setup |
| 2–3 | Phase 1: AlphaAXIOM factors |
| 4 | Phase 2: HMM regime detection |
| 5–6 | Phase 3: model routing |
| 7 | Phase 4–5: portfolio + execution |
| 8 | Phase 6: benchmarking + README |
