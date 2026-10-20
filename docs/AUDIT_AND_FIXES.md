# FOODSHOCK audit and fixes

Audit date: 21 October 2026. Baseline commit: 9200497072515b71f8820d49dded04dfda966ae0.

## Issues addressed

| Issue | Impact | Change |
|---|---|---|
| Python text files relied on platform-default encoding | Windows code pages could fail on the Unicode HTML template | Explicit UTF-8 for all template, SQL, JSON and HTML reads/writes |
| Non-finite scenario inputs were not fully rejected | NaN/infinite inputs could produce invalid budget results | Finite/range checks, overflow rejection and regression cases in Python and JavaScript |
| Blank baseline input was treated as numeric zero | An omitted input appeared to be an intentional zero budget | Blank rejected; an explicit zero remains valid and percentage change is unavailable |
| Negative ranking values were drawn beside commodity labels | Text could overlap and obscure the chart | Dedicated right-aligned value column |
| Export URL was immediately revoked | Browser download behavior could be unreliable | Attach/click/remove the link and defer URL cleanup; quoted CSV, CRLF and UTF-8 BOM added |
| Missing chart values could be plotted as zero | A gap could appear as a real observed value | Break SVG paths at missing/non-finite values; display unavailable metrics as n.a. |
| Commodity controls stayed visible on the total-budget page | Users could infer that commodity selection drove assumed spend | Context-specific controls and explicit total-spend scenario wording |
| Source dates were hardcoded in the pipeline | A future refresh could inherit stale provenance | Hash-checked source_metadata.json and workbook update-date reconciliation |
| Zero variance could divide a shock score by zero | Infinite scores could break strict JSON output | Undefined scores remain missing; regression case added |
| Insufficient or incompatible source history was not rejected early | Short series or incomplete baselines could reach model fitting | Minimum history, baseline completeness, matching calendars and unique source-column guards |
| Unknown model names silently ran ridge regression | A typo could select the wrong forecasting method | Explicit model-name, forecast-origin and finite-training validation |
| Prior navigation tests did not assert visibility | Tests could pass despite incorrect page state | Stateful DOM mock, visibility assertions and contextual-control checks |
| Mobile grids could exceed the viewport | Whole-page horizontal scrolling on a narrow phone display | Shrinkable grid tracks, bounded panels and compact heatmap labels; verified at 390 px in Chromium |
| No repeatable cross-platform test workflow | Future changes lacked a standard validation route | Linux/Windows GitHub Actions definition for rebuild, Python tests and dashboard logic |
| The README hid its strongest analytical story | A reader had to search for a reason to explore | Evidence-based share graphic, clear entry links and launch content |

## Numerical audit executed during this review

Independent JavaScript calculations reconciled all 2,568 price records:
unit conversions, MoM, YoY, 2020 rebasing and 36-month shock scores. Maximum absolute differences were below 0.000000001, consistent with serialized decimal rounding.

The updated dashboard source was executed with the same expanded DOM logic assertions used by tests/test_dashboard.cjs. The checks covered eight commodities × three windows, four navigation states, contextual controls, invalid/zero/overflow inputs, missing chart values and CSV construction/cleanup. This is logic validation, not real-browser rendering.

## Execution evidence

A new test initially had a syntax error and the first Chromium run exposed mobile overflow. Both failures were corrected before publication; the linked successful run records the final code. Existing model results were not changed to improve reported scores.

## Boundaries and remaining work

- The initial local execution environment was unavailable. GitHub Actions subsequently ran the Python rebuild, 10 regression tests and JavaScript logic checks on Windows and Linux, plus a real Chromium desktop/mobile smoke test. [Execution evidence](https://github.com/purushotmanmooper96-bit/foodshock-global-food-price-intelligence/actions/runs/39495977933), tested commit 0beebc0056f81050d975ec219f40f49b502d937c.
- Chromium verified navigation, invalid-input handling, native CSV download, zero page errors and no whole-page horizontal overflow at 390 px. Captures were saved as workflow artifacts. Pixel-perfect visual QA, other-browser coverage and Power BI Desktop execution remain outside this evidence.
- The Excel binary and existing numerical/model output snapshots are unchanged by this review. Excel remains a snapshot with documented manual refresh steps.
- Regression underperformance is a reported result, not an error to hide. No winner was switched using the held-out test results.
- Model choice and uncertainty calibration reuse the validation block. Bands are exploratory; no formal coverage guarantee is claimed.
- Source history may be revised; the backtest uses a current snapshot rather than contemporaneous data vintages.
- The source workbook's ancillary Mismatch Details sheet remains unreconciled independently.
- A complete .pbix, automated Excel rebuild, live data feed and deployment remain separate deliverables.
- Shareability was improved with a specific question, a simple visual and transparent evidence. Virality and hiring outcomes cannot be promised.
