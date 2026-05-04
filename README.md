# AXIOM — Adaptive Cross-regime Intelligent Order Management

> A regime-aware, multi-signal equity strategy that extends Microsoft Qlib with alternative data factors, heterogeneous model routing, and realistic execution simulation.

![Status](https://img.shields.io/badge/status-Phase%200%20Pending-lightgrey)

---

## Strategy Overview

AXIOM is a quantitative equity research system built on the thesis that **no single model dominates across all market regimes**. By detecting the current regime (Bull / Bear / Sideways) with a Gaussian HMM and routing predictions to specialised models — LightGBM for momentum, LSTM for drawdown dynamics, DoubleEnsemble for mean-reversion — the system adapts its factor weights and model architecture to the market environment. Custom alternative-data factors (earnings surprise, short interest, IV skew) augment Qlib's Alpha158 baseline, and all results pass through an Almgren-Chriss execution simulator to produce realistic, cost-adjusted returns.

Every component is benchmarked against a documented baseline so improvements are **provable, not claimed**.

```
RAW DATA LAYER
├── OHLCV (yfinance)
├── SEC EDGAR filings (earnings surprise)
├── FINRA short interest (biweekly)
└── Options chain IV skew (yfinance)
        ↓
FEATURE ENGINEERING LAYER
├── Alpha158 (baseline Qlib features)
└── AlphaAXIOM (custom factors: EPS surprise, short interest, IV skew)
        ↓
REGIME DETECTION LAYER
├── HMM on [VIX, yield curve slope, equity breadth]
└── Classifies market into: Bull / Bear / Sideways
        ↓
MODEL ROUTING LAYER
├── Bull regime  → LightGBM (momentum-biased features weighted up)
├── Bear regime  → LSTM (captures non-linear drawdown dynamics)
└── Sideways     → DoubleEnsemble (mean-reversion biased)
        ↓
PORTFOLIO CONSTRUCTION LAYER
├── TopkDropout signal → top 20 ranked stocks
├── Sector neutrality constraint (max 30% any single sector)
└── Risk-parity position sizing (not equal weight)
        ↓
EXECUTION SIMULATION LAYER
├── Almgren-Chriss market impact model
├── Bid-ask spread as f(ADV, volatility)
└── Transaction cost-adjusted returns
        ↓
EVALUATION LAYER
├── Annualized return, Sharpe, Sortino, Max Drawdown, Calmar
├── Information Coefficient (IC), ICIR, Rank IC
├── Benchmark: S&P 500 buy-and-hold
└── Per-regime performance breakdown
```

---

## Benchmark Table

| Strategy | Ann. Return | Sharpe | Max DD | ICIR |
|---|---|---|---|---|
| S&P 500 Buy & Hold | — | — | — | — |
| Qlib LightGBM Alpha158 | TBD | TBD | TBD | TBD |
| AXIOM (no regime routing) | TBD | TBD | TBD | TBD |
| AXIOM (full system) | TBD | TBD | TBD | TBD |
| AXIOM (realistic execution) | TBD | TBD | TBD | TBD |

> **Note:** TBD values are filled after each phase completes. Prototype results are never used. Each row is a controlled experiment isolating one variable's contribution.

---

## Build Phases

- [ ] **Phase 0** — Environment: Install Qlib, run Alpha158 baseline, record floor metrics
- [ ] **Phase 1** — AlphaAXIOM Factor Library: earnings surprise, short interest, IV skew (IC ≥ 0.02)
- [ ] **Phase 2** — Regime Detection: Gaussian HMM on VIX, yield curve, equity breadth
- [ ] **Phase 3** — Model Routing: LightGBM/LSTM/DoubleEnsemble per regime
- [ ] **Phase 4** — Portfolio Construction: risk-parity sizing, sector caps, weekly rebalance
- [ ] **Phase 5** — Execution Simulation: Almgren-Chriss impact model, bid-ask spread
- [ ] **Phase 6** — Evaluation & Writeup: benchmark table, per-regime breakdown, notebooks

---

## Repository Structure

```
AXIOM/
├── README.md                ← this file
├── docs/                    ← canonical project documentation
│   ├── PRD.md               ← phased build plan with acceptance criteria
│   ├── ARCHITECTURE.md      ← system architecture and module map
│   ├── DECISIONS.md         ← architectural decision records (ADRs)
│   └── CHANGELOG.md         ← chronological change log
├── wiki/                    ← Obsidian-compatible knowledge vault
│   ├── INDEX.md             ← vault entry point
│   └── concepts/            ← compiled concept pages
├── core/                    ← [PROTOTYPE] current strategy engine
│   ├── axiom_data_client.py ← defeatbeta-api wrapper, FRED, DuckDB
│   └── axiom_strategy.py    ← DCF scorer, macro regime, backtester
├── scripts/                 ← entry points and utilities
├── data/                    ← data acquisition and storage
│   ├── axiom_data_sync.py   ← yfinance S&P 500 bulk downloader
│   └── raw/                 ← downloaded market data
├── factors/                 ← (Phase 1) AlphaAXIOM factor library
├── regime/                  ← (Phase 2) HMM regime detection
├── models/                  ← (Phase 3) per-regime model configs
├── portfolio/               ← (Phase 4) risk-parity + sector constraints
├── execution/               ← (Phase 5) Almgren-Chriss simulation
├── backtest/                ← backtest runners and results
├── notebooks/               ← analysis and visualization
└── reports/                 ← generated output artifacts
```

---

## Setup

```bash
# Clone and install
git clone <repo>
cd AXIOM
pip install pyqlib lightgbm torch hmmlearn sec-edgar-downloader pandas yfinance

# Run baseline (Phase 0)
python -m qlib.run --config configs/workflow_config_lightgbm_Alpha158.yaml

# Run full AXIOM backtest (after all phases complete)
python backtest/run_axiom.py
```

---

## Knowledge System

AXIOM includes a self-maintaining knowledge infrastructure:

- **`docs/`** contains canonical documentation — PRD, architecture, decisions, and changelog. These are the source of truth.
- **`wiki/`** is an Obsidian-compatible vault containing LLM-compiled concept pages. Each page explains a core concept (Alpha158, regime detection, factor scoring, data layer) with cross-links.
- **`rules/`** contains Antigravity rules that enforce documentation discipline.
- **`raw/`** is the ingestion drop zone — place papers, research docs, or findings here and the wiki compiler will generate or update concept pages.

**Obsidian:** Point your vault at `AXIOM/wiki/` for graph view of concept relationships.

**Antigravity:** Say "compile wiki" after dropping files into `raw/` to trigger the LLM Wiki Compiler.

---

## Methodology Note

Each row in the benchmark table is a **controlled experiment**. One variable changes per row:

1. **S&P 500** — passive baseline (no model)
2. **Alpha158** — Qlib ML baseline (standard features, no custom factors)
3. **AXIOM no routing** — custom factors added, but same model for all regimes
4. **AXIOM full system** — regime detection + model routing active
5. **AXIOM realistic** — execution costs applied

This structure is what makes AXIOM a research project, not a demo. If the full system doesn't beat the baseline after execution costs, that is a valid and publishable result.
