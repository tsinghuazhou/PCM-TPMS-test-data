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
matplotlib.rcParams['xtick.major.size'] = 4
matplotlib.rcParams['ytick.major.size'] = 4
matplotlib.rcParams['xtick.minor.visible'] = True
matplotlib.rcParams['ytick.minor.visible'] = True

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
    worst_sensor = cols[worst_sensor_idx]
    remaining_cols = [c for i, c in enumerate(cols) if i != worst_sensor_idx]
    remaining_vals = np.delete(g, worst_sensor_idx, axis=1)
    raw_means = np.mean(remaining_vals, axis=1)
    return raw_means, worst_sensor, remaining_cols

def apply_ema(values, alpha):
    smoothed = [values[0]]
    for i in range(1, len(values)):
        smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
    return smoothed

base = r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究'

df_10w = load_and_process(f'{base}/temperature_record_20260804_163501.csv')
df_20w = load_and_process(f'{base}/temperature_record_20260731_195755.csv')
df_30w = load_and_process(f'{base}/temperature_record_20260803_171111-1.csv')

datasets = [
    ('10 W', df_10w, '#2a78d6'),
    ('20 W', df_20w, '#eda100'),
    ('30 W', df_30w, '#e34948'),
]

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)

for ax, (label, df, color) in zip(axes, datasets):
    t1 = df['T1'].values
    raw_b, _, _ = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
    smooth_b = apply_ema(raw_b, EMA_ALPHA)
    raw_c, _, _ = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
    smooth_c = apply_ema(raw_c, EMA_ALPHA)
    elapsed = df['elapsed'].values / 60.0

    ax.plot(elapsed, t1, color=color, linewidth=1.8, alpha=0.9, label='$T_1$ (Group A)')
    ax.plot(elapsed, smooth_b, color=color, linewidth=1.8, linestyle='--', alpha=0.7, label='$T_2$-$T_5$ (Group B)')
    ax.plot(elapsed, smooth_c, color=color, linewidth=1.8, linestyle=':', alpha=0.7, label='$T_6$-$T_9$ (Group C)')

    ax.axhline(y=42, color='gray', linewidth=0.8, linestyle='-.', alpha=0.5)
    ax.annotate('42\u00b0C', xy=(elapsed[0]+0.3, 42.5), fontsize=7, color='gray', alpha=0.7)

    ax.set_xlabel('Time (min)', fontsize=10)
    ax.set_title(f'Gyroid, {label}', fontsize=11, fontweight='bold')
    ax.set_xlim(0, elapsed[-1])
    ax.grid(True, alpha=0.15, linewidth=0.5)

axes[0].set_ylabel('Temperature (\u00b0C)', fontsize=10)
axes[0].legend(fontsize=7.5, loc='lower right', framealpha=0.9)

fig.suptitle('Temperature evolution of Gyroid TPMS/PCM composite under different heating powers',
             fontsize=12, fontweight='bold', y=1.02)

plt.tight_layout()
out = Path(r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究\output\paper\figures\fig_01_temperature_curves.pdf')
plt.savefig(str(out), dpi=300, bbox_inches='tight')
plt.savefig(str(out.with_suffix('.png')), dpi=200, bbox_inches='tight')
print(f'Saved: {out}')
