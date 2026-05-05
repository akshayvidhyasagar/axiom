---
type: concept
title: "Data Layer Architecture"
created: 2026-05-04
updated: 2026-05-04
tags:
  - concept
status: developing
related:
  - "[[qlib-alpha158]]"
  - "[[factor-scoring]]"
---

# Data Layer Architecture

## What It Is

The data layer is the foundation of every AXIOM computation. It defines how raw market data flows from external sources into the feature engineering pipeline. Every data source must satisfy two constraints: **free access** (no paid APIs — see ADR-004) and **point-in-time discipline** (no lookahead bias — see ADR-005).

## Data Sources

### OHLCV Price Data

| Attribute | Value |
|-----------|-------|
| Source | `yfinance` |
| Coverage | US equities, 2015–2024 |
| Frequency | Daily |
| Storage | `data/raw/ohlcv/{TICKER}.csv` |
| Fetcher | `data/axiom_data_sync.py` (bulk S&P 500 downloader) |

### SEC EDGAR Filings (Earnings Surprise)

| Attribute | Value |
|-----------|-------|
| Source | `sec-edgar-downloader` |
| Data | 10-Q/10-K filings, parsed for actual EPS vs consensus |
| Frequency | Quarterly |
| Storage | `data/raw/earnings/` |
| Fetcher | `data/fetch_earnings.py` (Phase 1) |
| Factor | SUE = (actual_EPS - consensus_EPS) / std(EPS_estimates) |

### FINRA Short Interest

| Attribute | Value |
|-----------|-------|
| Source | FINRA biweekly CSV (free download) |
| Data | Short shares outstanding per ticker |
| Frequency | Biweekly |
| Storage | `data/raw/short_interest/` |
| Fetcher | `data/fetch_short_interest.py` (Phase 1) |
| Factor | SIR = short_shares / avg_daily_volume |

### Options Chain (IV Skew)

| Attribute | Value |
|-----------|-------|
| Source | `yfinance` options chain |
| Data | Implied volatility surface, put/call volumes |
| Frequency | Daily (when markets open) |
| Storage | `data/raw/options/` |
| Fetcher | `data/fetch_options.py` (Phase 1) |
| Factor | IV_skew = IV(OTM put) - IV(ATM call) |

### Macro / Regime Inputs

| Attribute | Value |
|-----------|-------|
| Source | FRED API (free key) |
| Series | VIX (`VIXCLS`), 10Y-2Y spread (`T10Y2Y`), GDP (`GDPC1`), CPI (`CPIAUCSL`) |
| Frequency | Daily (VIX, yields) / Quarterly (GDP) / Monthly (CPI) |
| Used by | [[regime-detection]] HMM feature engineering |

## Data Flow

```
External APIs → data/fetch_*.py → data/raw/{category}/ → Qlib data prep → Alpha158 + AlphaAXIOM features
```

## Point-in-Time Discipline

All data access in backtests must be point-in-time (PIT). This means:

1. **No future data:** When computing signals for date *t*, only data available before *t* is used
2. **Publication lag:** SEC filings have a ~45-day lag; earnings data for Q1 is not available until mid-May
3. **Qlib alignment:** Qlib's built-in PIT handling covers OHLCV; custom factors must implement their own `at_date` filtering

This was identified as a critical issue during prototype debugging (see ADR-005).

## Prototype Data Layer

The current prototype uses a different data stack:

| Component | Prototype | Target AXIOM |
|-----------|-----------|-------------|
| Price data | `defeatbeta-api` DuckDB | `yfinance` → Qlib format |
| Fundamentals | `defeatbeta-api` Ticker | SEC EDGAR parsed |
| Macro | FRED API via `requests` | FRED API (same) |
| Valuation | `defeatbeta-api` DCF engine | Not used (ML-driven) |

The prototype data layer (`core/axiom_data_client.py`) will be superseded by individual fetchers in `data/` once Phase 0 begins.
