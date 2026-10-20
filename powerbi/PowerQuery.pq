// Create a blank query named FoodshockModel, paste this into Advanced Editor.
// Change RootFolder to your extracted folder. Then create the five reference queries below.
let
    RootFolder = "C:\Users\LENOVO\Downloads\FOODSHOCK",
    ReadCSV = (name as text, types as list) as table =>
        let
            Raw = Csv.Document(File.Contents(RootFolder & "\data\processed\" & name & ".csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            Headers = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
            Nulls = Table.ReplaceValue(Headers,"",null,Replacer.ReplaceValue,Table.ColumnNames(Headers)),
            Typed = Table.TransformColumnTypes(Nulls,types,"en-US")
        in Typed,
    Prices = ReadCSV("prices",{{"date",type date},{"commodity",type text},{"category",type text},{"source_price",type number},{"conversion_factor",Int64.Type},{"price_usd_mt",type number},{"mom",type number},{"yoy",type number},{"log_return",type number},{"shock_z",type number},{"volatility_12m",type number},{"index_2020",type number},{"alert",type text}}),
    Commodities = ReadCSV("dim_commodity",{{"commodity",type text},{"category",type text},{"conversion_factor",Int64.Type}}),
    Forecasts = ReadCSV("forecasts",{{"date",type date},{"commodity",type text},{"forecast",type number},{"lower80",type number},{"upper80",type number},{"last_price",type number},{"change",type number}}),
    Backtest = ReadCSV("backtest",{{"date",type date},{"commodity",type text},{"actual",type number},{"prediction",type number}}),
    Metrics = ReadCSV("model_metrics",{{"commodity",type text},{"selected",Int64.Type},{"validation_mae",type number},{"test_mae",type number},{"test_mape",type number},{"test_interval_coverage",type number},{"test_months",Int64.Type},{"validation_start",type date},{"validation_end",type date},{"test_start",type date},{"test_end",type date}})
in [prices=Prices,dim_commodity=Commodities,forecasts=Forecasts,backtest=Backtest,model_metrics=Metrics]

// Create separate blank queries, with the exact names below, each using ONE expression:
// prices:         = FoodshockModel[prices]
// dim_commodity:  = FoodshockModel[dim_commodity]
// forecasts:      = FoodshockModel[forecasts]
// backtest:       = FoodshockModel[backtest]
// model_metrics:  = FoodshockModel[model_metrics]
// Disable load for FoodshockModel. Apply changes for the five table queries.
