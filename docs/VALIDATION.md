# Validation evidence

Completed 21 October 2026.

## Executed

- Python 3.12.14: complete pipeline executed against the preserved World Bank snapshot.
- Six unittest cases passed: unit conversion/calendar size; SQL/Python MoM and YoY reconciliation across all 2,568 records; prediction invariance when current/future prices are altered; separate validation/test chronology and model selection; interval ordering and missing-history behavior; known-value scenario and invalid-input guard.
- Dependency-free Node.js interaction checks passed: eight commodity selections × three history windows; populated finite chart/table output; four navigation controls; known-value FX sensitivity; negative-budget input; selected-history CSV creation.
- Excel authored with native formulas, validation rules and two native editable charts. Workbook recalculated, key ranges inspected, Wheat YoY reconciled to Python and FX sensitivity changed/restored successfully. Overview rendered and visually reviewed. Chart labels adjusted for readability. Exported workbook inspected for formula-error values and chart references.
- Included database's SQL views executed successfully. Selected-model comparison exposes the actual baseline improvements and regressions.

## Not executed here

- Native browser rendering/responsive-layout/real download acceptance. A browser binary could not be installed in this environment. JavaScript tests use a lightweight DOM stub, so they do not prove CSS appearance or browser download behavior. Open the delivered HTML and inspect each page at desktop/mobile widths before publishing screenshots.
- Power BI Desktop import, DAX execution, visual interactions or .pbix generation. The Desktop guide includes expected values for acceptance. No tested Power BI report is claimed.
- Excel desktop application acceptance. The workbook was calculated, rendered and exported with the artifact engine; check it in your installed Excel before presenting it. Native feature definitions are included.
- Live source refresh or an operational deployment. All models run on the included snapshot. No external user accounts, company systems or paid APIs are involved.

## Refresh controls

Archive the old source, verify update date and schema, run the pipeline and tests, review changed historical values and model winners, refresh Power BI and update the Excel snapshot as documented. Do not overwrite a past evaluation claim with a newly tuned model while reusing the same test period as independent evidence.

## Follow-up audit: 21 October 2026

The updated JavaScript source passed expanded logic checks in an isolated JavaScript runtime. All 2,568 records independently reconciled for conversion, MoM, YoY, index rebasing and shock z-scores (maximum absolute difference below 1e-9). Python guards, UTF-8 handling and provenance validation were revised; the local Python environment was unavailable for this follow-up, so these changes are not covered by the earlier six-test pass. Ten Python test methods and a Linux/Windows GitHub Actions definition are now supplied. Workflow results, when available, are the execution evidence. Browser rendering and Power BI Desktop acceptance remain unexecuted. See AUDIT_AND_FIXES.md for detail.
