# Qlib Alpha158

> Related: [[factor-scoring]], [[regime-detection]]

## What It Is

Alpha158 is Microsoft Qlib's built-in feature set consisting of 158 technical factors computed from OHLCV data. It serves as the **baseline** for all AXIOM experiments — every custom factor, regime model, and routing decision is measured against Alpha158's standalone performance.

## Factor Categories

Alpha158 includes factors across several domains:

- **Price momentum:** returns over 5, 10, 20, 30, 60 day windows
- **Volume patterns:** VWAP ratios, volume moving averages, turnover
- **Volatility:** rolling standard deviation of returns (multiple windows)
- **Mean reversion:** distance from N-day high/low, Bollinger band position
- **Technical indicators:** RSI, MACD signal line, KDJ, Williams %R

## Role in AXIOM

1. **Phase 0:** Run LightGBM on Alpha158 to establish the floor metrics (Ann. Return, Sharpe, Max DD, ICIR)
2. **Phase 1:** AlphaAXIOM factors (earnings surprise, short interest, IV skew) are added **on top of** Alpha158, not replacing it
3. **Phase 3:** Per-regime models each receive the full Alpha158 + AlphaAXIOM feature set, with different feature weights per regime

## Qlib Configuration

The baseline experiment uses:

```yaml
model:
  class: LGBModel
  kwargs:
    loss: mse
    colsample_bytree: 0.8
    learning_rate: 0.1
dataset:
  class: Alpha158
  kwargs:
    instruments: csi500  # or sp500 equivalent
    start_time: "2015-01-01"
    end_time: "2024-12-31"
```

## Key Metrics to Record

| Metric | Description |
|--------|-------------|
| IC | Pearson correlation between predicted and actual returns |
| ICIR | IC / std(IC) — stability of predictive power |
| Rank IC | Spearman rank correlation — more robust to outliers |
| Ann. Return | Annualized portfolio return after TopkDropout |
| Sharpe | Risk-adjusted return |
| Max DD | Maximum peak-to-trough drawdown |

## References

- [Qlib Alpha158 documentation](https://qlib.readthedocs.io/en/latest/component/data.html#alpha158)
- [Qlib GitHub — Alpha158 source](https://github.com/microsoft/qlib/tree/main/qlib/contrib/data/handler.py)
