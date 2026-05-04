# Regime Detection

> Related: [[qlib-alpha158]], [[factor-scoring]]

## What It Is

Regime detection classifies the current market environment into discrete states so that different models, feature weights, and risk parameters can be applied contextually. AXIOM uses a **Gaussian Hidden Markov Model (HMM)** with 3 hidden states, trained on observable market indicators.

## AXIOM Architecture

### Input Features

| Feature | Source | Rationale |
|---------|--------|-----------|
| 20-day VIX rolling mean | FRED (`VIXCLS`) | Implied volatility captures fear/complacency |
| 10Y-2Y yield spread | FRED (`T10Y2Y`) | Yield curve inversion predicts recessions |
| NYSE advance-decline ratio | Computed from breadth data | Market participation breadth |

### Hidden States

The HMM learns 3 states from data. Post-hoc labeling assigns names based on average market return during each state:

| State | Label | Typical Characteristics |
|-------|-------|------------------------|
| 0 | **Bull** | Low VIX, positive yield spread, broad participation |
| 1 | **Bear** | High VIX, flat/inverted yield curve, narrow breadth |
| 2 | **Sideways** | Moderate VIX, mixed signals, mean-reverting price action |

### Model Routing

Each regime routes to a different model in Phase 3:

- **Bull** → LightGBM (momentum-biased features weighted up)
- **Bear** → LSTM (captures non-linear drawdown dynamics)
- **Sideways** → DoubleEnsemble (mean-reversion biased)

## Implementation

```python
# regime/hmm_detector.py
from hmmlearn import hmm
import numpy as np

class RegimeDetector:
    def __init__(self, n_states=3):
        self.model = hmm.GaussianHMM(
            n_components=n_states,
            covariance_type="full",
            n_iter=100
        )
    
    def fit(self, features: np.ndarray):
        """Train on [VIX_20d, yield_spread, adv_dec_ratio]"""
        self.model.fit(features)
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Return daily regime labels"""
        return self.model.predict(features)
```

## Validation

Regime transitions should align with known market events:
- **2020-02 → 2020-03:** Bull → Bear (COVID crash)
- **2020-04 → 2020-11:** Bear → Bull (Fed intervention rally)
- **2022-01 → 2022-10:** Bull → Bear (inflation/rate hike cycle)
- **2023-01 → 2023-06:** Bear → Sideways (soft landing uncertainty)

## Comparison with Prototype

The current prototype uses a rule-based 4-state classifier (`goldilocks`, `risk_on`, `risk_off`, `stagflation`) with hard thresholds on GDP growth, CPI, and credit spreads. This was abandoned in favour of the HMM approach (see ADR-003) because:

1. Hard thresholds don't adapt to evolving market regimes
2. The 4-state model produced identical classifications across all backtest quarters
3. HMM states are data-driven and capture non-linear regime boundaries
