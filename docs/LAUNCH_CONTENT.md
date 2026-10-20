# FOODSHOCK launch content

Prepared for manual sharing. Nothing has been posted to LinkedIn or another social platform. Reach and virality are not guaranteed.

## LinkedIn post

Cocoa prices fell 15.8% year on year.
They were still 149.7% above their 2020 average.

That contrast became the central story of FOODSHOCK, my independent food-price analytics project.

Using 2,568 World Bank commodity-month observations across eight benchmarks, I built:

• An interactive dashboard for price levels, annual changes and unusual monthly movements.
• An Excel workbook with editable procurement-budget scenarios.
• SQL views that independently reproduce price changes.
• A Python pipeline comparing regression with last-price and seasonal baselines.
• A Power BI build kit with import queries, DAX and report instructions. Desktop assembly is still required.

The modeling result was just as useful: last-price forecasts won validation for five of eight commodities. Regression then underperformed that baseline on two of its three selected test series.

The proposed use is practical: identify exposed inputs, review supplier quotes and test budget assumptions before changing procurement.

A sample scenario combining a 20% commodity shock, 60% pass-through and 10% currency depreciation increases assumed spend by 23.2%. That is a scenario calculation, not measured company savings.

The dashboard, source data, code, findings and limitations are public:
https://github.com/purushotmanmooper96-bit/foodshock-global-food-price-intelligence

Which would you investigate first in a procurement review: annual price increases, volatility or currency exposure?

#DataAnalytics #Python #SQL #Excel #DataVisualization

## Seven-slide carousel script

| Slide | Headline | Evidence / supporting copy |
|---|---|---|
| 1 | Cocoa fell 15.8%. Still 149.7% above 2020. | September 2026 snapshot. Nominal USD benchmark. |
| 2 | One percentage change cannot tell the whole story. | Cocoa index: 249.7 with 2020 average = 100. Rice rose 28.9% YoY but its index was 97.0. |
| 3 | The question I investigated | Which benchmarks show pressure, how predictable are next-month prices, and how do assumed shocks change a budget? |
| 4 | The data workflow | World Bank snapshot → Python cleaning/models → SQL reconciliation → Excel scenarios → interactive dashboard. Power BI build kit supplied separately. |
| 5 | The simple baseline often won | Last-price won validation for 5/8 commodities. Ridge underperformed the baseline on two of its three selected test series. |
| 6 | A budget stress test | Baseline 1,000,000 × (1 + 20% × 60%) × (1 + 10%) = 1,232,000. Assumptions, not realized costs. |
| 7 | Explore the evidence | Link to the repository. Include source, as-of date, limitations and Power BI build-kit status. Ask one specific procurement question. |

Use docs/social-card.svg as the first visual. Export it to PNG in a browser or design application if the social platform does not accept SVG. Keep source/as-of labels visible.

## Short video narration

“Cocoa prices fell 15.8% year on year, but they were still almost 150% above their 2020 average.

I investigated that gap using eight World Bank food benchmarks. FOODSHOCK combines price trends, shock signals, model evaluation and procurement-budget scenarios.

One result surprised me: the simplest forecast won validation for five of eight commodities. The regression model did not consistently beat it on the test period.

The project helps structure the next questions for a buyer: what exposure do we have, which quotes need review and how sensitive is our budget?

The code, dashboard, source data and limitations are in the public repository.”

## Repository description and topics

Suggested description:
Global food-price risk analysis with Excel, SQL, Python, an interactive dashboard and a Power BI build kit. World Bank data, forecast evaluation and procurement scenarios.

Suggested topics:
data-analysis, python, sql, excel, power-bi, food-prices, time-series, procurement, data-visualization, portfolio-project

These are suggestions; repository metadata has not been changed unless separately verified.

## Sharing checklist

- Use the provided source/as-of date rather than calling the figures live prices.
- Demonstrate one dashboard interaction and one decision question.
- Show model errors and uncertainty along with attractive charts.
- Ask for specific feedback on procurement interpretation or model evaluation.
- Add the repository to your GitHub profile and LinkedIn Featured section.
- Keep this independent project separate from employment experience.
- Do not claim country-level inflation coverage, optimized buying decisions, guaranteed accuracy, a completed .pbix or measured savings.
