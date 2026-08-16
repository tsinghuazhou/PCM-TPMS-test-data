import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

G = load('tpms_gyroid10w_20260804_163501.csv')
P = load('tpms_primitive10w_20260805_200423.csv')

EMA = 0.4
for df in [G, P]:
    for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
        df[f'{c}_ema'] = df[c].ewm(alpha=EMA, adjust=False).mean()

groups = {'A': ['T1'], 'B': ['T2','T3','T4','T5'], 'C': ['T6','T7','T8','T9']}

# Compute group averages
for df in [G, P]:
    for gname, cols in groups.items():
        df[f'{gname}_avg'] = df[cols].mean(axis=1)
        df[f'{gname}_avg_ema'] = df[f'{gname}_avg'].ewm(alpha=EMA, adjust=False).mean()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# --- Plot 1: Group A comparison ---
ax = axes[0, 0]
ax.plot(G['elapsed']/60, G['T1_ema'], 'r-', linewidth=2, label='Gyroid T1', alpha=0.8)
ax.plot(P['elapsed']/60, P['T1_ema'], 'r--', linewidth=2, label='Primitive T1', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Group A (Heater Zone) — T1', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(20, 110)
ax.annotate(f'Gyroid peak: {G["T1"].max():.1f}°C', xy=(20, 95), fontsize=9, color='red')
ax.annotate(f'Primitive peak: {P["T1"].max():.1f}°C', xy=(20, 103), fontsize=9, color='red')

# --- Plot 2: Group B comparison ---
ax = axes[0, 1]
ax.plot(G['elapsed']/60, G['B_avg_ema'], 'b-', linewidth=2, label='Gyroid B avg', alpha=0.8)
ax.plot(P['elapsed']/60, P['B_avg_ema'], 'b--', linewidth=2, label='Primitive B avg', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Group B (Mid Zone) — T2-T5 avg', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(20, 110)
g_b_peak = G[['T2','T3','T4','T5']].iloc[G['T1'].idxmax()].mean()
p_b_peak = P[['T2','T3','T4','T5']].iloc[P['T1'].idxmax()].mean()
ax.annotate(f'Gyroid peak avg: {g_b_peak:.1f}°C', xy=(18, 88), fontsize=9, color='blue')
ax.annotate(f'Primitive peak avg: {p_b_peak:.1f}°C', xy=(18, 93), fontsize=9, color='blue')

# --- Plot 3: Group C comparison ---
ax = axes[1, 0]
ax.plot(G['elapsed']/60, G['C_avg_ema'], 'g-', linewidth=2, label='Gyroid C avg', alpha=0.8)
ax.plot(P['elapsed']/60, P['C_avg_ema'], 'g--', linewidth=2, label='Primitive C avg', alpha=0.8)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('Group C (Far Zone) — T6-T9 avg', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(20, 110)
g_c_peak = G[['T6','T7','T8','T9']].iloc[G['T1'].idxmax()].mean()
p_c_peak = P[['T6','T7','T8','T9']].iloc[P['T1'].idxmax()].mean()
ax.annotate(f'Gyroid peak avg: {g_c_peak:.1f}°C', xy=(18, 72), fontsize=9, color='green')
ax.annotate(f'Primitive peak avg: {p_c_peak:.1f}°C', xy=(18, 65), fontsize=9, color='green')

# --- Plot 4: Temperature gradients over time ---
ax = axes[1, 1]
g_ab = G['A_avg_ema'] - G['B_avg_ema']
g_ac = G['A_avg_ema'] - G['C_avg_ema']
p_ab = P['A_avg_ema'] - P['B_avg_ema']
p_ac = P['A_avg_ema'] - P['C_avg_ema']

ax.plot(G['elapsed']/60, g_ab, 'b-', linewidth=2, label='Gyroid A-B', alpha=0.8)
ax.plot(P['elapsed']/60, p_ab, 'b--', linewidth=2, label='Primitive A-B', alpha=0.8)
ax.plot(G['elapsed']/60, g_ac, 'r-', linewidth=2, label='Gyroid A-C', alpha=0.8)
ax.plot(P['elapsed']/60, p_ac, 'r--', linewidth=2, label='Primitive A-C', alpha=0.8)
ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature Gradient (°C)', fontsize=11)
ax.set_title('Thermal Gradients — A-B and A-C', fontsize=12, fontweight='bold')
ax.legend(fontsize=9, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(0, 50)

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_primitive_vs_gyroid_10w.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_primitive_vs_gyroid_10w.pdf', bbox_inches='tight')
print("Saved: fig_compare_primitive_vs_gyroid_10w.png/pdf")

# --- Second figure: T7 anomaly and peak comparison ---
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))

# --- Plot 5: T7 comparison ---
ax = axes2[0]
ax.plot(G['elapsed']/60, G['T7_ema'], 'g-', linewidth=2, label='Gyroid T7', alpha=0.8)
ax.plot(P['elapsed']/60, P['T7_ema'], 'g--', linewidth=2, label='Primitive T7', alpha=0.8)
ax.plot(G['elapsed']/60, G['C_avg_ema'], 'k:', linewidth=1, label='Gyroid C avg', alpha=0.5)
ax.plot(P['elapsed']/60, P['C_avg_ema'], 'k--', linewidth=1, label='Primitive C avg', alpha=0.5)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.3)
ax.set_xlabel('Time (min)', fontsize=11)
ax.set_ylabel('Temperature (°C)', fontsize=11)
ax.set_title('T7 Anomaly — Primitive vs Gyroid', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 28)
ax.set_ylim(20, 80)
ax.annotate(f'Gyroid T7 peak: {G["T7"].max():.1f}°C', xy=(15, 76), fontsize=9, color='green')
ax.annotate(f'Primitive T7 peak: {P["T7"].max():.1f}°C', xy=(15, 50), fontsize=9, color='green')

# --- Plot 6: Peak temperature bar chart ---
ax = axes2[1]
sensors = ['T1', 'T2-T5\n(avg)', 'T6-T9\n(avg)']
g_peaks = [G['T1'].max(), 
           G[['T2','T3','T4','T5']].iloc[G['T1'].idxmax()].mean(),
           G[['T6','T7','T8','T9']].iloc[G['T1'].idxmax()].mean()]
p_peaks = [P['T1'].max(),
           P[['T2','T3','T4','T5']].iloc[P['T1'].idxmax()].mean(),
           P[['T6','T7','T8','T9']].iloc[P['T1'].idxmax()].mean()]

x = np.arange(len(sensors))
width = 0.35
ax.bar(x - width/2, g_peaks, width, label='Gyroid', color='#4CAF50', edgecolor='black', linewidth=0.5)
ax.bar(x + width/2, p_peaks, width, label='Primitive', color='#FF9800', edgecolor='black', linewidth=0.5)
ax.set_ylabel('Peak Temperature (°C)', fontsize=11)
ax.set_title('Peak Temperatures by Group', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(sensors, fontsize=10)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 120)

# Add value labels
for i, (gv, pv) in enumerate(zip(g_peaks, p_peaks)):
    ax.text(i - width/2, gv + 2, f'{gv:.1f}', ha='center', va='bottom', fontsize=9)
    ax.text(i + width/2, pv + 2, f'{pv:.1f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_t7_anomaly_and_peaks.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_t7_anomaly_and_peaks.pdf', bbox_inches='tight')
print("Saved: fig_compare_t7_anomaly_and_peaks.png/pdf")

# --- Third figure: Heating rate comparison ---
fig3, ax = plt.subplots(figsize=(12, 6))

sensors = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
g_rates = []
p_rates = []
t5 = 300

for c in sensors:
    g_mask = G['elapsed'] <= t5
    p_mask = P['elapsed'] <= t5
    g_rate = (G.loc[g_mask, f'{c}_ema'].iloc[-1] - G.loc[g_mask, f'{c}_ema'].iloc[0]) / (G.loc[g_mask, 'elapsed'].iloc[-1] / 60)
    p_rate = (P.loc[p_mask, f'{c}_ema'].iloc[-1] - P.loc[p_mask, f'{c}_ema'].iloc[0]) / (P.loc[p_mask, 'elapsed'].iloc[-1] / 60)
    g_rates.append(g_rate)
    p_rates.append(p_rate)

x = np.arange(len(sensors))
width = 0.35
ax.bar(x - width/2, g_rates, width, label='Gyroid', color='#4CAF50', edgecolor='black', linewidth=0.5)
ax.bar(x + width/2, p_rates, width, label='Primitive', color='#FF9800', edgecolor='black', linewidth=0.5)
ax.set_xlabel('Sensor', fontsize=11)
ax.set_ylabel('Heating Rate (°C/min)', fontsize=11)
ax.set_title('Heating Rate — First 5 Minutes (EMA smoothed)', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(sensors)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 5)

# Add value labels
for i, (gr, pr) in enumerate(zip(g_rates, p_rates)):
    ax.text(i - width/2, gr + 0.1, f'{gr:.2f}', ha='center', va='bottom', fontsize=8, rotation=45)
    ax.text(i + width/2, pr + 0.1, f'{pr:.2f}', ha='center', va='bottom', fontsize=8, rotation=45)

plt.tight_layout()
plt.savefig('output/paper/figures/fig_compare_heating_rates.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_compare_heating_rates.pdf', bbox_inches='tight')
print("Saved: fig_compare_heating_rates.png/pdf")

print("\n=== Summary Statistics ===")
print(f"Gyroid duration: {G['elapsed'].iloc[-1]/60:.2f} min")
print(f"Primitive duration: {P['elapsed'].iloc[-1]/60:.2f} min")
print(f"Gyroid T1 peak: {G['T1'].max():.2f}°C")
print(f"Primitive T1 peak: {P['T1'].max():.2f}°C")
print(f"Gyroid C-group peak avg: {g_peaks[2]:.2f}°C")
print(f"Primitive C-group peak avg: {p_peaks[2]:.2f}°C")
print(f"A-B gradient (Gyroid): {g_peaks[0] - g_peaks[1]:.2f}°C")
print(f"A-B gradient (Primitive): {p_peaks[0] - p_peaks[1]:.2f}°C")
print(f"A-C gradient (Gyroid): {g_peaks[0] - g_peaks[2]:.2f}°C")
print(f"A-C gradient (Primitive): {p_peaks[0] - p_peaks[2]:.2f}°C")
