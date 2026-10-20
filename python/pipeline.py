"""Rebuild FOODSHOCK from the included World Bank snapshot. Python 3.11+."""
from pathlib import Path
import hashlib, json, sqlite3, sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/processed'
URL = 'https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx'
MAPPING = {
    'Wheat, US HRW': ('Wheat', 'Grains', 1),
    'Maize': ('Maize', 'Grains', 1),
    'Rice, Thai 5%': ('Rice', 'Grains', 1),
    'Soybeans': ('Soybeans', 'Oilseeds', 1),
    'Palm oil': ('Palm oil', 'Oils', 1),
    'Soybean oil': ('Soybean oil', 'Oils', 1),
    'Sugar, world': ('Sugar', 'Soft commodities', 1000),
    'Cocoa': ('Cocoa', 'Soft commodities', 1000),
}

def features(a, t):
    """All inputs strictly precede target month t. a contains log prices."""
    return np.array([a[t-1], a[t-2], a[t-3], a[t-12], a[t-3:t].mean(), a[t-12:t].mean()])

def predict(a, t, model):
    if model == 'Last price':
        return float(a[t-1])
    if model == 'Seasonal naive':
        return float(a[t-12])
    # Expanding fit with at most 120 historical target months; fixed alpha=10.
    start = max(12, t-120)
    X = np.array([features(a, i) for i in range(start, t)])
    y = a[start:t]
    mu, scale = X.mean(0), X.std(0)
    scale[scale < 1e-10] = 1
    Z = np.c_[np.ones(len(X)), (X-mu)/scale]
    penalty = np.eye(Z.shape[1])*10
    penalty[0, 0] = 0
    coef = np.linalg.solve(Z.T@Z+penalty, Z.T@y)
    return float(np.r_[1, (features(a, t)-mu)/scale]@coef)

def scenario(spend, shock, fx, passed):
    """Illustrative local-currency spend, constant quantities and immediate pass-through."""
    if spend < 0 or shock <= -1 or fx <= -1 or not 0 <= passed <= 1:
        raise ValueError('Invalid scenario assumptions')
    return spend * (1 + shock*passed) * (1 + fx)

def load_prices():
    raw = pd.read_excel(ROOT/'data/raw/worldbank_monthly.xlsx', sheet_name='Monthly Prices', header=None)
    names = [str(x).strip() for x in raw.iloc[4]]
    data = raw.iloc[6:].copy()
    valid = data.iloc[:,0].astype(str).str.match(r'^\d{4}M\d{2}$')
    data = data.loc[valid]
    dates = pd.to_datetime(data.iloc[:,0], format='%YM%m')
    rows = []
    for source, (name, category, factor) in MAPPING.items():
        pos = names.index(source)
        source_unit = str(raw.iloc[5,pos])
        expected = '$/kg' if factor == 1000 else '$/mt'
        if expected not in source_unit:
            raise ValueError(f'Unit changed for {source}: {source_unit}')
        values = pd.to_numeric(data.iloc[:,pos], errors='coerce')
        for dt, value in zip(dates, values):
            if dt.year >= 2000:
                rows.append([dt.strftime('%Y-%m-%d'),name,category,source,source_unit,
                             None if pd.isna(value) else float(value),factor,
                             None if pd.isna(value) else float(value)*factor])
    df = pd.DataFrame(rows, columns=['date','commodity','category','source_series','source_unit','source_price','conversion_factor','price_usd_mt'])
    if df.duplicated(['date','commodity']).any():
        raise ValueError('Duplicate keys')
    if df.price_usd_mt.isna().any() or (df.price_usd_mt <= 0).any():
        raise ValueError('Missing/nonpositive selected prices: do not silently impute')
    df = df.sort_values(['commodity','date']).reset_index(drop=True)
    for _, g in df.groupby('commodity'):
        expected_dates = pd.date_range(g.date.min(),g.date.max(),freq='MS')
        if len(g) != len(expected_dates):
            raise ValueError('Incomplete monthly calendar')
    return df

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_prices()
    df['mom'] = df.groupby('commodity').price_usd_mt.pct_change(fill_method=None)
    df['yoy'] = df.groupby('commodity').price_usd_mt.pct_change(12,fill_method=None)
    df['log_return'] = df.groupby('commodity').price_usd_mt.transform(lambda s: np.log(s).diff())
    df['shock_z'] = df.groupby('commodity').log_return.transform(lambda s: (s-s.shift(1).rolling(36).mean())/s.shift(1).rolling(36).std())
    df['volatility_12m'] = df.groupby('commodity').log_return.transform(lambda s:s.rolling(12).std()*np.sqrt(12))
    df['index_2020'] = df.groupby('commodity').price_usd_mt.transform(lambda s:100*s/s[df.loc[s.index,'date'].str.startswith('2020')].mean())
    df['alert'] = np.where(df.shock_z >= 2,'Upward shock',np.where(df.shock_z <= -2,'Downward shock','Normal'))
    df.loc[df.shock_z.isna(),'alert'] = 'Insufficient history'
    metrics, forecasts, backtests = [], [], []
    models = ['Last price','Seasonal naive','Ridge lags']
    for commodity, g in df.groupby('commodity'):
        a = np.log(g.price_usd_mt.to_numpy())
        n = len(a)
        # Model selection ends before the untouched last-24-month test block.
        preds = {m:np.array([predict(a,t,m) for t in range(n-48,n)]) for m in models}
        actual = np.exp(a[-48:])
        vmae = {m:float(np.mean(np.abs(np.exp(p[:24])-actual[:24]))) for m,p in preds.items()}
        selected = min(models,key=lambda m:vmae[m])
        residual = np.abs(a[-48:-24] - preds[selected][:24])
        q = float(np.quantile(residual,.8))
        for m,p in preds.items():
            test = np.exp(p[24:])
            metrics.append(dict(commodity=commodity,model=m,selected=int(m==selected),validation_mae=vmae[m],
                test_mae=float(np.abs(test-actual[24:]).mean()),test_mape=float((np.abs(test-actual[24:])/actual[24:]).mean()),
                test_interval_coverage=float((np.abs(a[-24:]-p[24:]) <= q).mean()) if m==selected else None,
                test_months=24,validation_start=g.date.iloc[-48],validation_end=g.date.iloc[-25],test_start=g.date.iloc[-24],test_end=g.date.iloc[-1]))
        for j,t in enumerate(range(n-24,n)):
            backtests.append(dict(date=g.date.iloc[t],commodity=commodity,actual=float(np.exp(a[t])),prediction=float(np.exp(preds[selected][j+24])),model=selected))
        f=predict(a,n,selected)
        forecasts.append(dict(date=(pd.Timestamp(g.date.iloc[-1])+pd.offsets.MonthBegin()).strftime('%Y-%m-%d'),
            commodity=commodity,model=selected,forecast=float(np.exp(f)),lower80=float(np.exp(f-q)),upper80=float(np.exp(f+q)),
            last_price=float(np.exp(a[-1])),change=float(np.exp(f-a[-1])-1)))
    latest=df[df.date==df.date.max()].sort_values('yoy',ascending=False)
    frames={'prices':df,'latest':latest,'model_metrics':pd.DataFrame(metrics),'forecasts':pd.DataFrame(forecasts),'backtest':pd.DataFrame(backtests)}
    dim=df[['commodity','category','source_series','source_unit','conversion_factor']].drop_duplicates()
    frames['dim_commodity']=dim
    frames['dim_date']=pd.DataFrame({'date':sorted(df.date.unique())})
    frames['dim_date']['year']=pd.to_datetime(frames['dim_date'].date).dt.year
    frames['dim_date']['month']=pd.to_datetime(frames['dim_date'].date).dt.month
    for name, frame in frames.items():
        frame.to_csv(OUT/f'{name}.csv',index=False)
    with sqlite3.connect(ROOT/'foodshock.sqlite') as con:
        for name, frame in frames.items(): frame.to_sql(name,con,if_exists='replace',index=False)
        con.executescript((ROOT/'sql/analysis.sql').read_text())
        sql_latest=pd.read_sql('SELECT * FROM vw_latest',con)
        assert len(sql_latest)==len(latest)
        assert np.allclose(sql_latest.sort_values('commodity').yoy,latest.sort_values('commodity').yoy)
    manifest=dict(source_url=URL,source_sheet='Monthly Prices',snapshot_sha256=hashlib.sha256((ROOT/'data/raw/worldbank_monthly.xlsx').read_bytes()).hexdigest(),
        retrieved_on='2026-10-21',source_updated='2026-10-02',start=df.date.min(),end=df.date.max(),rows=len(df),commodities=len(dim),
        missing_selected_prices=int(df.price_usd_mt.isna().sum()),duplicates=int(df.duplicated(['date','commodity']).sum()),
        source_note='Workbook contains ancillary Mismatch Details. Analysis uses Monthly Prices only; original snapshot preserved. No claim of independent price verification.')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    clean=lambda f:json.loads(f.to_json(orient='records'))
    payload={k:clean(v) for k,v in frames.items()}
    payload['manifest']=manifest
    (OUT/'dashboard_data.json').write_text(json.dumps(payload,allow_nan=False))
    template=(ROOT/'python/dashboard_template.html').read_text()
    (ROOT/'FOODSHOCK_Dashboard.html').write_text(template.replace('__DATA__',json.dumps(payload,allow_nan=False)))
    print(json.dumps(manifest,indent=2))
    print(latest[['commodity','price_usd_mt','yoy','shock_z']].to_string(index=False))
    print(pd.DataFrame(metrics).query('selected==1')[['commodity','model','test_mape','test_interval_coverage']].to_string(index=False))

if __name__ == '__main__': main()
