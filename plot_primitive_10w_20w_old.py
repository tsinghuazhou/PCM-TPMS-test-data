"""
Gyroid 10W vs 20W 对比可视化
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

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
G10 = load('tpms_gyroid10w_20260804_163501.csv')
G20_old = load('tpms_gyroid30w_20260803_171111.csv')
G20_new = load('deprecated/tpms_primitive20w_20260806_162603.csv')

# Process groups
raw_b_10, _, _ = remove_worst_and_avg(G10, ['T2','T3','T4','T5'])
raw_c_10, _, _ = remove_worst_and_avg(G10, ['T6','T7','T8','T9'])

raw_b_20o, _, _ = remove_worst_and_avg(G20_old, ['T2','T3','T4','T5'])
raw_c_20o, _, _ = remove_worst_and_avg(G20_old, ['T6','T7','T8','T9'])

raw_b_20n, _, _ = remove_worst_and_avg(G20_new, ['T2','T3','T4','T5'])
raw_c_20n = G20_new['T7'].values

# Apply EMA
smooth_b_10 = apply_ema(raw_b_10)
smooth_c_10 = apply_ema(raw_c_10)
smooth_b_20o = apply_ema(raw_b_20o)
smooth_c_20o = apply_ema(raw_c_20o)
smooth_b_20n = apply_ema(raw_b_20n)
smooth_c_20n = apply_ema(raw_c_20n)

smooth_t1_10 = apply_ema(G10['T1'].values)
smooth_t1_20o = apply_ema(G20_old['T1'].values)
smooth_t1_20n = apply_ema(G20_new['T1'].values)

# Figure 1: Temperature curves comparison
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Gyroid TPMS/PCM 温度曲线对比：10W vs 20W', fontsize=16, fontweight='bold')

# 10W
ax = axes[0, 0]
ax.plot(G10['elapsed']/60, smooth_t1_10, 'r-', linewidth=2, label='A组 (T1)')
ax.plot(G10['elapsed']/60, smooth_b_10, 'b-', linewidth=2, label='B组 (T2-T5均值)')
ax.plot(G10['elapsed']/60, smooth_c_10, 'g-', linewidth=2, label='C组 (T6-T9均值)')
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='PCM熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('10W (25.38 min)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 100)

# 20W old
ax = axes[0, 1]
ax.plot(G20_old['elapsed']/60, smooth_t1_20o, 'r-', linewidth=2, label='A组 (T1)')
ax.plot(G20_old['elapsed']/60, smooth_b_20o, 'b-', linewidth=2, label='B组 (T2-T5均值)')
ax.plot(G20_old['elapsed']/60, smooth_c_20o, 'g-', linewidth=2, label='C组 (T6-T9均值)')
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='PCM熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('20W旧 (8.50 min, 2026-08-03)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 130)

# 20W new
ax = axes[0, 2]
ax.plot(G20_new['elapsed']/60, smooth_t1_20n, 'r-', linewidth=2, label='A组 (T1)')
ax.plot(G20_new['elapsed']/60, smooth_b_20n, 'b-', linewidth=2, label='B组 (T2-T5均值)')
ax.plot(G20_new['elapsed']/60, smooth_c_20n, 'g-', linewidth=2, label='C组 (T7)')
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='PCM熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('20W新 (12.35 min, 2026-08-06)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(20, 130)

# Temperature gradients
ax = axes[1, 0]
grad_ab_10 = smooth_t1_10 - smooth_b_10
grad_ac_10 = smooth_t1_10 - smooth_c_10
ax.plot(G10['elapsed']/60, grad_ab_10, 'b-', linewidth=2, label='A-B梯度')
ax.plot(G10['elapsed']/60, grad_ac_10, 'r-', linewidth=2, label='A-C梯度')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度差 (°C)')
ax.set_title('10W 温度梯度', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
grad_ab_20o = smooth_t1_20o - smooth_b_20o
grad_ac_20o = smooth_t1_20o - smooth_c_20o
ax.plot(G20_old['elapsed']/60, grad_ab_20o, 'b-', linewidth=2, label='A-B梯度')
ax.plot(G20_old['elapsed']/60, grad_ac_20o, 'r-', linewidth=2, label='A-C梯度')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度差 (°C)')
ax.set_title('20W旧 温度梯度', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

ax = axes[1, 2]
grad_ab_20n = smooth_t1_20n - smooth_b_20n
grad_ac_20n = smooth_t1_20n - smooth_c_20n
ax.plot(G20_new['elapsed']/60, grad_ab_20n, 'b-', linewidth=2, label='A-B梯度')
ax.plot(G20_new['elapsed']/60, grad_ac_20n, 'r-', linewidth=2, label='A-C梯度')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度差 (°C)')
ax.set_title('20W新 温度梯度', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_10w_20w_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_10w_20w_comparison.pdf', bbox_inches='tight')
print('Saved: gyroid_10w_20w_comparison.png/pdf')

# Figure 2: Bar chart comparison
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Gyroid TPMS/PCM 关键指标对比', fontsize=14, fontweight='bold')

# Peak temperatures
ax = axes2[0]
x = np.arange(3)
width = 0.25
a_vals = [93.77, 115.22, 112.98]
b_vals = [87.35, 94.78, 87.15]
c_vals = [76.73, 79.44, 67.05]
ax.bar(x - width, a_vals, width, label='A组 (T1)', color='#d62728')
ax.bar(x, b_vals, width, label='B组 (均值)', color='#1f77b4')
ax.bar(x + width, c_vals, width, label='C组 (均值/T7)', color='#2ca02c')
ax.set_xlabel('实验条件')
ax.set_ylabel('峰值温度 (°C)')
ax.set_title('峰值温度', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['10W', '20W旧', '20W新'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

# Temperature gradients
ax = axes2[1]
ab_vals = [6.42, 20.44, 25.83]
ac_vals = [17.04, 35.78, 45.93]
bc_vals = [10.62, 15.33, 20.10]
ax.bar(x - width, ab_vals, width, label='A-B', color='#1f77b4')
ax.bar(x, ac_vals, width, label='A-C', color='#d62728')
ax.bar(x + width, bc_vals, width, label='B-C', color='#2ca02c')
ax.set_xlabel('实验条件')
ax.set_ylabel('温度梯度 (°C)')
ax.set_title('温度梯度（T1峰值时刻）', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['10W', '20W旧', '20W新'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

# Time to reach 42°C
ax = axes2[2]
t1_vals = [147, 21, 69]
b_t_vals = [737, 219, 346]
c_t_vals = [910, 321, 500]
ax.bar(x - width, t1_vals, width, label='A组 (T1)', color='#d62728')
ax.bar(x, b_t_vals, width, label='B组 (均值)', color='#1f77b4')
ax.bar(x + width, c_t_vals, width, label='C组 (均值/T7)', color='#2ca02c')
ax.set_xlabel('实验条件')
ax.set_ylabel('时间 (s)')
ax.set_title('达到42°C时间', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['10W', '20W旧', '20W新'])
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_10w_20w_bars.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_10w_20w_bars.pdf', bbox_inches='tight')
print('Saved: gyroid_10w_20w_bars.png/pdf')

print('\nVisualization complete.')
