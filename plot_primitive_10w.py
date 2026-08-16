import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

df = pd.read_csv('tpms_primitive10w_20260805_200423.csv')
df['时间戳'] = pd.to_datetime(df['时间戳'])
df['elapsed_min'] = (df['时间戳'] - df['时间戳'].iloc[0]).dt.total_seconds() / 60

fig, ax = plt.subplots(figsize=(10, 6))

colors = {
    'T1': '#d62728',  # red
    'T2': '#1f77b4', 'T3': '#1f77b4', 'T4': '#1f77b4', 'T5': '#1f77b4',  # blue
    'T6': '#2ca02c', 'T7': '#2ca02c', 'T8': '#2ca02c', 'T9': '#2ca02c',  # green
}
linestyles = {'T1': '-', 'T2': '--', 'T3': '-.', 'T4': ':', 'T5': '--',
              'T6': '-', 'T7': '--', 'T8': '-.', 'T9': ':'}

for col in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    label = f"{col}"
    if col == 'T1':
        label = 'T1 (A group - heater)'
    elif col in ['T2','T3','T4','T5']:
        label = f'{col} (B group)' if col == 'T2' else None
    else:
        label = f'{col} (C group)' if col == 'T6' else None
    
    ax.plot(df['elapsed_min'], df[col], 
            color=colors[col], 
            linestyle=linestyles[col],
            linewidth=1.5 if col == 'T1' else 1.0,
            label=label,
            alpha=0.9 if col == 'T1' else 0.7)

# Mark PCM melting point
ax.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5, label='PCM melting point (42°C)')

# Mark peak time
peak_time = 26.93
ax.axvline(x=peak_time, color='black', linestyle='--', linewidth=1, alpha=0.5, label=f'Peak at {peak_time:.1f}min')

ax.set_xlabel('Time (min)', fontsize=12)
ax.set_ylabel('Temperature (°C)', fontsize=12)
ax.set_title('Primitive TPMS - 10W Heating\nTemperature vs Time', fontsize=14)
ax.legend(loc='upper left', fontsize=9, ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, df['elapsed_min'].max())
ax.set_ylim(20, 110)

plt.tight_layout()
plt.savefig('output/paper/figures/fig_primitive_10w_temperature_curves.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_primitive_10w_temperature_curves.pdf', bbox_inches='tight')
print("Saved: fig_primitive_10w_temperature_curves.png/pdf")

# Summary statistics figure
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart: peak temperatures
sensors = ['T1','T2','T3','T4','T5','T6','T7','T8','T9']
peaks = [df[s].max() for s in sensors]
colors_bar = ['#d62728'] + ['#1f77b4']*4 + ['#2ca02c']*4
ax1.bar(sensors, peaks, color=colors_bar, edgecolor='black', linewidth=0.5)
ax1.axhline(y=42, color='gray', linestyle=':', linewidth=1, alpha=0.5, label='PCM melting (42°C)')
ax1.set_xlabel('Sensor', fontsize=11)
ax1.set_ylabel('Peak Temperature (°C)', fontsize=11)
ax1.set_title('Peak Temperature by Sensor', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Comparison with Gyroid
metrics = ['Heating\nduration\n(min)', 'T1 peak\n(°C)', 'B group\navg (°C)', 'C group\navg (°C)']
primitive_vals = [26.93, 106.80, 93.38, 63.47]
gyroid_vals = [25.40, 93.77, 87.27, 76.65]

x = np.arange(len(metrics))
width = 0.35
ax2.bar(x - width/2, primitive_vals, width, label='Primitive', color='#ff7f0e', edgecolor='black', linewidth=0.5)
ax2.bar(x + width/2, gyroid_vals, width, label='Gyroid', color='#9467bd', edgecolor='black', linewidth=0.5)
ax2.set_xlabel('Metric', fontsize=11)
ax2.set_ylabel('Value', fontsize=11)
ax2.set_title('Primitive vs Gyroid (10W)', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(metrics)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/fig_primitive_10w_summary.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/fig_primitive_10w_summary.pdf', bbox_inches='tight')
print("Saved: fig_primitive_10w_summary.png/pdf")
