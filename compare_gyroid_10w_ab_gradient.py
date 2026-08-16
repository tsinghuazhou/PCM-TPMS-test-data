"""Gyroid 10W old (08-04) vs new (08-08): A-B gradient around phase change (42C)"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def b3_avg(df, cols=('T2','T3','T4','T5')):
    raw = df[list(cols)].mean(axis=1)
    worst = np.abs(df[list(cols)].subtract(raw, axis=0)).mean(axis=0).idxmax()
    return df[[c for c in cols if c != worst]].mean(axis=1), worst

old = load('tpms_gyroid10w_20260804_163501.csv')
new = load('tpms_gyroid10w_20260808_165138.csv')

b_old, wo_old = b3_avg(old)
b_new, wo_new = b3_avg(new)

print("=" * 70)
print("A-B GRADIENT COMPARISON: old Gyroid 10W (08-04) vs new (08-08)")
print("=" * 70)

# Key moments: T1 reaches 42C (melting start at heater), and B group reaches 42C
for name, df, b in [('OLD (08-04)', old, b_old), ('NEW (08-08)', new, b_new)]:
    print(f"\n--- {name} ---")
    # T1 = 42C
    i1 = (df['T1'] - 42).abs().idxmin()
    print(f"  T1=42C: t={df['elapsed'].iloc[i1]/60:.1f}min, A={df['T1'].iloc[i1]:.1f}, B={b.iloc[i1]:.1f}, A-B={df['T1'].iloc[i1]-b.iloc[i1]:+.1f}")
    # B = 42C
    i2 = (b - 42).abs().idxmin()
    print(f"  B=42C:  t={df['elapsed'].iloc[i2]/60:.1f}min, A={df['T1'].iloc[i2]:.1f}, B={b.iloc[i2]:.1f}, A-B={df['T1'].iloc[i2]-b.iloc[i2]:+.1f}")
    # mid-melting: T1 = 50C (just above melting)
    i3 = (df['T1'] - 50).abs().idxmin()
    print(f"  T1=50C: t={df['elapsed'].iloc[i3]/60:.1f}min, A={df['T1'].iloc[i3]:.1f}, B={b.iloc[i3]:.1f}, A-B={df['T1'].iloc[i3]-b.iloc[i3]:+.1f}")
    # T1 = 60C
    i4 = (df['T1'] - 60).abs().idxmin()
    print(f"  T1=60C: t={df['elapsed'].iloc[i4]/60:.1f}min, A={df['T1'].iloc[i4]:.1f}, B={b.iloc[i4]:.1f}, A-B={df['T1'].iloc[i4]-b.iloc[i4]:+.1f}")
    # end of record
    i5 = df['elapsed'].idxmax()
    print(f"  END:    t={df['elapsed'].iloc[i5]/60:.1f}min, A={df['T1'].iloc[i5]:.1f}, B={b.iloc[i5]:.1f}, A-B={df['T1'].iloc[i5]-b.iloc[i5]:+.1f}")

# A-B gradient evolution around melting (T1 from 38 to 55C)
print("\n--- A-B gradient vs T1 (melting window 38-55C) ---")
print(f"{'T1 (C)':>8} | {'OLD A-B':>10} | {'NEW A-B':>10}")
for t1 in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    r1 = [old['T1'].sub(t1).abs().idxmin(), new['T1'].sub(t1).abs().idxmin()]
    ab1 = old['T1'].iloc[r1[0]] - b_old.iloc[r1[0]]
    ab2 = new['T1'].iloc[r1[1]] - b_new.iloc[r1[1]]
    print(f"{t1:>8} | {ab1:>10.1f} | {ab2:>10.1f}")

# Phase change duration: time spent in 42-52C window (per T1 and per B)
print("\n--- Time in melting window 42-52C (T1) ---")
for name, df in [('OLD', old), ('NEW', new)]:
    win = df['elapsed'].loc[(df['T1'] >= 42) & (df['T1'] <= 52)]
    dur = win.iloc[-1] - win.iloc[0] if len(win) > 0 else np.nan
    print(f"  {name}: {dur/60:.1f} min")

# Also old vs new at same elapsed time (15 min, 20 min, 25 min)
print("\n--- A-B gradient at fixed times ---")
print(f"{'t (min)':>8} | {'OLD A-B':>10} | {'NEW A-B':>10}")
for tm in [10, 15, 20, 25]:
    i_old = (old['elapsed'] - tm*60).abs().idxmin()
    i_new = (new['elapsed'] - tm*60).abs().idxmin()
    print(f"{tm:>8} | {old['T1'].iloc[i_old]-b_old.iloc[i_old]:>10.1f} | {new['T1'].iloc[i_new]-b_new.iloc[i_new]:>10.1f}")
