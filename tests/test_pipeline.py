"""Run from project root: python -m unittest discover -s tests -v."""
import unittest, sys, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'python'))
from pipeline import predict, scenario, load_prices, source_metadata, shock_scores

class TestFoodshock(unittest.TestCase):
    def test_scenario_rejects_nonfinite_inputs(self):
        for values in [(float('nan'),.2,.1,.6),(1,float('inf'),.1,.6),
                       (1,.2,float('nan'),.6),(1,.2,.1,float('inf')),(1e308,1e308,.1,.6)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                scenario(*values)

    def test_unknown_model_and_short_history(self):
        for model, origin in [('unknown',50),('Ridge lags',12),('Seasonal naive',11)]:
            with self.subTest(model=model), self.assertRaises(ValueError):
                predict(np.arange(60,dtype=float),origin,model)

    def test_zero_variance_shocks_are_unavailable(self):
        self.assertTrue(shock_scores(pd.Series(np.zeros(100))).isna().all())

    def test_snapshot_metadata_matches_bytes(self):
        metadata=source_metadata()
        self.assertRegex(metadata['snapshot_sha256'],r'^[0-9a-f]{64}
        df=load_prices()
        sugar=df.query("commodity=='Sugar'").iloc[-1]
        self.assertAlmostEqual(sugar.source_price*1000,sugar.price_usd_mt)
        self.assertEqual(len(df),df.date.nunique()*df.commodity.nunique())

    def test_sql_python_every_month(self):
        p=pd.read_csv(ROOT/'data/processed/prices.csv')
        with sqlite3.connect(ROOT/'foodshock.sqlite') as c:
            s=pd.read_sql('SELECT commodity,date,mom,yoy FROM vw_price_changes',c)
        m=p.merge(s,on=['commodity','date'],suffixes=('_p','_s'),validate='one_to_one')
        self.assertEqual(len(m),len(p))
        for field in ['mom','yoy']:
            self.assertTrue(np.allclose(m[field+'_p'],m[field+'_s'],equal_nan=True))

    def test_forecast_has_no_future_access(self):
        a=np.log(np.linspace(100,250,180))
        for model in ['Last price','Seasonal naive','Ridge lags']:
            original=predict(a,150,model)
            changed=a.copy();changed[150:]=100
            self.assertAlmostEqual(original,predict(changed,150,model))

    def test_temporal_split_and_winner(self):
        m=pd.read_csv(ROOT/'data/processed/model_metrics.csv')
        for _,g in m.groupby('commodity'):
            winner=g[g.selected==1]
            self.assertEqual(len(winner),1)
            self.assertAlmostEqual(winner.validation_mae.iloc[0],g.validation_mae.min())
            self.assertTrue((g.validation_end<g.test_start).all())
            self.assertTrue((g.test_months==24).all())

    def test_intervals_and_data_history(self):
        f=pd.read_csv(ROOT/'data/processed/forecasts.csv')
        self.assertTrue((f.lower80<=f.forecast).all())
        self.assertTrue((f.forecast<=f.upper80).all())
        p=pd.read_csv(ROOT/'data/processed/prices.csv')
        self.assertTrue(p.groupby('commodity').head(12).yoy.isna().all())
        self.assertEqual(f.date.nunique(),1)
        expected=(pd.Timestamp(p.date.max())+pd.offsets.MonthBegin()).strftime('%Y-%m-%d')
        self.assertEqual(f.date.iloc[0],expected)

    def test_scenario_known_values_and_guards(self):
        self.assertAlmostEqual(scenario(1000000,.2,.1,.6),1232000)
        self.assertAlmostEqual(scenario(1000000,.2,0,0),1000000)
        self.assertEqual(scenario(0,.2,.1,.6),0)
        with self.assertRaises(ValueError):scenario(-1,.2,.1,.6)

if __name__=='__main__':unittest.main()
)
        self.assertLessEqual(metadata['source_updated'],metadata['retrieved_on'])

    def test_source_units(self):
        df=load_prices()
        sugar=df.query("commodity=='Sugar'").iloc[-1]
        self.assertAlmostEqual(sugar.source_price*1000,sugar.price_usd_mt)
        self.assertEqual(len(df),df.date.nunique()*df.commodity.nunique())

    def test_sql_python_every_month(self):
        p=pd.read_csv(ROOT/'data/processed/prices.csv')
        with sqlite3.connect(ROOT/'foodshock.sqlite') as c:
            s=pd.read_sql('SELECT commodity,date,mom,yoy FROM vw_price_changes',c)
        m=p.merge(s,on=['commodity','date'],suffixes=('_p','_s'),validate='one_to_one')
        self.assertEqual(len(m),len(p))
        for field in ['mom','yoy']:
            self.assertTrue(np.allclose(m[field+'_p'],m[field+'_s'],equal_nan=True))

    def test_forecast_has_no_future_access(self):
        a=np.log(np.linspace(100,250,180))
        for model in ['Last price','Seasonal naive','Ridge lags']:
            original=predict(a,150,model)
            changed=a.copy();changed[150:]=100
            self.assertAlmostEqual(original,predict(changed,150,model))

    def test_temporal_split_and_winner(self):
        m=pd.read_csv(ROOT/'data/processed/model_metrics.csv')
        for _,g in m.groupby('commodity'):
            winner=g[g.selected==1]
            self.assertEqual(len(winner),1)
            self.assertAlmostEqual(winner.validation_mae.iloc[0],g.validation_mae.min())
            self.assertTrue((g.validation_end<g.test_start).all())
            self.assertTrue((g.test_months==24).all())

    def test_intervals_and_data_history(self):
        f=pd.read_csv(ROOT/'data/processed/forecasts.csv')
        self.assertTrue((f.lower80<=f.forecast).all())
        self.assertTrue((f.forecast<=f.upper80).all())
        p=pd.read_csv(ROOT/'data/processed/prices.csv')
        self.assertTrue(p.groupby('commodity').head(12).yoy.isna().all())
        self.assertEqual(f.date.nunique(),1)
        expected=(pd.Timestamp(p.date.max())+pd.offsets.MonthBegin()).strftime('%Y-%m-%d')
        self.assertEqual(f.date.iloc[0],expected)

    def test_scenario_known_values_and_guards(self):
        self.assertAlmostEqual(scenario(1000000,.2,.1,.6),1232000)
        self.assertAlmostEqual(scenario(1000000,.2,0,0),1000000)
        self.assertEqual(scenario(0,.2,.1,.6),0)
        with self.assertRaises(ValueError):scenario(-1,.2,.1,.6)

if __name__=='__main__':unittest.main()
