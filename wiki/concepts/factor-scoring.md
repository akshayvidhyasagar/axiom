---
type: concept
title: "Factor Scoring"
created: 2026-05-04
updated: 2026-05-04
tags:
  - concept
status: developing
related:
  - "[[qlib-alpha158]]"
  - "[[regime-detection]]"
---

# Factor Scoring

## What It Is

Factor scoring is the quantitative validation process that determines whether a candidate factor has genuine predictive power for future stock returns. AXIOM uses **Information Coefficient (IC)** and **Information Coefficient Information Ratio (ICIR)** as the primary gatekeeping metrics. Factors that fail validation are dropped — this discipline separates research from noise.

## Key Metrics

### Information Coefficient (IC)

The Pearson correlation between the factor's cross-sectional values at time *t* and the realised returns at time *t+1*:

```
IC_t = corr(factor_values_t, returns_{t+1})
```

A single IC value is computed per time period. The average IC across all periods is the factor's predictive power.

| IC Value | Interpretation |
|----------|---------------|
| < 0.02 | **Drop** — indistinguishable from noise |
| 0.02–0.05 | Weak but usable in ensemble |
| 0.05–0.10 | Strong — typical of good Alpha158 factors |
| > 0.10 | Very strong — rare, check for lookahead bias |

### ICIR (Information Coefficient Information Ratio)

```
ICIR = mean(IC) / std(IC)
```

Measures the **stability** of predictive power. A factor with IC = 0.04 but ICIR = 2.0 is preferable to one with IC = 0.06 but ICIR = 0.5 — consistent weak signal beats unstable strong signal.

| ICIR Value | Interpretation |
|------------|---------------|
| < 0.5 | Unstable — unreliable for live trading |
| 0.5–1.0 | Moderate — acceptable for ensemble |
| > 1.0 | Stable — strong candidate |

### Rank IC

Spearman rank correlation instead of Pearson. More robust to outliers and non-linear relationships. Used as a secondary check.

## AXIOM Factor Validation Pipeline

```
factors/factor_validation.py
├── Load Alpha158 + AlphaAXIOM features
├── For each factor:
│   ├── Compute daily cross-sectional IC
│   ├── Compute ICIR over full sample
│   ├── Compute Rank IC
│   └── Flag if IC < 0.02 → DROP
├── Output: factor_report.csv
└── Surviving factors → model training
```

## AlphaAXIOM Factor Groups

| Group | Factors | Source | IC Threshold |
|-------|---------|--------|-------------|
| A — Earnings Surprise | SUE, revision momentum | SEC EDGAR | ≥ 0.02 |
| B — Short Interest | SIR, 14-day SIR delta | FINRA CSV | ≥ 0.02 |
| C — Options Signal | IV skew, put/call ratio | yfinance | ≥ 0.02 |

Each factor group is validated independently before being added to the model. At least 2 of 3 groups must pass for Phase 1 to be considered complete.

## Relationship to Regime Detection

Factor IC may vary by [[regime-detection|regime]]. A factor that is strong in Bull markets but weak in Bear markets is still valuable — it will receive higher weight in the Bull model and lower weight in the Bear model (Phase 3, model routing).

Per-regime IC analysis is performed in `notebooks/factor_analysis.ipynb`.
