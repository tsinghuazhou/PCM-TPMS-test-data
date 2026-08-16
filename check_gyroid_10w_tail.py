"""Check tail of Gyroid 10W repeat data"""
import pandas as pd
import numpy as np

df = pd.read_csv('tpms_gyroid10w_20260808_165138.csv', encoding='utf-8-sig')
df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
df['elapsed'] = (pd.to_datetime(df['time']) - pd.to_datetime(df['time'].iloc[0])).dt.total_seconds()

# T1 derivative last 5 min
m = df['elapsed'] >= df['elapsed'].max() - 300
dT1 = df.loc[m, 'T1'].diff().mean()
print(f"T1 avg slope last 5 min: {dT1:.3f} C/s ({dT1*60:.2f} C/min)")

# Is heating still ON at end? Check if T1 still rising
print(f"T1 last 60s start: {df.loc[df['elapsed']>=df['elapsed'].max()-60,'T1'].iloc[0]:.2f}")
print(f"T1 last value: {df['T1'].iloc[-1]:.2f}")

# When did T1 stop rising (peak time)?
t1_ema = df['T1'].ewm(alpha=0.1, adjust=False).mean()
deriv = t1_ema.diff()
rising = df.loc[deriv > 0.005, 'elapsed']
print(f"T1 last rising time: {rising.iloc[-1]/60:.1f} min")

# C group spread over time: at 10, 20, 30 min
for tmin in [10, 20, 30]:
    idx = (df['elapsed'] - tmin*60).abs().idxmin()
    cvals = [df.loc[idx, c] for c in ['T6','T7','T8','T9']]
    print(f"t={tmin}min: T6={cvals[0]:.1f} T7={cvals[1]:.1f} T8={cvals[2]:.1f} T9={cvals[3]:.1f} | spread={max(cvals)-min(cvals):.1f}")

# B group spread over time
for tmin in [10, 20, 30]:
    idx = (df['elapsed'] - tmin*60).abs().idxmin()
    bvals = [df.loc[idx, c] for c in ['T2','T3','T4','T5']]
    print(f"t={tmin}min: T2={bvals[0]:.1f} T3={bvals[1]:.1f} T4={bvals[2]:.1f} T5={bvals[3]:.1f} | spread={max(bvals)-min(bvals):.1f}")
