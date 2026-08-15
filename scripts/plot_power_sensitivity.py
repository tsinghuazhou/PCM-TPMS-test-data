"""
Power sensitivity analysis for three TPMS structures.
Panel A: Melting duration reduction factor (10W->20W->30W)
Panel B: A-B gradient increase factor (10W->20W->30W)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

matplotlib.use('Agg')

STYLE_PATH = Path(r"C:\Users\tsing\AppData\Roaming\com.ai4s.workbench\runtime\xdg-config\opencode\skills\publication-figures\openscience.mplstyle")
if STYLE_PATH.exists():
    plt.style.use(str(STYLE_PATH))

DATA_PATH = Path(r"D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究\output\paper\data\tpms_comprehensive_comparison.csv")
OUT_DIR = Path(r"D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究\output\paper\figures")

df = pd.read_csv(DATA_PATH)

structures = ['Gyroid', 'IWP', 'Primitive']
colors = {'Gyroid': '#2a78d6', 'IWP': '#4a3aa7', 'Primitive': '#e34948'}
transitions = ['10W→20W', '20W→30W', '10W→30W']

def get_val(power, struct, col):
    return df.loc[(df['Power'] == power) & (df['Structure'] == struct), col].values[0]

duration_reduction = {s: [] for s in structures}
gradient_increase = {s: [] for s in structures}

for s in structures:
    md_10 = get_val('10W', s, 'melting_duration')
    md_20 = get_val('20W', s, 'melting_duration')
    md_30 = get_val('30W', s, 'melting_duration')
    duration_reduction[s] = [md_10/md_20, md_20/md_30, md_10/md_30]

    ab_10 = get_val('10W', s, 'ab_42')
    ab_20 = get_val('20W', s, 'ab_42')
    ab_30 = get_val('30W', s, 'ab_42')
    gradient_increase[s] = [ab_20/ab_10, ab_30/ab_20, ab_30/ab_10]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(180/25.4, 80/25.4))

x = np.arange(len(transitions))
width = 0.22
offsets = [-width, 0, width]

for i, s in enumerate(structures):
    vals = duration_reduction[s]
    bars = ax1.bar(x + offsets[i], vals, width, label=s, color=colors[s],
                   edgecolor='white', linewidth=0.5, zorder=3)
    for bar, v in zip(bars, vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                 f'{v:.1f}×', ha='center', va='bottom', fontsize=6.5,
                 fontweight=600, color='#2a2723')

ax1.set_xticks(x)
ax1.set_xticklabels(transitions, fontsize=7.5)
ax1.set_ylabel('Reduction factor (×)', fontsize=8)
ax1.set_title('A', fontsize=10, fontweight=700, loc='left', pad=4)
ax1.set_ylim(0, max(max(duration_reduction[s]) for s in structures) * 1.25)
ax1.tick_params(axis='both', labelsize=7)
ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=False))
ax1.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.6, zorder=0)

for i, s in enumerate(structures):
    vals = gradient_increase[s]
    bars = ax2.bar(x + offsets[i], vals, width, label=s, color=colors[s],
                   edgecolor='white', linewidth=0.5, zorder=3)
    for bar, v in zip(bars, vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f'{v:.1f}×', ha='center', va='bottom', fontsize=6.5,
                 fontweight=600, color='#2a2723')

ax2.set_xticks(x)
ax2.set_xticklabels(transitions, fontsize=7.5)
ax2.set_ylabel('Increase factor (×)', fontsize=8)
ax2.set_title('B', fontsize=10, fontweight=700, loc='left', pad=4)
ax2.set_ylim(0, max(max(gradient_increase[s]) for s in structures) * 1.25)
ax2.tick_params(axis='both', labelsize=7)
ax2.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.6, zorder=0)

handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=3, fontsize=7.5,
           frameon=False, bbox_to_anchor=(0.5, 1.02), columnspacing=1.0)

fig.supxlabel('Power transition', fontsize=8, y=-0.02)

plt.tight_layout(rect=[0, 0.02, 1, 0.92])

OUT_DIR.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_DIR / 'power_sensitivity.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig(OUT_DIR / 'power_sensitivity.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)

print("Figures saved:")
print(f"  {OUT_DIR / 'power_sensitivity.png'}")
print(f"  {OUT_DIR / 'power_sensitivity.pdf'}")
print()
print("Data summary:")
for s in structures:
    print(f"  {s}: duration reduction 10W→30W = {duration_reduction[s][2]:.1f}×, "
          f"A-B gradient increase 10W→30W = {gradient_increase[s][2]:.1f}×")
