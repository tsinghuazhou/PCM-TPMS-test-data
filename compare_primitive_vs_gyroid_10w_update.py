"""Primitive vs Gyroid 10W: updated comparison in phase-change window (42-52C)
- Primitive 10W (2026-08-05, trimmed)
- Gyroid 10W old (2026-08-04)
- Gyroid 10W new (2026-08-08, C group only T9 reliable)
Rule: C group = T9 only (best contact); B group = remove worst of T2-T5, avg rest.
Focus: phase-change window T1 in [42, 52]C — above 42C only sensible window.
"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def b3_avg(df):
    raw = df[['T2','T3','T4','T5']].mean(axis=1)
    worst = np.abs(df[['T2','T3','T4','T5']].subtract(raw, axis=0)).mean(axis=0).idxmax()
    return df[[c for c in ['T2','T3','T4','T5'] if c != worst]].mean(axis=1), worst

prim = load('temperature_record_20260805_200423.csv')
gyro_old = load('temperature_record_20260804_163501.csv')
gyro_new = load('temperature_record_20260808_165138gyroid10w.csv')

b_prim, wo_p = b3_avg(prim)
b_gold, wo_go = b3_avg(gyro_old)
b_gnew, wo_gn = b3_avg(gyro_new)

datasets = [
    ('Primitive 10W (08-05)', prim, b_prim),
    ('Gyroid 10W OLD (08-04)', gyro_old, b_gold),
    ('Gyroid 10W NEW (08-08)', gyro_new, b_gnew),
]

print("=" * 76)
print("PRIMITIVE vs GYROID 10W — phase-change window comparison")
print("C group = T9 only (best-contact rule); B = worst-of-4 removed, avg 3")
print("=" * 76)

# 1. A-B gradient vs T1 across melting window
print("\n[1] A-B gradient vs T1 (melting window)")
print(f"{'T1 (C)':>8} | {'Prim A-B':>10} | {'GyroOLD A-B':>12} | {'GyroNEW A-B':>12}")
for t1 in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    row = []
    for name, df, b in datasets:
        i = df['T1'].sub(t1).abs().idxmin()
        row.append(df['T1'].iloc[i] - b.iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>12.1f} | {row[2]:>12.1f}")

# 2. A-C(T9) gradient vs T1
print("\n[2] A-C gradient (C=T9) vs T1 (melting window)")
print(f"{'T1 (C)':>8} | {'Prim A-C':>10} | {'GyroOLD A-C':>12} | {'GyroNEW A-C':>12}")
for t1 in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    row = []
    for name, df, b in datasets:
        i = df['T1'].sub(t1).abs().idxmin()
        row.append(df['T1'].iloc[i] - df['T9'].iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>12.1f} | {row[2]:>12.1f}")

# 3. Time to reach 42C (T1, B, T9)
print("\n[3] Time to 42C (min)")
print(f"{'sensor':>8} | {'Prim':>10} | {'GyroOLD':>10} | {'GyroNEW':>10}")
for c in ['T1','T2','T3','T4','T5','T9']:
    row = []
    for name, df, b in datasets:
        idx = df.loc[df[c] >= 42, 'elapsed']
        row.append(idx.iloc[0]/60 if len(idx) > 0 else np.nan)
    print(f"{c:>8} | {row[0]:>10.1f} | {row[1]:>10.1f} | {row[2]:>10.1f}")

# 4. B-group spread at T1=45C (mid melting)
print("\n[4] B-group (T2-T5) spread at T1=45C")
for name, df, b in datasets:
    i = df['T1'].sub(45).abs().idxmin()
    vals = [df.loc[i, c] for c in ['T2','T3','T4','T5']]
    print(f"  {name}: spread={max(vals)-min(vals):.1f} C  (worst removed: {b.name if hasattr(b,'name') else ''})")

# 5. Phase change duration (T1 in 42-52C)
print("\n[5] Melting duration (T1 in 42-52C)")
for name, df, b in datasets:
    win = df['elapsed'].loc[(df['T1'] >= 42) & (df['T1'] <= 52)]
    dur = win.iloc[-1] - win.iloc[0] if len(win) > 0 else np.nan
    print(f"  {name}: {dur/60:.1f} min")

# 6. A-B gradient at B=42C (B reaches melting)
print("\n[6] A-B gradient when B reaches 42C")
for name, df, b in datasets:
    i = b.sub(42).abs().idxmin()
    print(f"  {name}: A-B={df['T1'].iloc[i]-b.iloc[i]:.1f} C  (A={df['T1'].iloc[i]:.1f}, t={df['elapsed'].iloc[i]/60:.1f}min)")

# 7. C group contact structure per dataset (T9 reference at T1=45C)
print("\n[7] C-group contact check (offset from T9, at T1=45C)")
for name, df, b in datasets:
    i = df['T1'].sub(45).abs().idxmin()
    ref = df['T9'].iloc[i]
    offs = {c: df[c].iloc[i] - ref for c in ['T6','T7','T8']}
    print(f"  {name}: T6={offs['T6']:+.1f} T7={offs['T7']:+.1f} T8={offs['T8']:+.1f} (T9 ref={ref:.1f})")
