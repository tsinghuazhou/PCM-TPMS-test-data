import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Load data
gyroid_file = 'tpms_gyroid20w_20260731_195755.csv'
primitive_file = 'tpms_primitive20w_20260806_214551.csv'

df_g = pd.read_csv(gyroid_file, parse_dates=['时间戳'])
df_p = pd.read_csv(primitive_file, parse_dates=['时间戳'])

# Calculate elapsed time
df_g['elapsed'] = (df_g['时间戳'] - df_g['时间戳'].min()).dt.total_seconds()
df_p['elapsed'] = (df_p['时间戳'] - df_p['时间戳'].min()).dt.total_seconds()

# Remove outliers (same as analysis script)
# Gyroid: B-group remove T4, C-group remove T9
gyroid_b = df_g[['T2', 'T3', 'T5']].mean(axis=1)
gyroid_c = df_g[['T6', 'T7', 'T8']].mean(axis=1)

# Primitive: B-group remove T3, C-group only T7
primitive_b = df_p[['T2', 'T4', 'T5']].mean(axis=1)
primitive_c = df_p['T7']

# Create figure
fig = plt.figure(figsize=(16, 12))
gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

# Plot 1: Temperature curves - Group A (heater)
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df_g['elapsed']/60, df_g['T1'], 'r-', linewidth=2, label='Gyroid', alpha=0.7)
ax1.plot(df_p['elapsed']/60, df_p['T1'], 'b-', linewidth=2, label='Primitive', alpha=0.7)
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('Group A: Heater Surface (T1)', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.axhline(y=144.7, color='r', linestyle='--', alpha=0.3, label='Gyroid peak')
ax1.axhline(y=113.0, color='b', linestyle='--', alpha=0.3, label='Primitive peak')

# Plot 2: Temperature curves - Group B (mid layer)
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(df_g['elapsed']/60, gyroid_b, 'r-', linewidth=2, label='Gyroid', alpha=0.7)
ax2.plot(df_p['elapsed']/60, primitive_b, 'b-', linewidth=2, label='Primitive', alpha=0.7)
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Temperature (°C)')
ax2.set_title('Group B: Mid Layer (T2-T5 avg)', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Temperature gradients over time
ax3 = fig.add_subplot(gs[1, 0])
gyroid_grad_ab = df_g['T1'] - gyroid_b
gyroid_grad_ac = df_g['T1'] - gyroid_c
primitive_grad_ab = df_p['T1'] - primitive_b
primitive_grad_ac = df_p['T1'] - primitive_c

ax3.plot(df_g['elapsed']/60, gyroid_grad_ab, 'r-', linewidth=2, label='Gyroid A-B', alpha=0.7)
ax3.plot(df_g['elapsed']/60, gyroid_grad_ac, 'r--', linewidth=2, label='Gyroid A-C', alpha=0.7)
ax3.plot(df_p['elapsed']/60, primitive_grad_ab, 'b-', linewidth=2, label='Primitive A-B', alpha=0.7)
ax3.plot(df_p['elapsed']/60, primitive_grad_ac, 'b--', linewidth=2, label='Primitive A-C', alpha=0.7)
ax3.set_xlabel('Time (min)')
ax3.set_ylabel('Temperature Gradient (°C)')
ax3.set_title('Temperature Gradients Over Time', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Performance reversal bar chart (10W vs 20W)
ax4 = fig.add_subplot(gs[1, 1])
metrics = ['T1\n(heater)', 'B group\n(mid)', 'A-C\ngradient']
gyroid_10w = [93.8, 87.3, 17.1]
primitive_10w = [106.8, 93.0, 36.8]
gyroid_20w = [144.7, 81.0, 65.8]
primitive_20w = [113.0, 87.2, 45.9]

x = np.arange(len(metrics))
width = 0.2

bars1 = ax4.bar(x - 1.5*width, gyroid_10w, width, label='Gyroid 10W', color='salmon', alpha=0.7)
bars2 = ax4.bar(x - 0.5*width, primitive_10w, width, label='Primitive 10W', color='lightcoral', alpha=0.7)
bars3 = ax4.bar(x + 0.5*width, gyroid_20w, width, label='Gyroid 20W', color='lightblue', alpha=0.7)
bars4 = ax4.bar(x + 1.5*width, primitive_20w, width, label='Primitive 20W', color='steelblue', alpha=0.7)

ax4.set_ylabel('Temperature (°C)')
ax4.set_title('Performance Reversal: 10W vs 20W', fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(metrics)
ax4.legend(loc='upper left', fontsize=8)
ax4.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=7)

# Plot 5: Heating rates comparison
ax5 = fig.add_subplot(gs[2, 0])
locations = ['Heater\n(T1)', 'Mid layer\n(B)', 'Top surface\n(C)']
gyroid_rates = [26.50, 4.69, 4.54]
primitive_rates = [12.09, 4.71, 3.00]

x = np.arange(len(locations))
width = 0.35

bars1 = ax5.bar(x - width/2, gyroid_rates, width, label='Gyroid', color='salmon', alpha=0.7)
bars2 = ax5.bar(x + width/2, primitive_rates, width, label='Primitive', color='steelblue', alpha=0.7)

ax5.set_ylabel('Heating Rate (°C/min)')
ax5.set_title('Heating Rates (First 3 Minutes)', fontweight='bold')
ax5.set_xticks(x)
ax5.set_xticklabels(locations)
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9)

# Plot 6: Time to reach 42°C (PCM melting)
ax6 = fig.add_subplot(gs[2, 1])
locations = ['Heater\n(T1)', 'Mid layer\n(B)', 'Top surface\n(C)']
gyroid_times = [13, 416, 422]
primitive_times = [69, 346, 500]

x = np.arange(len(locations))
width = 0.35

bars1 = ax6.bar(x - width/2, gyroid_times, width, label='Gyroid', color='salmon', alpha=0.7)
bars2 = ax6.bar(x + width/2, primitive_times, width, label='Primitive', color='steelblue', alpha=0.7)

ax6.set_ylabel('Time to 42°C (s)')
ax6.set_title('PCM Melting Time (Time to Reach 42°C)', fontweight='bold')
ax6.set_xticks(x)
ax6.set_xticklabels(locations)
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}s',
                ha='center', va='bottom', fontsize=9)

# Add overall title
fig.suptitle('Gyroid vs Primitive at 20W: Power-Dependent Performance Reversal', 
             fontsize=16, fontweight='bold', y=0.98)

# Save
plt.savefig('output/paper/figures/gyroid_vs_primitive_20w_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_vs_primitive_20w_analysis.pdf', bbox_inches='tight')
print('Saved: gyroid_vs_primitive_20w_analysis.png/pdf')

# Create a second figure showing the temporal evolution
fig2, axes = plt.subplots(2, 3, figsize=(18, 10))

# Timepoint comparisons
timepoints = [120, 240, 360, 480, 600, 660]
time_labels = ['2 min', '4 min', '6 min', '8 min', '10 min', '11 min']

for idx, (t, label) in enumerate(zip(timepoints, time_labels)):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]
    
    # Get temperatures at this timepoint
    g_idx = (df_g['elapsed'] - t).abs().idxmin()
    p_idx = (df_p['elapsed'] - t).abs().idxmin()
    
    g_a = df_g.loc[g_idx, 'T1']
    g_b = gyroid_b.iloc[g_idx]
    g_c = gyroid_c.iloc[g_idx]
    
    p_a = df_p.loc[p_idx, 'T1']
    p_b = primitive_b.iloc[p_idx]
    p_c = primitive_c.iloc[p_idx]
    
    # Bar chart
    x = np.arange(3)
    width = 0.35
    ax.bar(x - width/2, [g_a, g_b, g_c], width, label='Gyroid', color='salmon', alpha=0.7)
    ax.bar(x + width/2, [p_a, p_b, p_c], width, label='Primitive', color='steelblue', alpha=0.7)
    
    ax.set_xlabel('Location')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(f'{label}', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['A\n(heater)', 'B\n(mid)', 'C\n(top)'])
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 160)
    
    # Add gradient annotations
    g_grad = g_a - g_c
    p_grad = p_a - p_c
    ax.text(0.5, 0.95, f'Gyroid A-C: {g_grad:.1f}°C\nPrimitive A-C: {p_grad:.1f}°C',
            transform=ax.transAxes, fontsize=8, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig2.suptitle('Temperature Distribution Evolution Over Time', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_vs_primitive_20w_temporal.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_vs_primitive_20w_temporal.pdf', bbox_inches='tight')
print('Saved: gyroid_vs_primitive_20w_temporal.png/pdf')

print('\nVisualization complete.')
