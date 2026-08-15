"""Gyroid 10W repeat: C group = T9 only (T9 judged best contact)"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

new = load('temperature_record_20260808_165138gyroid10w.csv')
old = load('temperature_record_20260804_163501.csv')

print("=" * 72)
print("C GROUP CONTACT ASSESSMENT - all 4 sensors shown (old vs new)")
print("=" * 72)
for name, df in [('OLD (08-04)', old), ('NEW (08-08)', new)]:
    idx = (df['elapsed'] - 1500).abs().idxmin()  # t=25min
    print(f"\n{name}  @25min:  T1={df['T1'].iloc[idx]:.1f}")
    print(f"  T6={df['T6'].iloc[idx]:.1f}  T7={df['T7'].iloc[idx]:.1f}  T8={df['T8'].iloc[idx]:.1f}  T9={df['T9'].iloc[idx]:.1f}")

# Per-sensor offset from T9 (contact indicator): T9 assumed good
print("\n--- C sensor offset from T9 @25min (T9 as reference, good contact) ---")
for name, df in [('OLD', old), ('NEW', new)]:
    idx = (df['elapsed'] - 1500).abs().idxmin()
    ref = df['T9'].iloc[idx]
    offs = {c: df[c].iloc[idx] - ref for c in ['T6','T7','T8']}
    print(f"{name}: T6={offs['T6']:+.1f}  T7={offs['T7']:+.1f}  T8={offs['T8']:+.1f}  (T9 ref={ref:.1f})")

# Recompute with C = T9 only
print("\n" + "=" * 72)
print("GRADIENTS with C group = T9 only")
print("=" * 72)
for name, df in [('OLD (08-04)', old), ('NEW (08-08)', new)]:
    idx = (df['elapsed'] - 1500).abs().idxmin()
    a = df['T1'].iloc[idx]
    b = df[['T2','T3','T4','T5']].mean(axis=1).iloc[idx]
    # remove worst of B for fairness
    raw_b = df[['T2','T3','T4','T5']].mean(axis=1)
    worst_b = np.abs(df[['T2','T3','T4','T5']].subtract(raw_b, axis=0)).mean(axis=0).idxmax()
    b3 = df[[c for c in ['T2','T3','T4','T5'] if c != worst_b]].mean(axis=1).iloc[idx]
    c9 = df['T9'].iloc[idx]
    print(f"{name} @25min: A={a:.1f}  B3(wo {worst_b})={b3:.1f}  C=T9={c9:.1f}")
    print(f"  A-B = {a-b3:.1f} C | A-C(T9) = {a-c9:.1f} C | B-C(T9) = {b3-c9:.1f} C")
    print(f"  (old C-avg rule was: A-C={a-75.7:.1f} vs now A-C(T9)={a-c9:.1f})")

# T9 time to 42C
print("\n--- T9 (contact-good) vs T1 time to 42C ---")
for name, df in [('OLD', old), ('NEW', new)]:
    t9 = df.loc[df['T9'] >= 42, 'elapsed']
    t1 = df.loc[df['T1'] >= 42, 'elapsed']
    print(f"{name}: T9 -> 42C at {t9.iloc[0]/60 if len(t9)>0 else float('nan'):.1f} min, T1 -> 42C at {t1.iloc[0]/60:.1f} min")

# Contact check all groups: is T9 contact plausible? compare T9 vs B vs T1 at steady-ish point
print("\n--- Overall contact structure @25min (A>T2-5>T9 should hold) ---")
for name, df in [('OLD', old), ('NEW', new)]:
    idx = (df['elapsed'] - 1500).abs().idxmin()
    a = df['T1'].iloc[idx]
    bmax = df.loc[idx, ['T2','T3','T4','T5']].max()
    c9 = df['T9'].iloc[idx]
    print(f"{name}: T1={a:.1f} > Bmax={bmax:.1f} > T9={c9:.1f}  | gaps A-Bmax={a-bmax:.1f}, Bmax-T9={bmax-c9:.1f}")
