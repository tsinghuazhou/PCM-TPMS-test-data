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
P_new = load('tpms_primitive20w_20260806_214551.csv')
P_old = load('deprecated/tpms_primitive20w_20260806_162603.csv')
G10 = load('tpms_gyroid10w_20260804_163501.csv')

# Process groups
raw_b_new, _, rem_b_new = remove_worst_and_avg(P_new, ['T2','T3','T4','T5'])
raw_c_new, _, rem_c_new = remove_worst_and_avg(P_new, ['T6','T7','T8','T9'])

raw_b_old, _, _ = remove_worst_and_avg(P_old, ['T2','T3','T4','T5'])
raw_c_old = P_old['T7'].values

raw_b_g10, _, _ = remove_worst_and_avg(G10, ['T2','T3','T4','T5'])
raw_c_g10, _, _ = remove_worst_and_avg(G10, ['T6','T7','T8','T9'])

# EMA
smooth_b_new = apply_ema(raw_b_new)
smooth_c_new = apply_ema(raw_c_new)
smooth_b_old = apply_ema(raw_b_old)
smooth_c_old = apply_ema(raw_c_old)
smooth_b_g10 = apply_ema(raw_b_g10)
smooth_c_g10 = apply_ema(raw_c_g10)

# Figure 1: Temperature curves
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Primitive 20W Repeat Experiment Analysis', fontsize=16, fontweight='bold')

# 10W reference
ax = axes[0, 0]
ax.plot(G10['elapsed']/60, G10['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(G10['elapsed']/60, smooth_b_g10, 'b-', lw=2, label='B (mid)')
ax.plot(G10['elapsed']/60, smooth_c_g10, 'g-', lw=2, label='C (top)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Gyroid 10W (reference)', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 100)

# Old Primitive 20W
ax = axes[0, 1]
ax.plot(P_old['elapsed']/60, P_old['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(P_old['elapsed']/60, smooth_b_old, 'b-', lw=2, label='B (mid)')
ax.plot(P_old['elapsed']/60, smooth_c_old, 'g-', lw=2, label='C (T7 only)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Primitive 20W - Run 1 (16:26)', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 120)

# New Primitive 20W
ax = axes[0, 2]
ax.plot(P_new['elapsed']/60, P_new['T1'].ewm(alpha=0.4,adjust=False).mean(), 'r-', lw=2, label='A (T1)')
ax.plot(P_new['elapsed']/60, smooth_b_new, 'b-', lw=2, label='B (mid)')
ax.plot(P_new['elapsed']/60, smooth_c_new, 'g-', lw=2, label='C (top, 3 sensors)')
ax.axhline(y=42, color='gray', ls='--', lw=1, alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (C)')
ax.set_title('Primitive 20W - Run 2 (21:45) NEW', fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3); ax.set_ylim(20, 120)

# Gradients
ax = axes[1, 0]
g_ab = G10['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_g10
g_ac = G10['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_g10
ax.plot(G10['elapsed']/60, g_ab, 'b-', lw=2, label='A-B')
ax.plot(G10['elapsed']/60, g_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('Gyroid 10W Gradients', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 1]
o_ab = P_old['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_old
o_ac = P_old['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_old
ax.plot(P_old['elapsed']/60, o_ab, 'b-', lw=2, label='A-B')
ax.plot(P_old['elapsed']/60, o_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('Primitive 20W Run 1 Gradients', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 2]
n_ab = P_new['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_b_new
n_ac = P_new['T1'].ewm(alpha=0.4,adjust=False).mean() - smooth_c_new
ax.plot(P_new['elapsed']/60, n_ab, 'b-', lw=2, label='A-B')
ax.plot(P_new['elapsed']/60, n_ac, 'r-', lw=2, label='A-C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (C)')
ax.set_title('Primitive 20W Run 2 Gradients (NEW)', fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_20w_repeat_curves.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_20w_repeat_curves.pdf', bbox_inches='tight')
print('Saved: primitive_20w_repeat_curves.png/pdf')

# Figure 2: Reproducibility comparison
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Primitive 20W Reproducibility: Run 1 vs Run 2', fontsize=14, fontweight='bold')

# Peak temperatures
ax = axes2[0]
x = np.arange(3)
w = 0.35
vals1 = [112.98, 87.15, 67.05]
vals2 = [115.76, 91.08, 76.99]
ax.bar(x - w/2, vals1, w, label='Run 1 (16:26)', color='#FF9800', edgecolor='black', lw=0.5)
ax.bar(x + w/2, vals2, w, label='Run 2 (21:45)', color='#4CAF50', edgecolor='black', lw=0.5)
ax.set_ylabel('Peak Temperature (C)')
ax.set_title('Peak Temperatures', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['A (T1)', 'B (mid)', 'C (top)'])
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
for i, (v1, v2) in enumerate(zip(vals1, vals2)):
    ax.text(i - w/2, v1 + 1, '%.1f' % v1, ha='center', va='bottom', fontsize=9)
    ax.text(i + w/2, v2 + 1, '%.1f' % v2, ha='center', va='bottom', fontsize=9)

# Gradients
ax = axes2[1]
g1 = [25.83, 45.93, 20.10]
g2 = [24.68, 38.77, 14.08]
ax.bar(x - w/2, g1, w, label='Run 1', color='#FF9800', edgecolor='black', lw=0.5)
ax.bar(x + w/2, g2, w, label='Run 2', color='#4CAF50', edgecolor='black', lw=0.5)
ax.set_ylabel('Gradient (C)')
ax.set_title('Temperature Gradients', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['A-B', 'A-C', 'B-C'])
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
for i, (v1, v2) in enumerate(zip(g1, g2)):
    ax.text(i - w/2, v1 + 0.5, '%.1f' % v1, ha='center', va='bottom', fontsize=9)
    ax.text(i + w/2, v2 + 0.5, '%.1f' % v2, ha='center', va='bottom', fontsize=9)

# C-group sensors
ax = axes2[1]  # reuse
# Actually let's make a separate figure for C-group

# Time to 42C
ax = axes2[2]
t1 = [69, 31]
tb = [346, 321]
tc = [500, 415]
ax.bar(x - w/2, [t1[0], tb[0], tc[0]], w, label='Run 1', color='#FF9800', edgecolor='black', lw=0.5)
ax.bar(x + w/2, [t1[1], tb[1], tc[1]], w, label='Run 2', color='#4CAF50', edgecolor='black', lw=0.5)
ax.set_ylabel('Time to 42C (s)')
ax.set_title('PCM Melting Time', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(['A (T1)', 'B (mid)', 'C (top)'])
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
for i, (v1, v2) in enumerate(zip([t1[0], tb[0], tc[0]], [t1[1], tb[1], tc[1]])):
    ax.text(i - w/2, v1 + 5, '%d' % v1, ha='center', va='bottom', fontsize=9)
    ax.text(i + w/2, v2 + 5, '%d' % v2, ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('output/paper/figures/primitive_20w_repeat_bars.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_20w_repeat_bars.pdf', bbox_inches='tight')
print('Saved: primitive_20w_repeat_bars.png/pdf')

# Figure 3: C-group sensor comparison
fig3, ax = plt.subplots(figsize=(10, 5))
sensors = ['T6', 'T7', 'T8', 'T9']
run1 = [P_old[c].max() for c in sensors]
run2 = [P_new[c].max() for c in sensors]
x = np.arange(4)
w = 0.35
ax.bar(x - w/2, run1, w, label='Run 1 (16:26)', color='#FF9800', edgecolor='black', lw=0.5)
ax.bar(x + w/2, run2, w, label='Run 2 (21:45)', color='#4CAF50', edgecolor='black', lw=0.5)
ax.set_xlabel('Sensor')
ax.set_ylabel('Peak Temperature (C)')
ax.set_title('C-group (Top Surface) Sensor Comparison\nRun 2 shows much better contact for T7/T8/T9', fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(sensors)
ax.legend(); ax.grid(True, alpha=0.3, axis='y')
ax.axhline(y=50, color='red', ls=':', lw=1, alpha=0.5)
for i, (v1, v2) in enumerate(zip(run1, run2)):
    ax.text(i - w/2, v1 + 1, '%.1f' % v1, ha='center', va='bottom', fontsize=9)
    ax.text(i + w/2, v2 + 1, '%.1f' % v2, ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('output/paper/figures/primitive_20w_repeat_cgroup.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/primitive_20w_repeat_cgroup.pdf', bbox_inches='tight')
print('Saved: primitive_20w_repeat_cgroup.png/pdf')

print('\nAll plots saved.')
