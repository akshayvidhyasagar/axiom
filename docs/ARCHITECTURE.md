# AXIOM — Architecture Document

## System Architecture

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

## Repository Structure

```
AXIOM/
├── README.md                ← architecture diagram, benchmark table, methodology
├── AGENTS.md                ← GitNexus + Antigravity agent rules
├── ANTIGRAVITY.md           ← Antigravity editor config
│
├── docs/                    ← canonical project documentation
│   ├── PRD.md               ← phased build plan with acceptance criteria
│   ├── ARCHITECTURE.md      ← this file
│   ├── DECISIONS.md         ← architectural decision records (ADRs)
│   └── CHANGELOG.md         ← chronological change log
│
├── wiki/                    ← Obsidian-compatible knowledge vault
│   ├── index.md             ← master catalog
│   ├── hot.md               ← session context cache (~500 words)
│   ├── log.md               ← append-only operation log
│   ├── concepts/
│   │   ├── qlib-alpha158.md
│   │   ├── regime-detection.md
│   │   ├── factor-scoring.md
│   │   └── polygon-data-layer.md
│   ├── modules/             ← one page per AXIOM module
│   ├── decisions/           ← ADR navigation
│   ├── papers/              ← research paper summaries
│   ├── gaps/                ← open questions
│   ├── flows/               ← data flow diagrams
│   ├── sources/             ← ingested source summaries
│   └── meta/                ← dashboard, lint reports
│
├── rules/                   ← Antigravity knowledge-base rules
│   └── axiom-kb.md
│
├── skills/                  ← claude-obsidian skill definitions
│   ├── WIKI.md              ← master schema reference
│   ├── wiki/SKILL.md
│   ├── wiki-ingest/SKILL.md
│   ├── wiki-query/SKILL.md
│   ├── wiki-lint/SKILL.md
│   ├── wiki-fold/SKILL.md
│   ├── save/SKILL.md
│   ├── autoresearch/SKILL.md
│   ├── canvas/SKILL.md
│   └── obsidian-markdown/SKILL.md
│
├── raw/                     ← wiki ingestion drop zone (papers, docs, findings)
│   └── .gitkeep
│
├── core/                    ← PROTOTYPE: current strategy engine
│   ├── __init__.py
│   ├── axiom_data_client.py ← defeatbeta-api wrapper, FRED, local DuckDB
│   └── axiom_strategy.py    ← DCF + fundamentals scorer, macro regime, backtest
│
├── scripts/                 ← entry points and utilities
│   ├── __init__.py
│   ├── axiom_backtest.py    ← ⚠ DEPRECATED — prototype backtest (see ADR-002)
│   ├── axiom_main.py        ← prototype: live signal generation + report
│   ├── axiom_usage.py       ← prototype: API usage examples
│   └── axiom_report_gen.py  ← prototype: HTML report regeneration
│
├── data/                    ← data acquisition and storage
│   ├── axiom_data_sync.py   ← yfinance S&P 500 OHLCV bulk downloader
│   └── raw/                 ← downloaded market data
│       ├── ohlcv/           ← per-ticker OHLCV CSVs
│       ├── earnings/        ← (Phase 1) SEC EDGAR filings
│       ├── short_interest/  ← (Phase 1) FINRA biweekly data
│       └── options/         ← (Phase 1) options chain snapshots
│
├── factors/                 ← (Phase 1) AlphaAXIOM factor library
│   ├── alpha158_ext.py      ← custom factor definitions as Qlib ExpressionOps
│   └── factor_validation.py ← IC/ICIR per-factor validation
│
├── regime/                  ← (Phase 2) regime detection
│   ├── hmm_detector.py      ← Gaussian HMM, 3 hidden states
│   └── regime_labels.py     ← daily label output for routing
│
├── models/                  ← (Phase 3) per-regime model configs
│   ├── bull_model.yaml      ← LightGBM, momentum-biased
│   ├── bear_model.yaml      ← LSTM, volatility-biased
│   └── sideways_model.yaml  ← DoubleEnsemble, balanced
│
├── portfolio/               ← (Phase 4) portfolio construction
│   ├── risk_parity.py       ← inverse-volatility position sizing
│   └── sector_constraints.py ← GICS sector caps (30%)
│
├── execution/               ← (Phase 5) execution simulation
│   └── almgren_chriss.py    ← market impact + bid-ask model
│
├── backtest/                ← backtest runners and results
│   ├── run_baseline.py      ← (Phase 0) Qlib Alpha158 baseline
│   ├── run_axiom.py         ← (Phase 6) full AXIOM system backtest
│   └── results/             ← serialized backtest outputs
│
├── notebooks/               ← analysis and visualization
│   ├── factor_analysis.ipynb      ← (Phase 1) factor IC/ICIR
│   ├── regime_visualization.ipynb ← (Phase 2) regime overlay on price
│   └── results_analysis.ipynb     ← (Phase 6) final comparative analysis
│
└── reports/                 ← generated output artifacts
    └── axiom_report.html    ← prototype HTML investment report
```

---

## Frontend Stack

AXIOM includes a Vite-based frontend layer using the **shadcn/ui** design system with a blocks-first development protocol.

### Technology

| Layer | Tool | Config |
|-------|------|--------|
| Build | Vite | `vite.config.js` |
| Styling | Tailwind CSS v4 | `src/index.css` |
| Components | shadcn/ui (`@shadcn` registry) | `components.json` |
| Typography | Geist / Geist Mono | Loaded via CSS import |
| Icons | Lucide | `components.json → iconLibrary` |

### Frontend Directories

| Path | Purpose |
|------|---------|
| `src/index.css` | Global theme — Obsidian Dark CSS variables, Geist fonts, glassmorphism utilities |
| `components/ui/` | shadcn-managed component files — installed via `shadcn add`, not manually authored |
| `components.json` | shadcn registry configuration — style, aliases, icon library |
| `lib/utils` | Shared utilities (e.g., `cn()` class merge helper) |
| `index.html` | Vite entry point |

### Development Protocol

All frontend UI work follows the **Shadcn Blocks-First Protocol** defined in `ANTIGRAVITY.md`. Key rules:

1. Search `registry:block` for full page layouts before building custom layouts
2. Fall to `registry:ui` for individual primitives
3. Install via shadcn MCP tools — never manually create component files
4. Theme only via `src/index.css` CSS variables
5. Audit after every installation

---

## Module Dependency Map

| Module | Imports From | External Dependencies |
|--------|-------------|----------------------|
| `core/axiom_data_client.py` | — | `defeatbeta_api`, `requests`, `pandas`, `yfinance` |
| `core/axiom_strategy.py` | `core.axiom_data_client` | `pandas`, `math`, `concurrent.futures` |
| `scripts/axiom_backtest.py` | `core.axiom_data_client`, `core.axiom_strategy` | — |
| `scripts/axiom_main.py` | `core.axiom_data_client`, `core.axiom_strategy` | — |
| `scripts/axiom_usage.py` | `core.axiom_data_client`, `core.axiom_strategy` | — |
| `scripts/axiom_report_gen.py` | `core.axiom_data_client`, `core.axiom_strategy` | — |
| `data/axiom_data_sync.py` | — | `yfinance`, `requests`, `pandas` |

### Planned Dependencies (not yet implemented)

| Module | Imports From | External Dependencies |
|--------|-------------|----------------------|
| `factors/alpha158_ext.py` | — | `qlib` |
| `factors/factor_validation.py` | `factors.alpha158_ext` | `qlib`, `pandas`, `numpy` |
| `regime/hmm_detector.py` | — | `hmmlearn`, `pandas`, `numpy` |
| `regime/regime_labels.py` | `regime.hmm_detector` | `pandas` |
| `portfolio/risk_parity.py` | — | `numpy`, `pandas` |
| `portfolio/sector_constraints.py` | — | `pandas`, `yfinance` |
| `execution/almgren_chriss.py` | — | `numpy` |
| `backtest/run_baseline.py` | — | `qlib` |
| `backtest/run_axiom.py` | `regime`, `models`, `portfolio`, `execution` | `qlib` |

---

## Current State

The repository contains a **working prototype** built on the `defeatbeta-api` DuckDB data layer. This prototype provides:

- DCF + fundamentals-based signal scoring with macro regime awareness
- Point-in-time backtesting with lookahead bias prevention
- HTML investment report generation
- 15-ticker US large-cap universe

This prototype is **not** the target AXIOM system. It will be superseded by the Qlib-based architecture described above, starting with Phase 0.

---

## Deprecation Notices

| File | Status | Note |
|------|--------|------|
| `scripts/axiom_backtest.py` | ⚠ DEPRECATED | Prototype backtest. Will be replaced by `backtest/run_axiom.py` after Phase 0. See ADR-002. |
| `core/axiom_data_client.py` | PROTOTYPE | Will be superseded by Qlib data handlers + custom data fetchers in `data/`. |
| `core/axiom_strategy.py` | PROTOTYPE | Signal scoring will move to Qlib factor/model pipeline. Report generation may persist. |
