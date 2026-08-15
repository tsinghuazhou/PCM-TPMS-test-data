import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['axes.linewidth'] = 1.0
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'

STYLE = Path(r'C:\Users\tsing\AppData\Roaming\com.ai4s.workbench\runtime\xdg-config\opencode\skills\publication-figures\openscience.mplstyle')
if STYLE.exists():
    plt.style.use(str(STYLE))

BASE = Path(r'D:\qqhru.edu.cn\日新Rx102科研组 - General\openscience\PCM材料在TPMS晶格下的实验分析研究')
CSV = BASE / 'output' / 'paper' / 'data' / 'tpms_comprehensive_comparison.csv'
OUT_DIR = BASE / 'output' / 'paper' / 'figures'

df = pd.read_csv(CSV)

structures = ['Gyroid', 'IWP', 'Primitive']
powers = ['10W', '20W', '30W']
colors = {'Gyroid': '#2171b5', 'IWP': '#756bb1', 'Primitive': '#cb181d'}
markers_map = {'Gyroid': 'o', 'IWP': 's', 'Primitive': 'D'}

melt = {}
grad = {}
for _, row in df.iterrows():
    p = row['Power']
    s = row['Structure']
    melt[(p, s)] = row['melting_duration']
    grad[(p, s)] = row['ab_42']

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(180 / 25.4, 80 / 25.4))

x = np.arange(len(powers))
width = 0.22

for i, struct in enumerate(structures):
    vals = [melt[(p, struct)] for p in powers]
    bars = ax_a.bar(x + i * width, vals, width, label=struct,
                    color=colors[struct], alpha=0.88, edgecolor='white',
                    linewidth=0.6, zorder=3)
    for bar, val in zip(bars, vals):
        fmt = f'{val:.2f}' if val < 1 else f'{val:.1f}'
        ax_a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                  fmt, ha='center', va='bottom', fontsize=6.0, fontweight='bold')

ax_a.set_xlabel('Heating Power', fontsize=8.5)
ax_a.set_ylabel('Melting Duration (min)', fontsize=8.5)
ax_a.set_title('(a) Melting Duration by Structure', fontsize=9, fontweight='bold')
ax_a.set_xticks(x + width)
ax_a.set_xticklabels(powers, fontsize=8)
ax_a.tick_params(axis='y', labelsize=7.5)
ax_a.grid(True, axis='y', alpha=0.15, linewidth=0.5, zorder=0)
ax_a.set_ylim(0, 15.5)

arrow_style = dict(arrowstyle='->,head_width=0.3,head_length=0.2',
                   color='#d62728', lw=1.4, mutation_scale=12)

for p_idx, p in enumerate(['20W', '30W']):
    g_val = melt[(p, 'Gyroid')]
    i_val = melt[(p, 'IWP')]
    x_g = p_idx + 1 + 0 * width + width / 2
    x_i = p_idx + 1 + 1 * width + width / 2
    y_g = g_val
    y_i = i_val
    mid_y = max(y_g, y_i) + 0.8
    ax_a.annotate('', xy=(x_g, y_g + 0.35), xytext=(x_i, y_i + 0.35),
                  arrowprops=dict(arrowstyle='->,head_width=0.25,head_length=0.15',
                                  color='#d62728', lw=1.3, connectionstyle='arc3,rad=-0.3',
                                  mutation_scale=10))

rev_x = 1.0 + width
rev_y = 13.8
ax_a.annotate('Performance Ranking\nReversal', xy=(rev_x, 12.5),
              xytext=(rev_x - 0.55, rev_y),
              fontsize=6.2, fontweight='bold', color='#d62728',
              ha='center', va='center',
              bbox=dict(boxstyle='round,pad=0.3', fc='#fff5f5', ec='#d62728',
                        lw=0.8, alpha=0.9),
              arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.0,
                              connectionstyle='arc3,rad=0.2'))

ax_a.legend(fontsize=6.5, loc='upper right', framealpha=0.9, edgecolor='#cccccc')

for i, struct in enumerate(structures):
    vals = [grad[(p, struct)] for p in powers]
    bars = ax_b.bar(x + i * width, vals, width, label=struct,
                    color=colors[struct], alpha=0.88, edgecolor='white',
                    linewidth=0.6, zorder=3)
    for bar, val in zip(bars, vals):
        ax_b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                  f'{val:.1f}', ha='center', va='bottom', fontsize=6.0, fontweight='bold')

ax_b.set_xlabel('Heating Power', fontsize=8.5)
ax_b.set_ylabel('A\u2013B Gradient at T1=42\u00b0C (\u00b0C)', fontsize=8.5)
ax_b.set_title('(b) Thermal Uniformity (Lower = Better)', fontsize=9, fontweight='bold')
ax_b.set_xticks(x + width)
ax_b.set_xticklabels(powers, fontsize=8)
ax_b.tick_params(axis='y', labelsize=7.5)
ax_b.grid(True, axis='y', alpha=0.15, linewidth=0.5, zorder=0)
ax_b.set_ylim(0, 20)

for p_idx, p in enumerate(powers):
    g_val = grad[(p, 'Gyroid')]
    for j, struct in enumerate(['IWP', 'Primitive']):
        s_val = grad[(p, struct)]
        pct = (s_val - g_val) / g_val * 100
        x_s = p_idx + (j + 1) * width + width / 2
        ax_b.annotate(f'{pct:.0f}%\u2191', xy=(x_s, s_val + 0.3),
                      fontsize=5.5, color=colors[struct], ha='center',
                      va='bottom', fontweight='bold')

ax_b.legend(fontsize=6.5, loc='upper left', framealpha=0.9, edgecolor='#cccccc')

fig.subplots_adjust(wspace=0.35, left=0.07, right=0.97, top=0.93, bottom=0.15)

for ext in ['.png', '.pdf']:
    out = OUT_DIR / f'performance_ranking{ext}'
    fig.savefig(str(out), dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')

plt.close(fig)
print('Done.')
