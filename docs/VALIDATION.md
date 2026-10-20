# Validation evidence

Review completed 21 October 2026.

[Verified GitHub Actions run](https://github.com/purushotmanmooper96-bit/foodshock-global-food-price-intelligence/actions/runs/39495977933)  
Tested code commit: 0beebc0056f81050d975ec219f40f49b502d937c  
Pull request: https://github.com/purushotmanmooper96-bit/foodshock-global-food-price-intelligence/pull/1

## Executed audit checks

| Check | Result and scope |
|---|---|
| Independent numerical reconciliation | All 2,568 records reconciled for unit conversion, MoM, YoY, 2020 index and shock z-score; maximum absolute difference below 1e-9 |
| Python rebuild, Ubuntu | Passed against the preserved source snapshot with provenance validation |
| Python rebuild, Windows | Passed with PYTHONUTF8=0, exercising explicit text encodings |
| Python regression suite | 10 tests passed on each platform, including finite/range/overflow guards, source metadata, zero-variance shock behavior, model origins, split chronology and SQL reconciliation |
| JavaScript DOM checks | Passed on both platforms; eight commodities × three history windows, page visibility, contextual controls, valid/invalid budgets, missing chart values and CSV construction/cleanup |
| Real Chromium desktop | Passed at 1440 × 1100: benchmark selection, all four pages, scenario input handling, a real quoted UTF-8 CSV download and zero page errors |
| Real Chromium mobile | Passed at 390 × 844: controls visible and no whole-page horizontal overflow |
| Captures | Desktop overview, forecast and scenario plus mobile overview saved in workflow artifacts; artifacts expire according to the workflow retention period |

## Original Excel checks

The unchanged Excel workbook was authored with 267 formulas and two native editable charts. The original build recalculated it, reconciled Wheat YoY to Python, tested and restored FX sensitivity, rendered the overview, inspected chart references and found no exported formula-error cells. It was not opened in desktop Excel during this audit.

## Limits of the checks

- Browser smoke tests verify concrete interactions and a specified viewport; they do not prove pixel-perfect design, accessibility conformance, every browser or every device.
- No Power BI Desktop execution or finished .pbix is claimed.
- Excel remains a snapshot with a documented manual refresh process.
- Numerical output snapshots and model winners were preserved. This audit does not establish predictive superiority or future uncertainty coverage.
- The source workbook's ancillary Mismatch Details sheet was not independently reconciled.
- Code/runtime dependencies use version ranges and CI action major-version references; this is not a fully locked reproducibility environment.
- No live data refresh, realized procurement savings, social-media publication or production deployment is claimed.

## Refresh controls

Archive the old source, verify its update label and units, update source_metadata.json with the new hash and retrieval evidence, then run the pipeline and tests. Review revised history/model winners, refresh Power BI and update the Excel snapshot as documented. Keep evaluation periods independent of future tuning decisions.
