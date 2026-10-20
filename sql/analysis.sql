-- SQLite 3.25+. Grain: one commodity per calendar month. Null lag history stays null.
CREATE UNIQUE INDEX IF NOT EXISTS ix_prices_key ON prices(commodity,date);
DROP VIEW IF EXISTS vw_price_changes;
CREATE VIEW vw_price_changes AS
WITH lagged AS (
 SELECT date,commodity,category,price_usd_mt,
 LAG(price_usd_mt,1) OVER(PARTITION BY commodity ORDER BY date) AS previous_month,
 LAG(price_usd_mt,12) OVER(PARTITION BY commodity ORDER BY date) AS previous_year
 FROM prices
)
SELECT *,price_usd_mt/NULLIF(previous_month,0)-1 AS mom,
 price_usd_mt/NULLIF(previous_year,0)-1 AS yoy FROM lagged;
DROP VIEW IF EXISTS vw_latest;
CREATE VIEW vw_latest AS
SELECT * FROM vw_price_changes WHERE date=(SELECT MAX(date) FROM prices);
DROP VIEW IF EXISTS vw_annual_summary;
CREATE VIEW vw_annual_summary AS
SELECT commodity,SUBSTR(date,1,4) AS year,COUNT(*) AS months,
 AVG(price_usd_mt) AS mean_usd_mt,MIN(price_usd_mt) AS minimum_usd_mt,
 MAX(price_usd_mt) AS maximum_usd_mt
FROM prices GROUP BY commodity,SUBSTR(date,1,4);
-- An incomplete year is intentionally not labelled a full-year result.
DROP VIEW IF EXISTS vw_model_comparison;
CREATE VIEW vw_model_comparison AS
SELECT s.commodity,s.model,s.test_mape,s.test_interval_coverage,
 1-s.test_mae/NULLIF(b.test_mae,0) AS test_mae_improvement_vs_last_price
FROM model_metrics s JOIN model_metrics b ON s.commodity=b.commodity
AND b.model='Last price' WHERE s.selected=1;
-- Investigation queries:
-- SELECT * FROM vw_latest ORDER BY yoy DESC;
-- SELECT commodity,date,shock_z,mom FROM prices WHERE ABS(shock_z)>=2 ORDER BY date DESC;
-- SELECT * FROM vw_model_comparison;
-- SELECT * FROM vw_annual_summary WHERE months=12;
