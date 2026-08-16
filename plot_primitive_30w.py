"""
Primitive 30W 可视化
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
P20 = load('tpms_primitive20w_20260806_214551.csv')
P10 = load('tpms_primitive10w_20260805_200423.csv')

# Process groups
raw_b_30, _, _ = remove_worst_and_avg(P30, ['T2','T3','T4','T5'])
raw_c_30, _, _ = remove_worst_and_avg(P30, ['T6','T7','T8','T9'])
raw_b_20, _, _ = remove_worst_and_avg(P20, ['T2','T3','T4','T5'])
raw_c_20, _, _ = remove_worst_and_avg(P20, ['T6','T7','T8','T9'])
raw_b_10, _, _ = remove_worst_and_avg(P10, ['T2','T3','T4','T5'])
raw_c_10, _, _ = remove_worst_and_avg(P10, ['T6','T7','T8','T9'])

# EMA
smooth_b_30 = apply_ema(raw_b_30)
smooth_c_30 = apply_ema(raw_c_30)
smooth_b_20 = apply_ema(raw_b_20)
smooth_c_20 = apply_ema(raw_c_20)
smooth_b_10 = apply_ema(raw_b_10)
smooth_c_10 = apply_ema(raw_c_10)

# Figure 1: Temperature curves
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Primitive TPMS/PCM: 10W vs 20W vs 30W Comparison', fontsize=16, fontweight='bold')

# 10W
ax = axes[0, 0]
ax.plot(P10['elapsed']/60, P10['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(P10['elapsed']/60, smooth_b_10, 'b-', lw=2, label='B (mid)')
ax.plot(P10['elapsed']/60, smooth_c_10, 'g-', lw=2, label='C (top)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Primitive 10W (26.93 min)', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 120)

# 20W
ax = axes[0, 1]
ax.plot(P20['elapsed']/60, P20['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(P20['elapsed']/60, smooth_b_20, 'b-', lw=2, label='B (mid)')
ax.plot(P20['elapsed']/60, smooth_c_20, 'g-', lw=2, label='C (top)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Primitive 20W (11.93 min)', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 140)

# 30W
ax = axes[0, 2]
ax.plot(P30['elapsed']/60, P30['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(P30['elapsed']/60, smooth_b_30, 'b-', lw=2, label='B (mid)')
ax.plot(P30['elapsed']/60, smooth_c_30, 'g-', lw=2, label='C (top)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Primitive 30W (12.45 min) NEW', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 140)

# Gradients
ax = axes[1, 0]
g_ab = P10['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_10
g_ac = P10['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_10
ax.plot(P10['elapsed']/60, g_ab, 'b-', lw=2, label='A-B')
ax.plot(P10['elapsed']/60, g_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('10W Gradients', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 1]
g_ab = P20['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_20
g_ac = P20['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_20
ax.plot(P20['elapsed']/60, g_ab, 'b-', lw=2, label='A-B')
ax.plot(P20['elapsed']/60, g_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('20W Gradients', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 2]
g_ab = P30['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_30
g_ac = P30['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_30
ax.plot(P30['elapsed']/60, g_ab, 'b-', lw=2, label='A-B')
ax.plot(P30['elapsed']/60, g_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('30W Gradients (NEW)', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_30w_curves.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_30w_curves.pdf', bbox_inches='tight')
print('Saved: primitive_30w_curves.png/pdf')

# Figure 2: Power comparison bars
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Primitive TPMS: Power Comparison (10W vs 20W vs 30W)', fontsize=14, fontweight='bold')

# Peak temperatures
ax = axes2[0]
x = np.arange(3)
w = 0.25
a_vals = [106.80, 115.76, 134.16]
b_vals = [93.05, 91.08, 98.45]
c_vals = [70.07, 76.99, 78.59]
ax.bar(x - w, a_vals, w, label='A (T1)', color='#d62728')
ax.bar(x, b_vals, w, label='B (mid)', color='#1f77b4')
ax.bar(x + w, c_vals, w, label='C (top)', color='#2ca02c')
ax.set_ylabel('Peak Temperature (C)')
ax.set_title('Peak Temperatures', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['10W', '20W', '30W'])
ax.legend(fontsize=9); ax.grid(True, alpha=0.3, axis='y')

# Temperature gradients
ax = axes2[1]
ab_vals = [13.75, 24.68, 35.71]
ac_vals = [36.73, 38.77, 55.57]
bc_vals = [22.98, 14.08, 19.86]
ax.bar(x - w, ab_vals, w, label='A-B', color='#1f77b4')
ax.bar(x, ac_vals, w, label='A-C', color='#d62728')
ax.bar(x + w, bc_vals, w, label='B-C', color='#2ca02c')
ax.set_ylabel('Gradient (C)')
ax.set_title('Temperature Gradients', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['10W', '20W', '30W'])
ax.legend(fontsize=9); ax.grid(True, alpha=0.3, axis='y')

# Time to 42C
ax = axes2[2]
t1_vals = [104, 31, 40]
tb_vals = [770, 321, 218]
tc_vals = [955, 415, 323]
ax.bar(x - w, t1_vals, w, label='A (T1)', color='#d62728')
ax.bar(x, tb_vals, w, label='B (mid)', color='#1f77b4')
ax.bar(x + w, tc_vals, w, label='C (top)', color='#2ca02c')
ax.set_ylabel('Time to 42C (s)')
ax.set_title('PCM Melting Time', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['10W', '20W', '30W'])
ax.legend(fontsize=9); ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_power_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_power_comparison.pdf', bbox_inches='tight')
print('Saved: primitive_power_comparison.png/pdf')

# Figure 3: C-group sensors
fig3, ax = plt.subplots(figsize=(10, 5))
sensors = ['T6', 'T7', 'T8', 'T9']
p10_c = [P10[c].max() for c in sensors]
p20_c = [P20[c].max() for c in sensors]
p30_c = [P30[c].max() for c in sensors]
x = np.arange(4)
w = 0.25
ax.bar(x - w, p10_c, w, label='10W', color='#4CAF50', edgecolor='black', lw=0.5)
ax.bar(x, p20_c, w, label='20W', color='#FF9800', edgecolor='black', lw=0.5)
ax.bar(x + w, p30_c, w, label='30W', color='#F44336', edgecolor='black', lw=0.5)
ax.set_xlabel('Sensor')
ax.set_ylabel('Peak Temperature (C)')
ax.set_title('C-group (Top Surface) Sensor Comparison\nT6 consistently outlier across all powers', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(sensors)
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('output/paper/figures/primitive_30w_cgroup.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_30w_cgroup.pdf', bbox_inches='tight')
print('Saved: primitive_30w_cgroup.png/pdf')

print('\nAll plots saved.')
