import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def remove_worst_and_avg(df, cols):
    g = df[cols].values
    group_mean = np.mean(g, axis=1)
    sensor_devs = []
    for i in range(len(cols)):
        dev = np.mean(np.abs(g[:, i] - group_mean))
        sensor_devs.append(dev)
    worst_idx = np.argmax(sensor_devs)
    worst = cols[worst_idx]
    remaining = [c for i, c in enumerate(cols) if i != worst_idx]
    raw_means = np.mean(np.delete(g, worst_idx, axis=1), axis=1)
    return raw_means, worst, remaining

G = load('temperature_record_20260804_163501.csv')
P = load('temperature_record_20260805_200423.csv')

EMA = 0.4
for df in [G, P]:
    for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
        df[f'{c}_ema'] = df[c].ewm(alpha=EMA, adjust=False).mean()

raw_b_g, worst_b_g, rem_b_g = remove_worst_and_avg(G, ['T2','T3','T4','T5'])
smooth_b_g = pd.Series(raw_b_g).ewm(alpha=EMA, adjust=False).mean().values
raw_c_g, worst_c_g, rem_c_g = remove_worst_and_avg(G, ['T6','T7','T8','T9'])
smooth_c_g = pd.Series(raw_c_g).ewm(alpha=EMA, adjust=False).mean().values

raw_b_p, worst_b_p, rem_b_p = remove_worst_and_avg(P, ['T2','T3','T4','T5'])
smooth_b_p = pd.Series(raw_b_p).ewm(alpha=EMA, adjust=False).mean().values
raw_c_p, worst_c_p, rem_c_p = remove_worst_and_avg(P, ['T6','T7','T8','T9'])
smooth_c_p = pd.Series(raw_c_p).ewm(alpha=EMA, adjust=False).mean().values

# Figure 1: Group temperature comparison (corrected)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# A group (T1)
ax = axes[0]
ax.plot(G['elapsed']/60, G['T1_ema'], 'r-', linewidth=2, label='Gyroid T1', alpha=0.8)
ax.plot(P['elapsed']/60, P['T1_ema'], 'r--', linewidth=2, label='Primitive T1', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5, label='PCM melting (42°C)')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('A Group (Heater Contact) — T1', fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.annotate(f'Gyroid: {G["T1"].max():.1f}°C', xy=(22, 95), fontsize=9, color='red')
ax.annotate(f'Primitive: {P["T1"].max():.1f}°C', xy=(22, 103), fontsize=9, color='red')

# B group (mid layer, corrected)
ax = axes[1]
ax.plot(G['elapsed']/60, smooth_b_g, 'b-', linewidth=2, label=f'Gyroid B (no {worst_b_g})', alpha=0.8)
ax.plot(P['elapsed']/60, smooth_b_p, 'b--', linewidth=2, label=f'Primitive B (no {worst_b_p})', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('B Group (Mid Layer) — avg of 3', fontweight='bold')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)

g_b_peak = smooth_b_g[G['T1'].idxmax()]
p_b_peak = smooth_b_p[P['T1'].idxmax()]
ax.annotate(f'Gyroid: {g_b_peak:.1f}°C', xy=(22, 88), fontsize=9, color='blue')
ax.annotate(f'Primitive: {p_b_peak:.1f}°C', xy=(22, 93), fontsize=9, color='blue')

# C group (top layer, corrected)
ax = axes[2]
ax.plot(G['elapsed']/60, smooth_c_g, 'g-', linewidth=2, label=f'Gyroid C (no {worst_c_g})', alpha=0.8)
ax.plot(P['elapsed']/60, smooth_c_p, 'g--', linewidth=2, label=f'Primitive C (no {worst_c_p})', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('C Group (Top Surface) — avg of 3', fontweight='bold')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)

g_c_peak = smooth_c_g[G['T1'].idxmax()]
p_c_peak = smooth_c_p[P['T1'].idxmax()]
ax.annotate(f'Gyroid: {g_c_peak:.1f}°C', xy=(22, 77), fontsize=9, color='green')
ax.annotate(f'Primitive: {p_c_peak:.1f}°C', xy=(22, 70), fontsize=9, color='green')

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_corrected_groups.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_corrected_groups.pdf', bbox_inches='tight')
print("Saved: fig_compare_corrected_groups.png/pdf")

# Figure 2: Temperature gradients over time
fig2, ax = plt.subplots(figsize=(12, 6))

g_ab = G['T1_ema'] - smooth_b_g
g_ac = G['T1_ema'] - smooth_c_g
p_ab = P['T1_ema'] - smooth_b_p
p_ac = P['T1_ema'] - smooth_c_p

ax.plot(G['elapsed']/60, g_ab, 'b-', linewidth=2, label='Gyroid A-B', alpha=0.8)
ax.plot(P['elapsed']/60, p_ab, 'b--', linewidth=2, label='Primitive A-B', alpha=0.8)
ax.plot(G['elapsed']/60, g_ac, 'r-', linewidth=2, label='Gyroid A-C', alpha=0.8)
ax.plot(P['elapsed']/60, p_ac, 'r--', linewidth=2, label='Primitive A-C', alpha=0.8)

ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature Gradient (°C)', fontsize=11)
ax.set_title('Thermal Gradients — Corrected Statistics\n(A=heater, B=mid layer, C=top surface)', fontsize=12, fontweight='bold')
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(0, 45)

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_corrected_gradients.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_corrected_gradients.pdf', bbox_inches='tight')
print("Saved: fig_compare_corrected_gradients.png/pdf")

# Figure 3: T7 anomaly and C-group detail
fig3, axes = plt.subplots(1, 2, figsize=(14, 5))

# T7 comparison
ax = axes[0]
ax.plot(G['elapsed']/60, G['T7_ema'], 'm-', linewidth=2, label='Gyroid T7', alpha=0.8)
ax.plot(P['elapsed']/60, P['T7_ema'], 'm--', linewidth=2, label='Primitive T7', alpha=0.8)
ax.plot(G['elapsed']/60, smooth_c_g, 'g:', linewidth=1.5, label='Gyroid C avg (no T6)', alpha=0.6)
ax.plot(P['elapsed']/60, smooth_c_p, 'g--', linewidth=1.5, label='Primitive C avg (no T7)', alpha=0.6)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.3)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('T7 Anomaly — Primitive vs Gyroid', fontweight='bold')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(20, 80)
ax.annotate(f'Gyroid T7: {G["T7"].max():.1f}°C', xy=(15, 76), fontsize=9, color='magenta')
ax.annotate(f'Primitive T7: {P["T7"].max():.1f}°C', xy=(15, 50), fontsize=9, color='magenta')

# C-group sensor detail at peak
ax = axes[1]
g_idx = G['T1'].idxmax()
p_idx = P['T1'].idxmax()
g_c_vals = [G[c].iloc[g_idx] for c in ['T6','T7','T8','T9']]
p_c_vals = [P[c].iloc[p_idx] for c in ['T6','T7','T8','T9']]

x = np.arange(4)
width = 0.35
bars1 = ax.bar(x - width/2, g_c_vals, width, label='Gyroid', color='#4CAF50', edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, p_c_vals, width, label='Primitive', color='#FF9800', edgecolor='black', linewidth=0.5)

ax.set_xlabel('Sensor')
ax.set_ylabel('Peak Temperature (°C)')
ax.set_title('C-Group (Top Surface) — Peak Temperatures', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['T6', 'T7', 'T8', 'T9'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 80)

# Highlight outliers
ax.axhline(y=50, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax.annotate('T7 outlier\n(Primitive)', xy=(1 + width/2, 48.33), xytext=(1.5, 55),
           fontsize=9, color='red', ha='center',
           arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax.annotate('T6 outlier\n(Gyroid)', xy=(0 - width/2, 52.74), xytext=(0.5, 58),
           fontsize=9, color='red', ha='center',
           arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_corrected_t7.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_corrected_t7.pdf', bbox_inches='tight')
print("Saved: fig_compare_corrected_t7.png/pdf")

print("\n=== Summary (Corrected Statistics) ===")
print(f"Outlier removal:")
print(f"  Gyroid:    B removed {worst_b_g}, C removed {worst_c_g}")
print(f"  Primitive: B removed {worst_b_p}, C removed {worst_c_p}")
print(f"\nPeak group averages:")
print(f"  A (T1):      Gyroid={G['T1'].max():.2f}°C  Primitive={P['T1'].max():.2f}°C  Δ={P['T1'].max()-G['T1'].max():+.2f}°C")
print(f"  B (mid):     Gyroid={g_b_peak:.2f}°C  Primitive={p_b_peak:.2f}°C  Δ={p_b_peak-g_b_peak:+.2f}°C")
print(f"  C (top):     Gyroid={g_c_peak:.2f}°C  Primitive={p_c_peak:.2f}°C  Δ={p_c_peak-g_c_peak:+.2f}°C")
print(f"\nTemperature gradients at T1 peak:")
print(f"  A-B:  Gyroid={G['T1'].iloc[g_idx]-g_b_peak:.2f}°C  Primitive={P['T1'].iloc[p_idx]-p_b_peak:.2f}°C  ratio={(P['T1'].iloc[p_idx]-p_b_peak)/(G['T1'].iloc[g_idx]-g_b_peak):.2f}x")
print(f"  A-C:  Gyroid={G['T1'].iloc[g_idx]-g_c_peak:.2f}°C  Primitive={P['T1'].iloc[p_idx]-p_c_peak:.2f}°C  ratio={(P['T1'].iloc[p_idx]-p_c_peak)/(G['T1'].iloc[g_idx]-g_c_peak):.2f}x")
print(f"  B-C:  Gyroid={g_b_peak-g_c_peak:.2f}°C  Primitive={p_b_peak-p_c_peak:.2f}°C  ratio={(p_b_peak-p_c_peak)/(g_b_peak-g_c_peak):.2f}x")
