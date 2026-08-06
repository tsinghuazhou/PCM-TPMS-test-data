"""
Primitive 10W vs 20W 对比可视化
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
    sensor_devs = []
    for i in range(len(cols)):
        dev = np.mean(np.abs(g[:, i] - group_mean))
        sensor_devs.append(dev)
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
P10 = load('temperature_record_20260805_200423.csv')
P20 = load('temperature_record_20260806_162603.csv')

# Process groups
raw_b_10, worst_b_10, rem_b_10 = remove_worst_and_avg(P10, ['T2','T3','T4','T5'])
raw_c_10, worst_c_10, rem_c_10 = remove_worst_and_avg(P10, ['T6','T7','T8','T9'])

raw_b_20, worst_b_20, rem_b_20 = remove_worst_and_avg(P20, ['T2','T3','T4','T5'])
raw_c_20 = P20['T7'].values

# Apply EMA
smooth_b_10 = apply_ema(raw_b_10)
smooth_c_10 = apply_ema(raw_c_10)
smooth_b_20 = apply_ema(raw_b_20)
smooth_c_20 = apply_ema(raw_c_20)

smooth_t1_10 = apply_ema(P10['T1'].values)
smooth_t1_20 = apply_ema(P20['T1'].values)

# Figure 1: Temperature curves comparison (2x3 grid)
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Primitive TPMS/PCM Temperature Curves: 10W vs 20W', fontsize=16, fontweight='bold')

# 10W - Group A
ax = axes[0, 0]
ax.plot(P10['elapsed']/60, smooth_t1_10, 'r-', linewidth=2, label='A group (T1)')
ax.plot(P10['elapsed']/60, smooth_b_10, 'b-', linewidth=2, label='B group (T2-T5 avg)')
ax.plot(P10['elapsed']/60, smooth_c_10, 'g-', linewidth=2, label='C group (T6-T9 avg)')
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='PCM melting 42C')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (C)')
ax.set_title('10W (26.93 min)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 120)

# 20W - Group A
ax = axes[0, 1]
ax.plot(P20['elapsed']/60, smooth_t1_20, 'r-', linewidth=2, label='A group (T1)')
ax.plot(P20['elapsed']/60, smooth_b_20, 'b-', linewidth=2, label='B group (T2-T5 avg)')
ax.plot(P20['elapsed']/60, smooth_c_20, 'g-', linewidth=2, label='C group (T7)')
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='PCM melting 42C')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (C)')
ax.set_title('20W (12.35 min)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 120)

# Overlay comparison
ax = axes[0, 2]
ax.plot(P10['elapsed']/60, smooth_t1_10, 'r-', linewidth=2, label='10W T1', alpha=0.7)
ax.plot(P20['elapsed']/60, smooth_t1_20, 'r--', linewidth=2, label='20W T1', alpha=0.7)
ax.plot(P10['elapsed']/60, smooth_b_10, 'b-', linewidth=2, label='10W B', alpha=0.7)
ax.plot(P20['elapsed']/60, smooth_b_20, 'b--', linewidth=2, label='20W B', alpha=0.7)
ax.plot(P10['elapsed']/60, smooth_c_10, 'g-', linewidth=2, label='10W C', alpha=0.7)
ax.plot(P20['elapsed']/60, smooth_c_20, 'g--', linewidth=2, label='20W C', alpha=0.7)
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (C)')
ax.set_title('Overlay: 10W (solid) vs 20W (dashed)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 120)

# 10W - Temperature gradients
ax = axes[1, 0]
grad_ab_10 = smooth_t1_10 - smooth_b_10
grad_ac_10 = smooth_t1_10 - smooth_c_10
ax.plot(P10['elapsed']/60, grad_ab_10, 'b-', linewidth=2, label='A-B gradient')
ax.plot(P10['elapsed']/60, grad_ac_10, 'r-', linewidth=2, label='A-C gradient')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature difference (C)')
ax.set_title('10W Temperature Gradients', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

# 20W - Temperature gradients
ax = axes[1, 1]
grad_ab_20 = smooth_t1_20 - smooth_b_20
grad_ac_20 = smooth_t1_20 - smooth_c_20
ax.plot(P20['elapsed']/60, grad_ab_20, 'b-', linewidth=2, label='A-B gradient')
ax.plot(P20['elapsed']/60, grad_ac_20, 'r-', linewidth=2, label='A-C gradient')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature difference (C)')
ax.set_title('20W Temperature Gradients', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

# Gradient overlay
ax = axes[1, 2]
ax.plot(P10['elapsed']/60, grad_ab_10, 'b-', linewidth=2, label='10W A-B', alpha=0.7)
ax.plot(P20['elapsed']/60, grad_ab_20, 'b--', linewidth=2, label='20W A-B', alpha=0.7)
ax.plot(P10['elapsed']/60, grad_ac_10, 'r-', linewidth=2, label='10W A-C', alpha=0.7)
ax.plot(P20['elapsed']/60, grad_ac_20, 'r--', linewidth=2, label='20W A-C', alpha=0.7)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature difference (C)')
ax.set_title('Gradient Overlay: 10W (solid) vs 20W (dashed)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_10w_20w_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_10w_20w_comparison.pdf', bbox_inches='tight')
print('Saved: primitive_10w_20w_comparison.png/pdf')

# Figure 2: Bar chart comparison
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Primitive TPMS/PCM Key Metrics: 10W vs 20W', fontsize=14, fontweight='bold')

# Peak temperatures
ax = axes2[0]
x = np.arange(3)
width = 0.35
a_vals = [106.80, 112.98]
b_vals = [93.05, 87.15]
c_vals = [70.07, 67.05]
ax.bar(x - width/2, [a_vals[0], b_vals[0], c_vals[0]], width, label='10W', color='#4CAF50', edgecolor='black', linewidth=0.5)
ax.bar(x + width/2, [a_vals[1], b_vals[1], c_vals[1]], width, label='20W', color='#FF9800', edgecolor='black', linewidth=0.5)
ax.set_ylabel('Peak Temperature (C)')
ax.set_title('Peak Temperatures by Group', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['A (T1)', 'B (mid)', 'C (top)'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
for i, (v10, v20) in enumerate(zip(a_vals, [b_vals[0], c_vals[0]])):
    pass
for i, v in enumerate([a_vals[0], b_vals[0], c_vals[0]]):
    ax.text(i - width/2, v + 1, f'{v:.1f}', ha='center', va='bottom', fontsize=9)
for i, v in enumerate([a_vals[1], b_vals[1], c_vals[1]]):
    ax.text(i + width/2, v + 1, f'{v:.1f}', ha='center', va='bottom', fontsize=9)

# Temperature gradients
ax = axes2[1]
ab_vals = [13.75, 25.83]
ac_vals = [36.73, 45.93]
bc_vals = [22.98, 20.10]
ax.bar(x - width/2, [ab_vals[0], ac_vals[0], bc_vals[0]], width, label='10W', color='#4CAF50', edgecolor='black', linewidth=0.5)
ax.bar(x + width/2, [ab_vals[1], ac_vals[1], bc_vals[1]], width, label='20W', color='#FF9800', edgecolor='black', linewidth=0.5)
ax.set_ylabel('Temperature Gradient (C)')
ax.set_title('Temperature Gradients at T1 Peak', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['A-B', 'A-C', 'B-C'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
for i, v in enumerate([ab_vals[0], ac_vals[0], bc_vals[0]]):
    ax.text(i - width/2, v + 0.5, f'{v:.1f}', ha='center', va='bottom', fontsize=9)
for i, v in enumerate([ab_vals[1], ac_vals[1], bc_vals[1]]):
    ax.text(i + width/2, v + 0.5, f'{v:.1f}', ha='center', va='bottom', fontsize=9)

# Time to reach 42C
ax = axes2[2]
t1_vals = [104, 69]
b_t_vals = [770, 346]
c_t_vals = [955, 500]
ax.bar(x - width/2, [t1_vals[0], b_t_vals[0], c_t_vals[0]], width, label='10W', color='#4CAF50', edgecolor='black', linewidth=0.5)
ax.bar(x + width/2, [t1_vals[1], b_t_vals[1], c_t_vals[1]], width, label='20W', color='#FF9800', edgecolor='black', linewidth=0.5)
ax.set_ylabel('Time to 42C (s)')
ax.set_title('Time to Reach PCM Melting Point', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['A (T1)', 'B (mid)', 'C (top)'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
for i, v in enumerate([t1_vals[0], b_t_vals[0], c_t_vals[0]]):
    ax.text(i - width/2, v + 10, f'{v}', ha='center', va='bottom', fontsize=9)
for i, v in enumerate([t1_vals[1], b_t_vals[1], c_t_vals[1]]):
    ax.text(i + width/2, v + 10, f'{v}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_10w_20w_bars.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_10w_20w_bars.pdf', bbox_inches='tight')
print('Saved: primitive_10w_20w_bars.png/pdf')

# Figure 3: T7 behavior comparison
fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))
fig3.suptitle('T7 Sensor Behavior: Reversal Between 10W and 20W', fontsize=14, fontweight='bold')

# T7 in 10W
ax = axes3[0]
ax.plot(P10['elapsed']/60, P10['T6'].ewm(alpha=0.4,adjust=False).mean(), 'g-', linewidth=1.5, label='T6', alpha=0.7)
ax.plot(P10['elapsed']/60, P10['T7'].ewm(alpha=0.4,adjust=False).mean(), 'm-', linewidth=2, label='T7 (OUTLIER)', alpha=0.9)
ax.plot(P10['elapsed']/60, P10['T8'].ewm(alpha=0.4,adjust=False).mean(), 'g--', linewidth=1.5, label='T8', alpha=0.7)
ax.plot(P10['elapsed']/60, P10['T9'].ewm(alpha=0.4,adjust=False).mean(), 'g:', linewidth=1.5, label='T9', alpha=0.7)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (C)')
ax.set_title('10W: T7 is OUTLIER (low)', fontweight='bold', color='red')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 80)

# T7 in 20W
ax = axes3[1]
ax.plot(P20['elapsed']/60, P20['T6'].ewm(alpha=0.4,adjust=False).mean(), 'g-', linewidth=1.5, label='T6 (bad contact)', alpha=0.7)
ax.plot(P20['elapsed']/60, P20['T7'].ewm(alpha=0.4,adjust=False).mean(), 'm-', linewidth=2, label='T7 (RELIABLE)', alpha=0.9)
ax.plot(P20['elapsed']/60, P20['T8'].ewm(alpha=0.4,adjust=False).mean(), 'g--', linewidth=1.5, label='T8 (bad contact)', alpha=0.7)
ax.plot(P20['elapsed']/60, P20['T9'].ewm(alpha=0.4,adjust=False).mean(), 'g:', linewidth=1.5, label='T9 (bad contact)', alpha=0.7)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (C)')
ax.set_title('20W: T7 is RELIABLE (high)', fontweight='bold', color='green')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 80)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_t7_reversal.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_t7_reversal.pdf', bbox_inches='tight')
print('Saved: primitive_t7_reversal.png/pdf')

print('\nVisualization complete.')
