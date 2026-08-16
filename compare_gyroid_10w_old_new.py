"""Gyroid 10W repeat (2026-08-08) formal analysis + comparison with 2026-08-04 run"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def remove_worst_and_avg(df, cols):
    raw = df[cols].mean(axis=1)
    worst = np.abs(df[cols].subtract(raw, axis=0)).mean(axis=0).idxmax()
    rem = df[[c for c in cols if c != worst]].mean(axis=1)
    return raw, worst, rem

new = load('tpms_gyroid10w_20260808_165138.csv')
old = load('tpms_gyroid10w_20260804_163501.csv')

print("=" * 70)
print("COMPARISON: Gyroid 10W old (08-04) vs new (08-08)")
print("=" * 70)

for name, df in [('OLD (08-04)', old), ('NEW (08-08)', new)]:
    print(f"\n--- {name}: {len(df)} rows, {df['elapsed'].iloc[-1]/60:.2f} min ---")
    # T1 still rising at end?
    slope = df.loc[df['elapsed'] >= df['elapsed'].max()-120, 'T1'].diff().mean()
    print(f"  T1 slope last 2 min: {slope*60:+.2f} C/min (heating {'ON' if slope > 0.5 else 'OFF/steady'})")
    print(f"  T1 final: {df['T1'].iloc[-1]:.1f} C")
    # at 25 min
    idx25 = (df['elapsed'] - 1500).abs().idxmin()
    print(f"  At 25.0 min: T1={df['T1'].iloc[idx25]:.1f}")

    raw_b, worst_b, rem_b = remove_worst_and_avg(df, ['T2','T3','T4','T5'])
    raw_c, worst_c, rem_c = remove_worst_and_avg(df, ['T6','T7','T8','T9'])
    # at 25 min (comparable point)
    print(f"  At 25 min: A={df['T1'].iloc[idx25]:.1f} B(wo {worst_b})={rem_b.iloc[idx25]:.1f} C(wo {worst_c})={rem_c.iloc[idx25]:.1f}")
    print(f"    A-B={df['T1'].iloc[idx25]-rem_b.iloc[idx25]:.1f}  A-C={df['T1'].iloc[idx25]-rem_c.iloc[idx25]:.1f}  B-C={rem_b.iloc[idx25]-rem_c.iloc[idx25]:.1f}")
    print(f"  B spread@25min: {max(df.loc[idx25,['T2','T3','T4','T5']])-min(df.loc[idx25,['T2','T3','T4','T5']]):.1f}")
    print(f"  C spread@25min: {max(df.loc[idx25,['T6','T7','T8','T9']])-min(df.loc[idx25,['T6','T7','T8','T9']]):.1f} (worst={worst_c})")

# time to 42C
print("\n--- Time to 42C (melting) ---")
for name, df in [('OLD', old), ('NEW', new)]:
    row = []
    for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
        idx = df.loc[df[c] >= 42, 'elapsed']
        row.append(f"{c}:{idx.iloc[0]/60 if len(idx)>0 else float('nan'):.1f}")
    print(f"{name}: " + " ".join(row))

# FIGURE: overlay curves
fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))

colors = {'T1': '#C44E52', 'T2': '#1F77B4', 'T3': '#1F77B4', 'T4': '#1F77B4', 'T5': '#1F77B4',
          'T6': '#2CA02C', 'T7': '#2CA02C', 'T8': '#2CA02C', 'T9': '#2CA02C'}

# Panel 1: T1 comparison
ax = axes[0]
ax.plot(old['elapsed']/60, old['T1'], '-', color='#888888', lw=1.2, label='OLD T1 (08-04)')
ax.plot(new['elapsed']/60, new['T1'], '-', color='#C44E52', lw=1.5, label='NEW T1 (08-08)')
ax.set_xlabel('Time (min)'); ax.set_ylabel('T (°C)')
ax.set_title('T1 (bottom center)'); ax.legend(fontsize=8)
ax.axhline(42, color='k', ls=':', lw=0.8)

# Panel 2: B group averages
ax = axes[1]
old_b = old[['T2','T3','T4','T5']].mean(axis=1)
new_b = new[['T2','T3','T4','T5']].mean(axis=1)
ax.plot(old['elapsed']/60, old_b, '-', color='#888888', lw=1.2, label='OLD B (08-04)')
ax.plot(new['elapsed']/60, new_b, '-', color='#1F77B4', lw=1.5, label='NEW B (08-08)')
ax.set_xlabel('Time (min)'); ax.set_ylabel('T (°C)')
ax.set_title('B group avg (mid-layer)'); ax.legend(fontsize=8)
ax.axhline(42, color='k', ls=':', lw=0.8)

# Panel 3: C group members NEW (show all 4, highlight T7)
ax = axes[2]
for c in ['T6','T7','T8','T9']:
    ax.plot(new['elapsed']/60, new[c], '-', color=colors[c], lw=1.0, alpha=0.85, label=f'NEW {c}')
ax.set_xlabel('Time (min)'); ax.set_ylabel('T (°C)')
ax.set_title('C group sensors (top surface, NEW)'); ax.legend(fontsize=8)
ax.axhline(42, color='k', ls=':', lw=0.8)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_10w_repeat_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_10w_repeat_comparison.pdf', bbox_inches='tight')
print("\nSaved: gyroid_10w_repeat_comparison.png/pdf")
