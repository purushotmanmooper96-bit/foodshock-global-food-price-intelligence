# FOODSHOCK analytical report

Prepared 21 October 2026. Data through September 2026.

## Why this problem matters

Food procurement is exposed to international commodity-price changes and exchange-rate movements. A buyer deciding whether to review prices, suppliers or budgets needs a coherent view of recent changes, historical price levels and forecasting uncertainty. A global benchmark observatory is a manageable, evidence-backed first stage; it does not require inventing a company's purchase history.

The World Bank's commodity-market publications identify geopolitical, energy and supply pressures as relevant global context. Those publications motivate the question. This project's price-only dataset cannot isolate any particular cause.

## Research questions

1. Which selected benchmarks show the largest latest annual increases?
2. Are recent increases also unusual against each commodity's own recent history?
3. Can a lagged-price regression beat simple last-price or seasonal baselines?
4. How sensitive is an assumed procurement budget to commodity and FX changes?

## Observed findings

All figures below are calculated from the included World Bank snapshot. Prices are standardized to USD per metric ton.

| Commodity | Sep 2026 USD/mt | YoY | Index, 2020 average=100 |
|---|---:|---:|---:|
| Wheat | 347.0 | +48.4% | 149.8 |
| Soybean oil | 1,615.0 | +39.3% | 192.8 |
| Soybeans | 524.0 | +29.7% | 128.9 |
| Rice | 482.0 | +28.9% | 97.0 |
| Maize | 239.6 | +21.4% | 144.8 |
| Sugar | 410.0 | +17.1% | 144.7 |
| Palm oil | 1,180.0 | +13.8% | 157.0 |
| Cocoa | 5,920.0 | −15.8% | 249.7 |

**Finding 1 — pressure is broad but uneven.** Seven of the eight selected benchmarks increased year on year. Wheat and soybean oil show the largest increases. This describes this selected benchmark set; it is not a global food-price inflation index.

**Proposed response:** first investigate uncovered wheat/oil commitments and upcoming contract renewals. Rank real purchasing exposures using actual quantities and contracts before prioritizing by percentage changes. A large percentage increase in a small input can matter less than a small change in a major input.

**Finding 2 — direction and level tell different stories.** Cocoa is down 15.8% year on year but remains about 149.7% above its 2020 average. Rice is up 28.9% year on year but remains about 3.0% below its 2020 average. A growth-only chart would miss both distinctions.

**Proposed response:** show both YoY and a common-base index in procurement reviews. A price decline does not prove that a commodity is inexpensive, and a percentage increase does not prove it is at a historical extreme.

**Finding 3 — current annual pressure does not equal an unusual monthly jump.** None of the eight latest-month observations crosses the exploratory upward-shock threshold of z ≥ 2. Strong annual increases can accumulate without a single extreme monthly change.

**Proposed response:** keep annual-pressure review and sudden-shock investigation as separate triggers. Review a z-score flag with fresh quotes and source releases; do not use it as an automatic purchase instruction.

## Forecast evaluation

All commodities use the same chronology:

- Validation: October 2022–September 2024, 24 months.
- Test: October 2024–September 2026, 24 months.
- Next relative-to-snapshot estimate: October 2026.

Three candidates predict one month ahead at each rolling origin. The final 24 test months are not used to choose the model or calibrate its uncertainty band. Expanding model fits during the test period may use previously observed test-month prices, as they would become available in operation; they never use the month being predicted or later months.

| Commodity | Validation-selected model | Test MAPE | Test empirical-band coverage |
|---|---|---:|---:|
| Cocoa | Last price | 11.15% | 62.5% |
| Maize | Ridge lags | 4.27% | 83.3% |
| Palm oil | Last price | 3.85% | 75.0% |
| Rice | Last price | 5.26% | 66.7% |
| Soybean oil | Last price | 5.04% | 75.0% |
| Soybeans | Ridge lags | 3.00% | 87.5% |
| Sugar | Last price | 4.07% | 87.5% |
| Wheat | Ridge lags | 4.09% | 70.8% |

MAPE is mean absolute percentage error, not a probability of being correct. MAE is also supplied because percentage and absolute errors answer different questions. The uncertainty band targets 80% based on earlier residuals, but test coverage ranges from 62.5% to 87.5%. Its future coverage is not guaranteed.

**Finding 4 — complexity is not a reliable advantage.** Last-price wins validation for five commodities. Among the three ridge winners, test MAE improves about 0.7% for soybeans versus last-price, but worsens about 17.3% for maize and 15.2% for wheat. Validation ranking does not ensure future superiority.

**Proposed response:** treat these forecasts as a transparent planning baseline. Retain the simple comparison, monitor new errors and avoid automated sourcing based on this model. Before production use, add more evaluation folds, explicit benchmarks for uncertainty and verified explanatory variables. Do not tune on this test block and then continue calling it untouched.

### How the regression works

Target: log price for the next monthly observation. Features available strictly before the target are log-price lags 1, 2, 3 and 12, plus preceding 3- and 12-month means. Each ridge fit uses up to 120 earlier target months and scales inputs using training data only. Regularization alpha is fixed at 10; no claim of an optimized hyperparameter search is made. Exponentiating the log prediction gives a price estimate, not an explicitly bias-corrected conditional mean.

Shock calculation uses sample standard deviation of the previous 36 log returns. Volatility uses sample standard deviation of the latest 12 returns × square root of 12. Both are price-risk descriptors, not causal models.

## Budget model and solution demonstration

For baseline spend of 1,000,000 local currency units, assumed commodity shock of +20%, pass-through of 60% and currency depreciation of +10%:

```text
Stressed spend = 1,000,000 × (1 + 0.20 × 0.60) × (1 + 0.10)
               = 1,232,000
Additional monthly budget = 232,000
Percentage increase = 23.2%
```

This is an assumed scenario, not a finding about a real organization. The commodity and FX effects compound. Excel extends the idea to a quantity-weighted basket: each commodity's metric tons × USD/mt creates its base exposure; commodity-specific shocks and a shared pass-through create stressed USD costs; the exchange rate and FX shock convert the basket to local currency.

| Evidence/trigger | Proposed action | Evidence needed before implementation | Outcome to measure |
|---|---|---|---|
| High YoY on a large input exposure | Review contract renewal and supplier quotes | Purchase quantities, quote dates, contract terms | Budget variance and quote coverage |
| Upward shock flag | Investigate lead times and uncovered commitments | Supplier availability, inventory cover, source release | Stockout days, inventory carrying cost |
| Large FX sensitivity | Review invoice currency and currency exposure | Payment schedule and contract currency | FX-related purchase variance |
| High concentration in one ingredient | Evaluate approved substitutes or alternate suppliers | Quality, yield, safety, tariffs, freight, capacity | Total landed cost and rejection rate |
| Forecast error/coverage deterioration | Review model reliability and widen planning assumptions | Newly observed prices and logged predictions | MAE, MAPE and interval coverage |

No action's savings are measured by this dataset. A credible next phase would evaluate proposed actions against actual purchase costs, service levels and operational constraints.

## Data model and quality

Main fact grain: commodity × first day of calendar month. `prices` stores source metadata, original values, conversion factors, normalized prices and computed metrics. `dim_commodity` has eight unique commodity keys. `dim_date` is a monthly CSV helper; the Power BI guide instead creates a complete daily Calendar table.

Forecast grain is commodity × forecast month. Backtest grain is commodity × test month. Model-metric grain is commodity × candidate model. Join through dimensions rather than connecting fact tables directly.

Checks enforce unique fact keys, complete monthly calendars, positive selected prices, expected original units and no missing selected prices. There are 321 months per commodity. The first 12 months legitimately have no YoY, and shock scores require enough prior returns; these are not zero observations. Python and SQL MoM/YoY reconcile across all records.

## Limitations and development priorities

1. Eight selected international benchmarks do not represent the whole food system. No country-level comparisons or retail-inflation claims are supported.
2. Nominal USD prices are not inflation-adjusted. Procurement currency effects are illustrative unless real exposures are supplied.
3. Source history may be revised. This is a retrospective backtest on a current snapshot, not a real-time vintage-data backtest.
4. The raw workbook contains an ancillary Mismatch Details sheet. We preserve it and explicitly select Monthly Prices; independent reconciliation of the comparison sheet is outside this build.
5. Twenty-four test observations per commodity provide limited evidence. Empirical intervals can under-cover, particularly for cocoa.
6. Correlations and timing do not identify whether conflict, weather, energy, trade policy or other factors caused a change.
7. This is monthly, offline analysis. No live-feed, production-deployment, guaranteed accuracy or realized savings claim is made.
8. Power BI import/model assets need execution and visual acceptance in Desktop. The Excel file is a snapshot with formula updates for existing data and a documented manual extension process.

## A 90-second interview walkthrough

“I studied global food benchmark volatility because it creates procurement-budget uncertainty. I used World Bank monthly data, normalized the original units and validated calendar completeness and unique keys. SQL reproduces the monthly changes independently. My dashboard separates price levels, annual changes and sudden-shock signals.

“I compared ridge regression against last-price and seasonal baselines using separate validation and test periods. Last-price won five of eight validation comparisons. Ridge then underperformed the baseline on two of its three selected test series, which showed why model comparison and honest reporting matter.

“I built a scenario model for commodity and currency exposure. It helps a buyer test a budget assumption and decide what evidence to investigate next. It does not claim savings without actual procurement data. I would extend it with contracts, quantities, landed costs and additional time-based validation before operational use.”

## Sources

- World Bank commodity data and publications: https://www.worldbank.org/en/research/commodity-markets
- Monthly file and its exact hash: data/processed/manifest.json
- World Bank dataset terms: https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets
- Power BI references and acceptance instructions: powerbi/BUILD_GUIDE.md

All numerical findings and model scores in this report are computed from this project's included snapshot and output files. The proposals are analytical recommendations for investigation, not observed outcomes.

## Follow-up review

See [AUDIT_AND_FIXES.md](AUDIT_AND_FIXES.md) for code-level findings, fixes, independent numerical reconciliation and current validation boundaries. Existing numerical snapshots and model winners are unchanged. Selection and uncertainty calibration reuse the validation block, so intervals are exploratory rather than a formal out-of-sample coverage guarantee. Source metadata now ties provenance dates to the verified workbook hash and update label. See [LAUNCH_CONTENT.md](LAUNCH_CONTENT.md) for shareable explanations that retain these limits.
