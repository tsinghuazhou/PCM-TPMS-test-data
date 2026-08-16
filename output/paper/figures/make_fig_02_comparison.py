import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['axes.linewidth'] = 1.0
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'

STYLE = Path(r'C:\Users\tsing\AppData\Roaming\com.ai4s.workbench\runtime\xdg-config\opencode\skills\publication-figures\openscience.mplstyle')
if STYLE.exists():
    plt.style.use(str(STYLE))

EMA_ALPHA = 0.4

def load_and_process(filepath):
    df = pd.read_csv(filepath, parse_dates=[0])
    df.columns = ['time', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
    elapsed = (df['time'] - df['time'].min()).dt.total_seconds()
    df['elapsed'] = elapsed
    return df

def remove_worst_sensor_and_average(df, cols):
    g = df[cols].values
    group_mean = np.mean(g, axis=1)
    sensor_devs = []
    for i in range(len(cols)):
        dev = np.mean(np.abs(g[:, i] - group_mean))
        sensor_devs.append(dev)
    worst_sensor_idx = np.argmax(sensor_devs)
    remaining_cols = [c for j, c in enumerate(cols) if j != worst_sensor_idx]
    remaining_vals = np.delete(g, worst_sensor_idx, axis=1)
    raw_means = np.mean(remaining_vals, axis=1)
    return raw_means

def apply_ema(values, alpha):
    smoothed = [values[0]]
    for i in range(1, len(values)):
        smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
    return smoothed

base = r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究'

df_10w = load_and_process(f'{base}/tpms_gyroid10w_20260804_163501.csv')
df_20w = load_and_process(f'{base}/tpms_gyroid20w_20260731_195755.csv')
df_30w = load_and_process(f'{base}/tpms_gyroid30w_20260803_171111-1.csv')

datasets = [('10W', df_10w), ('20W', df_20w), ('30W', df_30w)]
results = {}
for name, df in datasets:
    t1_final = df['T1'].iloc[-1]
    raw_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
    smooth_b = apply_ema(raw_b, EMA_ALPHA)
    raw_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
    smooth_c = apply_ema(raw_c, EMA_ALPHA)
    results[name] = {
        'T1': t1_final,
        'T2-T5': smooth_b[-1],
        'T6-T9': smooth_c[-1],
    }

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

powers = ['10W', '20W', '30W']
colors_power = ['#2a78d6', '#eda100', '#e34948']
x = np.arange(3)
width = 0.25

for i, group in enumerate(['T1', 'T2-T5', 'T6-T9']):
    vals = [results[p][group] for p in powers]
    bars = axes[0].bar(x + i*width - width, vals, width, label=group,
                       color=['#2a78d6', '#1baf7a', '#e34948'][i], alpha=0.85, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     f'{val:.1f}', ha='center', va='bottom', fontsize=7.5)

axes[0].set_xlabel('Heating Power', fontsize=10)
axes[0].set_ylabel('Final Temperature (\u00b0C)', fontsize=10)
axes[0].set_title('(a) Final temperature by group and power', fontsize=10, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(powers)
axes[0].legend(fontsize=8, loc='upper left')
axes[0].set_ylim(0, 170)
axes[0].grid(True, axis='y', alpha=0.15, linewidth=0.5)

temp_rise = {}
for name, df in datasets:
    t1_rise = df['T1'].iloc[-1] - df['T1'].iloc[0]
    raw_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
    smooth_b = apply_ema(raw_b, EMA_ALPHA)
    raw_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
    smooth_c = apply_ema(raw_c, EMA_ALPHA)
    b_rise = smooth_b[-1] - smooth_b[0]
    c_rise = smooth_c[-1] - smooth_c[0]
    temp_rise[name] = {'T1': t1_rise, 'T2-T5': b_rise, 'T6-T9': c_rise}

for i, group in enumerate(['T1', 'T2-T5', 'T6-T9']):
    vals = [temp_rise[p][group] for p in powers]
    bars = axes[1].bar(x + i*width - width, vals, width, label=group,
                       color=['#2a78d6', '#1baf7a', '#e34948'][i], alpha=0.85, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     f'{val:.1f}', ha='center', va='bottom', fontsize=7.5)

axes[1].set_xlabel('Heating Power', fontsize=10)
axes[1].set_ylabel('Temperature Rise (\u00b0C)', fontsize=10)
axes[1].set_title('(b) Temperature rise by group and power', fontsize=10, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(powers)
axes[1].legend(fontsize=8, loc='upper left')
axes[1].set_ylim(0, 140)
axes[1].grid(True, axis='y', alpha=0.15, linewidth=0.5)

fig.suptitle('Gyroid TPMS/PCM: heating power comparison', fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()

out = Path(r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究\output\paper\figures\fig_02_power_comparison.pdf')
plt.savefig(str(out), dpi=300, bbox_inches='tight')
plt.savefig(str(out.with_suffix('.png')), dpi=200, bbox_inches='tight')
print(f'Saved: {out}')

fig2, ax2 = plt.subplots(figsize=(8, 5))

durations = {'10W': 1523/60, '20W': 667/60, '30W': 510/60}
bars = ax2.bar(powers, [durations[p] for p in powers],
               color=colors_power, alpha=0.85, edgecolor='white', width=0.5)
for bar, p in zip(bars, powers):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{durations[p]:.1f} min', ha='center', va='bottom', fontsize=9)

ax2.set_xlabel('Heating Power', fontsize=11)
ax2.set_ylabel('Duration (min)', fontsize=11)
ax2.set_title('Gyroid TPMS/PCM: heating duration vs. power', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 35)
ax2.grid(True, axis='y', alpha=0.15, linewidth=0.5)
plt.tight_layout()

out2 = Path(r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究\output\paper\figures\fig_03_duration.pdf')
plt.savefig(str(out2), dpi=300, bbox_inches='tight')
plt.savefig(str(out2.with_suffix('.png')), dpi=200, bbox_inches='tight')
print(f'Saved: {out2}')
