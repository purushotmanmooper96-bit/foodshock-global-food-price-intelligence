# Data dictionary

| File | Grain / purpose |
|---|---|
| prices.csv | One commodity-month, full normalized history and metrics |
| latest.csv | Eight latest-month rows; convenience output, not a second analytical fact |
| dim_commodity.csv | One commodity; category and original-unit mapping |
| dim_date.csv | One month; monthly helper rather than a marked Power BI daily date table |
| forecasts.csv | One commodity in the next month relative to last observation |
| model_metrics.csv | One commodity-candidate model; validation and test metrics |
| backtest.csv | One commodity-test month, validation-selected model only |
| manifest.json | Source, hash, dates, counts, caveat |
| dashboard_data.json | Same outputs serialized for the HTML dashboard |

## prices.csv

| Column | Type | Meaning |
|---|---|---|
| date | ISO date | First day of represented month, not release date |
| commodity | Text | Stable key shared with dimension |
| category | Text | Project grouping for grains, oils, oilseeds, soft commodities |
| source_series | Text | Trimmed original World Bank series header |
| source_unit | Text | Original workbook unit label |
| source_price | Decimal | Original price, before unit conversion |
| conversion_factor | Integer | 1 or 1,000 |
| price_usd_mt | Decimal | source_price × conversion_factor |
| mom | Decimal fraction | Price / prior-month price − 1 |
| yoy | Decimal fraction | Price / same-month prior-year price − 1 |
| log_return | Decimal | Natural log of current/prior price |
| shock_z | Decimal | Current log return vs preceding 36 log returns, sample standard deviation |
| volatility_12m | Decimal | Latest 12 monthly log returns' sample SD × √12 |
| index_2020 | Decimal | 100 × price / 2020 average monthly price |
| alert | Text | Upward shock, Downward shock, Normal, Insufficient history |

Empty lag/rolling results mean unavailable history. Do not replace them with zero. Percentage measures are fractions (0.1 means 10%), while index_2020 is an index in points.

## Forecasts and model metrics

`forecast`, `lower80`, `upper80`, `last_price`, `validation_mae` and `test_mae` use USD/metric ton. `change`, `test_mape` and `test_interval_coverage` are fractions. `selected` is 1 for exactly one validation winner per commodity and 0 otherwise. `model` identifies Last price, Seasonal naive or Ridge lags. The coverage result is only populated for selected models because the project calibrates a band for the selected model only.

The `validation_start/end` and `test_start/end` fields make split boundaries explicit. Backtest predictions use the selected model, with training updated only as earlier actual observations become available. Forecast dates are monthly periods, not a claim that predictions were published before that month began.
