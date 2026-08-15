"""Primitive vs Gyroid 10W updated comparison figure (phase-change window)"""
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
    return df[[c for c in ['T2','T3','T4','T5'] if c != worst]].mean(axis=1)

prim = load('temperature_record_20260805_200423.csv')
gold = load('temperature_record_20260804_163501.csv')
gnew = load('temperature_record_20260808_165138gyroid10w.csv')

b_prim, b_gold, b_gnew = b3_avg(prim), b3_avg(gold), b3_avg(gnew)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Panel 1: A-B gradient vs T1 in melting window
ax = axes[0]
for df, b, lab, col in [(prim, b_prim, 'Primitive', '#C44E52'),
                         (gold, b_gold, 'Gyroid OLD', '#2CA02C'),
                         (gnew, b_gnew, 'Gyroid NEW', '#1F77B4')]:
    # A-B as function of T1
    ab = df['T1'] - b
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], ab[mask], '-', lw=2, color=col, label=lab)
ax.axvspan(42, 52, color='gray', alpha=0.2, label='melting window')
ax.axvline(42, color='k', ls=':', lw=0.8)
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B gradient (°C)')
ax.set_title('A-B gradient vs T1\n(phase-change window shaded)')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Panel 2: A-C gradient vs T1 (C=T9)
ax = axes[1]
for df, b, lab, col in [(prim, b_prim, 'Primitive', '#C44E52'),
                         (gold, b_gold, 'Gyroid OLD', '#2CA02C'),
                         (gnew, b_gnew, 'Gyroid NEW', '#1F77B4')]:
    ac = df['T1'] - df['T9']
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], ac[mask], '-', lw=2, color=col, label=lab)
ax.axvspan(42, 52, color='gray', alpha=0.2)
ax.axvline(42, color='k', ls=':', lw=0.8)
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C gradient (°C)')
ax.set_title('A-C gradient vs T1 (C = T9)\n(phase-change window shaded)')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Panel 3: time to 42C per sensor
ax = axes[2]
labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T9']
x = np.arange(len(labels))
w = 0.27
for j, (df, lab, col) in enumerate([(prim, 'Prim', '#C44E52'), (gold, 'Gyro OLD', '#2CA02C'), (gnew, 'Gyro NEW', '#1F77B4')]):
    times = []
    for c in labels:
        idx = df.loc[df[c] >= 42, 'elapsed']
        times.append(idx.iloc[0]/60 if len(idx) > 0 else np.nan)
    ax.bar(x + (j-1)*w, times, w, color=col, label=lab, edgecolor='k', lw=0.5)
ax.axhline(12, color='gray', ls='--', lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel('Time to 42°C (min)')
ax.set_title('Time to reach melting (42°C)')
ax.legend(fontsize=8); ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_vs_gyroid_10w_update.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_vs_gyroid_10w_update.pdf', bbox_inches='tight')
print("Saved: primitive_vs_gyroid_10w_update.png/pdf")
