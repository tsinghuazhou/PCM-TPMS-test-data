"""Gyroid 10W repeat experiment analysis (2026-08-08)"""
import pandas as pd
import numpy as np

df = pd.read_csv('temperature_record_20260808_165138gyroid10w.csv', encoding='utf-8-sig')
df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
df['time'] = pd.to_datetime(df['time'])
df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()

print("Gyroid 10W (2026-08-08) analysis")
print("=" * 60)
print(f"Rows: {len(df)}, Duration: {df['elapsed'].iloc[-1]/60:.2f} min")
print(f"Sampling: {df['elapsed'].diff().median():.1f} s")

dt = df['elapsed'].diff()
print(f"Gaps >3s: {(dt>3).sum()}, max gap: {dt.max():.1f} s")

# Time to reach 42C (PCM melting) per group
def time_to_42(col):
    idx = df.loc[df[col] >= 42, 'elapsed']
    return idx.iloc[0]/60 if len(idx) > 0 else np.nan

print("\nTime to reach 42C (min):")
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    print(f"  {c}: {time_to_42(c):.1f}")

# Peaks
print("\nPeak temperatures:")
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    print(f"  {c}: {df[c].max():.1f} C at {df['elapsed'].iloc[df[c].idxmax()]/60:.1f} min")

# Group stats at T1 peak (same rule: remove worst sensor of 4, avg remaining 3)
def remove_worst_and_avg(cols):
    raw = df[cols].mean(axis=1)
    worst_idx = np.abs(df[cols].subtract(raw, axis=0)).mean(axis=0).idxmax()
    rem = df[[c for c in cols if c != worst_idx]].mean(axis=1)
    return raw, worst_idx, rem

p_idx = df['T1'].idxmax()
raw_b, worst_b, rem_b = remove_worst_and_avg(['T2','T3','T4','T5'])
raw_c, worst_c, rem_c = remove_worst_and_avg(['T6','T7','T8','T9'])

a_peak = df['T1'].iloc[p_idx]
b_at_peak = rem_b.iloc[p_idx]
c_at_peak = rem_c.iloc[p_idx]

print("\nAt T1 peak (%.1f C, %.1f min):" % (a_peak, df['elapsed'].iloc[p_idx]/60))
print(f"  B avg (removed {worst_b}): {b_at_peak:.2f} C  | raw: {raw_b.iloc[p_idx]:.2f}")
print(f"  C avg (removed {worst_c}): {c_at_peak:.2f} C  | raw: {raw_c.iloc[p_idx]:.2f}")
print(f"  A-B gradient: {a_peak - b_at_peak:.2f} C")
print(f"  A-C gradient: {a_peak - c_at_peak:.2f} C")
print(f"  B-C gradient: {b_at_peak - c_at_peak:.2f} C")

# Heating rates (first 5 min)
m1 = df['elapsed'] <= 300
t1_rate = (df.loc[m1,'T1'].iloc[-1] - df.loc[m1,'T1'].iloc[0]) / 5
b_rate = (rem_b[m1.values].iloc[-1] - rem_b[m1.values].iloc[0]) / 5
c_rate = (rem_c[m1.values].iloc[-1] - rem_c[m1.values].iloc[0]) / 5
print("\nHeating rates first 5 min (C/min):")
print(f"  T1: {t1_rate:.2f}, B: {b_rate:.2f}, C: {c_rate:.2f}")

# Contact check: T1 vs B gap
print(f"\nT1-B gap at peak: {a_peak - b_at_peak:.2f} C (contact quality indicator)")

# Energy
e = 10 * df['elapsed'].iloc[-1] / 1000
print(f"Energy input: {e:.2f} kJ (10W x {df['elapsed'].iloc[-1]/60:.1f} min)")

# C group individual spread at T1 peak
print("\nC group individual temps at T1 peak:")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: {df[c].iloc[p_idx]:.2f} C")
