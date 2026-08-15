"""Gyroid 20W NEW analysis (2026-08-08)
- Compare with old Gyroid 20W (2026-07-31, marked invalid)
- Phase-change window (42-52C) analysis
- C group = T9 only (best contact)
"""
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

def b3_avg(df):
    raw = df[['T2','T3','T4','T5']].mean(axis=1)
    worst = np.abs(df[['T2','T3','T4','T5']].subtract(raw, axis=0)).mean(axis=0).idxmax()
    return df[[c for c in ['T2','T3','T4','T5'] if c != worst]].mean(axis=1), worst

g20_new = load('temperature_record_20260808_190451 (4).csv')
g20_old = load('temperature_record_20260731_195755.csv')

b_new, wo_new = b3_avg(g20_new)
b_old, wo_old = b3_avg(g20_old)

print("=" * 76)
print("GYROID 20W: NEW vs OLD comparison")
print("=" * 76)

print(f"\n[Data summary]")
print(f"NEW: {len(g20_new)} rows, {g20_new.elapsed.iloc[-1]/60:.2f} min, T1 end={g20_new.T1.iloc[-1]:.1f}C")
print(f"OLD: {len(g20_old)} rows, {g20_old.elapsed.iloc[-1]/60:.2f} min, T1 end={g20_old.T1.iloc[-1]:.1f}C")

print(f"\n[B group worst removed]")
print(f"NEW: {wo_new} (spread at end: {g20_new[['T2','T3','T4','T5']].iloc[-1].max() - g20_new[['T2','T3','T4','T5']].iloc[-1].min():.1f}C)")
print(f"OLD: {wo_old} (spread at end: {g20_old[['T2','T3','T4','T5']].iloc[-1].max() - g20_old[['T2','T3','T4','T5']].iloc[-1].min():.1f}C)")

print(f"\n[C group contact check at T1=45C]")
for name, df in [('NEW', g20_new), ('OLD', g20_old)]:
    i = df.T1.sub(45).abs().idxmin()
    ref = df.T9.iloc[i]
    offs = {c: df[c].iloc[i] - ref for c in ['T6','T7','T8']}
    print(f"  {name}: T6={offs['T6']:+.1f} T7={offs['T7']:+.1f} T8={offs['T8']:+.1f} (T9 ref={ref:.1f})")

print(f"\n[1] A-B gradient vs T1 (melting window)")
print(f"{'T1 (C)':>8} | {'NEW A-B':>10} | {'OLD A-B':>10}")
for t1 in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    row = []
    for df, b in [(g20_new, b_new), (g20_old, b_old)]:
        i = df.T1.sub(t1).abs().idxmin()
        row.append(df.T1.iloc[i] - b.iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>10.1f}")

print(f"\n[2] A-C gradient (C=T9) vs T1 (melting window)")
print(f"{'T1 (C)':>8} | {'NEW A-C':>10} | {'OLD A-C':>10}")
for t1 in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    row = []
    for df, b in [(g20_new, b_new), (g20_old, b_old)]:
        i = df.T1.sub(t1).abs().idxmin()
        row.append(df.T1.iloc[i] - df.T9.iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>10.1f}")

print(f"\n[3] Time to 42C (min)")
print(f"{'sensor':>8} | {'NEW':>10} | {'OLD':>10}")
for c in ['T1','T2','T3','T4','T5','T9']:
    row = []
    for df in [g20_new, g20_old]:
        idx = df.loc[df[c] >= 42, 'elapsed']
        row.append(idx.iloc[0]/60 if len(idx) > 0 else np.nan)
    print(f"{c:>8} | {row[0]:>10.1f} | {row[1]:>10.1f}")

print(f"\n[4] Melting duration (T1 in 42-52C)")
for name, df, b in [('NEW', g20_new, b_new), ('OLD', g20_old, b_old)]:
    win = df.elapsed.loc[(df.T1 >= 42) & (df.T1 <= 52)]
    dur = win.iloc[-1] - win.iloc[0] if len(win) > 0 else np.nan
    print(f"  {name}: {dur/60:.1f} min")

# Figure
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Panel 1: A-B gradient vs T1
ax = axes[0]
for df, b, lab, col in [(g20_new, b_new, 'NEW', '#1F77B4'), (g20_old, b_old, 'OLD', '#C44E52')]:
    ab = df.T1 - b
    mask = (df.T1 >= 38) & (df.T1 <= 60)
    ax.plot(df.loc[mask, 'T1'], ab[mask], '-', lw=2, color=col, label=lab)
ax.axvspan(42, 52, color='gray', alpha=0.2)
ax.axvline(42, color='k', ls=':', lw=0.8)
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B gradient (°C)')
ax.set_title('A-B gradient vs T1\n(phase-change window shaded)')
ax.legend(); ax.grid(alpha=0.3)

# Panel 2: A-C gradient vs T1
ax = axes[1]
for df, b, lab, col in [(g20_new, b_new, 'NEW', '#1F77B4'), (g20_old, b_old, 'OLD', '#C44E52')]:
    ac = df.T1 - df.T9
    mask = (df.T1 >= 38) & (df.T1 <= 60)
    ax.plot(df.loc[mask, 'T1'], ac[mask], '-', lw=2, color=col, label=lab)
ax.axvspan(42, 52, color='gray', alpha=0.2)
ax.axvline(42, color='k', ls=':', lw=0.8)
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C gradient (°C)')
ax.set_title('A-C gradient vs T1 (C = T9)')
ax.legend(); ax.grid(alpha=0.3)

# Panel 3: time to 42C per sensor
ax = axes[2]
labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T9']
x = np.arange(len(labels))
w = 0.35
for j, (df, lab, col) in enumerate([(g20_new, 'NEW', '#1F77B4'), (g20_old, 'OLD', '#C44E52')]):
    times = []
    for c in labels:
        idx = df.loc[df[c] >= 42, 'elapsed']
        times.append(idx.iloc[0]/60 if len(idx) > 0 else np.nan)
    ax.bar(x + (j-0.5)*w, times, w, color=col, label=lab, edgecolor='k', lw=0.5)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel('Time to 42°C (min)')
ax.set_title('Time to reach melting (42°C)')
ax.legend(); ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_20w_new_vs_old.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_20w_new_vs_old.pdf', bbox_inches='tight')
print("\nSaved: gyroid_20w_new_vs_old.png/pdf")
