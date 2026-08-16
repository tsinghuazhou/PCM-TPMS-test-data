"""
Primitive 30W 实验数据分析
"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def remove_worst_and_avg(df, cols):
    g = df[cols].values
    group_mean = np.mean(g, axis=1)
    sensor_devs = [np.mean(np.abs(g[:, i] - group_mean)) for i in range(len(cols))]
    worst_idx = np.argmax(sensor_devs)
    worst = cols[worst_idx]
    remaining = [c for i, c in enumerate(cols) if i != worst_idx]
    raw_means = np.mean(np.delete(g, worst_idx, axis=1), axis=1)
    return raw_means, worst, remaining

def apply_ema(values, alpha=0.4):
    smoothed = [values[0]]
    for i in range(1, len(values)):
        smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
    return np.array(smoothed)

# Load data
P30 = load('tpms_primitive30w_20260807_193935.csv')
P20 = load('tpms_primitive20w_20260806_214551.csv')  # Run 2
P10 = load('tpms_primitive10w_20260805_200423.csv')

print("=" * 70)
print("Primitive 30W Analysis (2026-08-07)")
print("=" * 70)
print(f"\nDuration: {P30['elapsed'].iloc[-1]/60:.2f} min ({len(P30)} rows)")

# Contact quality check
print("\n=== Contact Quality Check ===")
m2 = P30['elapsed'] <= 120
t1_ema = P30.loc[m2, 'T1'].ewm(alpha=0.4, adjust=False).mean()
b_avg = P30.loc[m2, ['T2','T3','T4','T5']].mean(axis=1).ewm(alpha=0.4, adjust=False).mean()
gap = t1_ema.iloc[-1] - b_avg.iloc[-1]
print(f"T1-B gap (2min EMA): {gap:.1f} C")

m1 = P30['elapsed'] <= 60
t1_rate = (P30.loc[m1, 'T1'].iloc[-1] - P30.loc[m1, 'T1'].iloc[0]) / (60/60)
b_rate = (P30.loc[m1, ['T2','T3','T4','T5']].mean(axis=1).iloc[-1] - 
          P30.loc[m1, ['T2','T3','T4','T5']].mean(axis=1).iloc[0]) / (60/60)
print(f"T1 initial rate (60s): {t1_rate:.1f} C/min")
print(f"B initial rate (60s): {b_rate:.1f} C/min")
print(f"T1/B rate ratio: {t1_rate/b_rate:.1f}x")

# Outlier removal
print("\n=== Outlier Removal ===")
raw_b, worst_b, rem_b = remove_worst_and_avg(P30, ['T2','T3','T4','T5'])
raw_c, worst_c, rem_c = remove_worst_and_avg(P30, ['T6','T7','T8','T9'])
print(f"B-group: removed {worst_b}, kept {rem_b}")
print(f"C-group: removed {worst_c}, kept {rem_c}")

# C-group sensor comparison
print("\n=== C-group Sensor Peaks ===")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: {P30[c].max():.1f} C")

# Peak group values
p_idx = P30['T1'].idxmax()
a_peak = P30['T1'].iloc[p_idx]
b_peak = raw_b[p_idx]
c_peak = raw_c[p_idx]

print(f"\n=== Peak Group Temperatures ===")
print(f"A (T1):       {a_peak:.2f} C")
print(f"B (mid, 3avg): {b_peak:.2f} C")
print(f"C (top, 3avg): {c_peak:.2f} C")
print(f"\nA-B gradient: {a_peak - b_peak:.2f} C")
print(f"A-C gradient: {a_peak - c_peak:.2f} C")
print(f"B-C gradient: {b_peak - c_peak:.2f} C")

# Time to 42C
print(f"\n=== Time to 42C ===")
for name, vals in [('T1', P30['T1']), ('B avg', pd.Series(raw_b)), ('C avg', pd.Series(raw_c))]:
    above = P30.loc[vals >= 42, 'elapsed']
    if len(above) > 0:
        print(f"{name}: {above.iloc[0]:.0f} s ({above.iloc[0]/60:.2f} min)")
    else:
        print(f"{name}: not reached")

# Heating rates
print(f"\n=== Heating Rates (first 3 min) ===")
m3 = P30['elapsed'] <= 180
t1_rate_3 = (P30.loc[m3, 'T1'].ewm(alpha=0.4, adjust=False).mean().iloc[-1] - 
             P30.loc[m3, 'T1'].ewm(alpha=0.4, adjust=False).mean().iloc[0]) / (P30.loc[m3, 'elapsed'].iloc[-1]/60)
b_rate_3 = (apply_ema(raw_b)[m3.values][-1] - apply_ema(raw_b)[m3.values][0]) / (P30.loc[m3, 'elapsed'].iloc[-1]/60)
c_rate_3 = (apply_ema(raw_c)[m3.values][-1] - apply_ema(raw_c)[m3.values][0]) / (P30.loc[m3, 'elapsed'].iloc[-1]/60)
print(f"T1 (A): {t1_rate_3:.2f} C/min")
print(f"B avg:  {b_rate_3:.2f} C/min")
print(f"C avg:  {c_rate_3:.2f} C/min")

# Comparison with 10W and 20W
print(f"\n{'='*70}")
print("COMPARISON: Primitive 10W vs 20W vs 30W")
print(f"{'='*70}")

# Process 10W and 20W
raw_b_10, _, _ = remove_worst_and_avg(P10, ['T2','T3','T4','T5'])
raw_c_10, _, _ = remove_worst_and_avg(P10, ['T6','T7','T8','T9'])
raw_b_20, _, _ = remove_worst_and_avg(P20, ['T2','T3','T4','T5'])
raw_c_20, _, _ = remove_worst_and_avg(P20, ['T6','T7','T8','T9'])

p10_idx = P10['T1'].idxmax()
p20_idx = P20['T1'].idxmax()

a10 = P10['T1'].iloc[p10_idx]
b10 = raw_b_10[p10_idx]
c10 = raw_c_10[p10_idx]

a20 = P20['T1'].iloc[p20_idx]
b20 = raw_b_20[p20_idx]
c20 = raw_c_20[p20_idx]

print(f"\n{'Metric':<20s} {'10W':>12s} {'20W':>12s} {'30W':>12s}")
print("-" * 60)
print(f"{'Duration (min)':<20s} {P10['elapsed'].iloc[-1]/60:>12.2f} {P20['elapsed'].iloc[-1]/60:>12.2f} {P30['elapsed'].iloc[-1]/60:>12.2f}")
print(f"{'A (T1) peak':<20s} {a10:>12.2f} {a20:>12.2f} {a_peak:>12.2f}")
print(f"{'B (mid) peak':<20s} {b10:>12.2f} {b20:>12.2f} {b_peak:>12.2f}")
print(f"{'C (top) peak':<20s} {c10:>12.2f} {c20:>12.2f} {c_peak:>12.2f}")
print(f"{'A-B gradient':<20s} {a10-b10:>12.2f} {a20-b20:>12.2f} {a_peak-b_peak:>12.2f}")
print(f"{'A-C gradient':<20s} {a10-c10:>12.2f} {a20-c20:>12.2f} {a_peak-c_peak:>12.2f}")
print(f"{'B-C gradient':<20s} {b10-c10:>12.2f} {b20-c20:>12.2f} {b_peak-c_peak:>12.2f}")

# Time to 42C comparison
print(f"\n{'Time to 42C (s)':<20s}")
for name, v10, v20, v30 in [
    ('T1', P10['T1'], P20['T1'], P30['T1']),
    ('B avg', pd.Series(raw_b_10), pd.Series(raw_b_20), pd.Series(raw_b)),
    ('C avg', pd.Series(raw_c_10), pd.Series(raw_c_20), pd.Series(raw_c))]:
    t10 = P10.loc[v10 >= 42, 'elapsed'].iloc[0] if len(P10.loc[v10 >= 42, 'elapsed']) > 0 else float('nan')
    t20 = P20.loc[v20 >= 42, 'elapsed'].iloc[0] if len(P20.loc[v20 >= 42, 'elapsed']) > 0 else float('nan')
    t30 = P30.loc[v30 >= 42, 'elapsed'].iloc[0] if len(P30.loc[v30 >= 42, 'elapsed']) > 0 else float('nan')
    print(f"  {name:<10s} {t10:>8.0f} {t20:>8.0f} {t30:>8.0f}")

# Energy analysis
print(f"\n=== Energy Analysis ===")
e10 = 10 * P10['elapsed'].iloc[-1] / 1000
e20 = 20 * P20['elapsed'].iloc[-1] / 1000
e30 = 30 * P30['elapsed'].iloc[-1] / 1000
print(f"Energy input: 10W={e10:.2f} kJ, 20W={e20:.2f} kJ, 30W={e30:.2f} kJ")

t1r10 = a10 - P10['T1'].iloc[0]
t1r20 = a20 - P20['T1'].iloc[0]
t1r30 = a_peak - P30['T1'].iloc[0]
print(f"T1 rise: 10W={t1r10:.1f} C, 20W={t1r20:.1f} C, 30W={t1r30:.1f} C")

print(f"\n{'='*70}")
print("Analysis complete.")
print(f"{'='*70}")
