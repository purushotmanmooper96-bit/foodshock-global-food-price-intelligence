# Build the Power BI report

Status: import queries, measures, theme and page specifications supplied. These have not been executed in Power BI Desktop in this environment. No .pbix is included. The HTML dashboard is the working, independently usable dashboard.

1. Extract FOODSHOCK to a permanent folder. Open Power BI Desktop, Get data > Blank query > Advanced Editor. Paste PowerQuery.pq and change RootFolder. Name it FoodshockModel.
2. Create the five reference queries documented at the bottom of that file. Disable load for FoodshockModel and apply changes. Do not import `latest.csv` as a second price fact.
3. Create Calendar using the first declaration in Measures.dax. Mark Calendar as a date table using Calendar[Date]. Calendar is daily and includes the forecast month; the CSV dim_date is monthly and should not be marked as a daily date table.
4. Create single-direction, one-to-many relationships:

| One side | Many side | Direction |
|---|---|---|
| dim_commodity[commodity] | prices[commodity] | Dimension to fact |
| dim_commodity[commodity] | forecasts[commodity] | Dimension to fact |
| dim_commodity[commodity] | backtest[commodity] | Dimension to fact |
| dim_commodity[commodity] | model_metrics[commodity] | Dimension to fact |
| Calendar[Date] | prices[date] | Calendar to prices |
| Calendar[Date] | backtest[date] | Calendar to backtest |
| Calendar[Date] | forecasts[date] | Calendar to forecasts |

5. Create each remaining DAX table and each measure separately. Shock, FX, PassThrough and Spend remain disconnected from all other tables. Use single-select slicers on their Value columns.
6. Import theme.json from View > Themes > Browse for themes. Use a 1440 × 900 custom page, dark canvas and a left navigation area approximately 210 px wide. Add page navigation buttons. Default commodity: Wheat, single select. Avoid 3D charts; compare values using consistent scales.

## Page specifications

| Page | Visuals and field assignments |
|---|---|
| Executive overview | Cards: Latest price, Latest YoY, Latest index, Shock signal. Line: Calendar[Date] versus Index 2020. Bar: dim_commodity[commodity] versus Latest YoY. Matrix: commodity with Latest price/MoM/YoY/index. Commodity and date slicers. |
| Forecast laboratory | Cards: Next forecast, Lower band, Upper band, Test MAPE, Test band coverage. Line: Calendar[Date] with Actual test price and Predicted test price, filtered to nonblank backtest values. Table: model_metrics model, validation_mae, test_mae, test_mape, selected. |
| Budget simulator | Single-select sliders: Shock[Value], FX[Value], PassThrough[Value], Spend[Value]. Cards: Baseline spend, Stressed spend, Additional budget, Budget change. Add the assumptions and formula from the HTML simulator. |
| Evidence and methodology | Data period, provider, source URL, grain, unit conversion, validation/test dates and model limitations. Explain that international benchmark changes are not domestic retail inflation. |

For the cross-commodity ranking, disable the commodity slicer's interaction with that bar chart, while keeping date interaction enabled. Otherwise the single-select slicer reduces the ranking to one bar. For the model laboratory, avoid a page-level date filter that hides test observations. Forecast measures intentionally ignore Calendar filters so the next month remains visible.

## Acceptance checks in Desktop

- September 2026, Wheat: latest price 347 USD/mt, YoY 48.41745%, index 149.84346.
- Sugar: 410 USD/mt. Verify conversion from 0.41 USD/kg.
- Cocoa: 5,920 USD/mt; YoY −15.78947% despite a 2020-based index of 249.70123.
- Default simulator: baseline 1,000,000, shock 20%, FX 10%, pass-through 60% gives 1,232,000 and a 23.2% change.
- No commodity selection or multiple commodities: price cards intentionally blank, rather than summing unlike benchmark prices.
- First 12 months of YoY remain blank. Annual averages use only available months, not summed prices.
- Change slicers, export underlying data, verify forecast boundaries, then save FOODSHOCK.pbix. Record Desktop version and acceptance results before calling the Power BI report tested.

## Microsoft references

- https://learn.microsoft.com/power-bi/guidance/star-schema
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables
- https://learn.microsoft.com/power-bi/desktop-what-if

Python model outputs refresh by running the pipeline, then Home > Refresh in Desktop. They do not retrain inside DAX. The Excel workbook contains a data snapshot; pipeline refresh does not automatically rebuild Excel.
