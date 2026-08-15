"""
Publication-quality figure: Temperature evolution curves for three TPMS structures
at three power levels (3x3 subplot grid).

Rows: 10W, 20W, 30W
Columns: Gyroid, IWP, Primitive
Each subplot: T1 (heater), B-group (interior), C-group (surface) vs time
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import warnings
warnings.filterwarnings('ignore')

mpl.rcParams.update({
    'font.family': 'Arial',
    'font.size': 7,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.minor.width': 0.4,
    'ytick.minor.width': 0.4,
    'lines.linewidth': 1.0,
    'legend.frameon': False,
    'legend.fontsize': 6,
    'axes.labelsize': 7,
    'axes.titlesize': 8,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'mathtext.fontset': 'dejavusans',
})

MM = 1.0 / 25.4
FIG_W = 180 * MM
FIG_H = 120 * MM

STRUCTURE_COLORS = {
    'Gyroid': '#1f77b4',
    'IWP': '#9467bd',
    'Primitive': '#d62728',
}

PCM_MELTING_POINT = 42.0

DATA_FILES = {
    (10, 'Gyroid'):    'temperature_record_20260808_165138gyroid10w.csv',
    (10, 'IWP'):       'temperature_record_20260809_170915 (1).xlsx',
    (10, 'Primitive'): 'temperature_record_20260805_200423.csv',
    (20, 'Gyroid'):    'temperature_record_20260808_190451 (4).csv',
    (20, 'IWP'):       'temperature_record_20260809_201218iwp20w.csv',
    (20, 'Primitive'): 'temperature_record_20260806_214551.csv',
    (30, 'Gyroid'):    'temperature_record_20260808_203206.csv',
    (30, 'IWP'):       'temperature_record_20260810_152336iwp30w.csv',
    (30, 'Primitive'): 'temperature_record_20260807_193935.csv',
}

B_GROUP_COLS = {
    'Gyroid': ['T2', 'T3', 'T5'],
    'IWP': ['T2', 'T3'],
    'Primitive': ['T2', 'T3', 'T5'],
}

C_GROUP_COLS = {
    'Gyroid': ['T9'],
    'IWP': ['T8', 'T9'],
    'Primitive': ['T9'],
}


def load_csv_data(path, structure):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
    for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['time'] = pd.to_datetime(df['time'])
    df = df.dropna(subset=['T1']).reset_index(drop=True)
    df['elapsed_s'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    df['elapsed_min'] = df['elapsed_s'] / 60.0
    return df


def load_xlsx_data(path, structure):
    df = pd.read_excel(path)
    df.columns = ['time', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
    for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['time'] = pd.to_datetime(df['time'])
    df = df.dropna(subset=['T1']).reset_index(drop=True)
    df['elapsed_s'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    df['elapsed_min'] = df['elapsed_s'] / 60.0
    return df


def load_iwp_csv_data(path, structure):
    """Load IWP CSV data with proper time handling.
    IWP data files have minute-precision timestamps, so we use row index as seconds (1 Hz sampling).
    """
    for enc in ['utf-8-sig', 'gbk', 'latin1']:
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    df.columns = ['time', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
    for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=['T1']).reset_index(drop=True)
    # IWP data has minute-precision timestamps, use row index as seconds (1 Hz sampling)
    df['elapsed_s'] = df.index.astype(float)
    df['elapsed_min'] = df['elapsed_s'] / 60.0
    return df


def downsample(df, factor=5):
    return df.iloc[::factor].reset_index(drop=True)


def lighten_color(hex_color, factor=0.4):
    rgb = mpl.colors.to_rgb(hex_color)
    return tuple(c + (1 - c) * factor for c in rgb)


def plot_subplot(ax, df, structure, power, show_xlabel, show_ylabel, show_legend):
    color = STRUCTURE_COLORS[structure]
    color_b = lighten_color(color, 0.25)
    color_c = lighten_color(color, 0.50)

    b_cols = B_GROUP_COLS[structure]
    c_cols = C_GROUP_COLS[structure]

    t = df['elapsed_min'].values
    t1 = df['T1'].values
    b_avg = df[b_cols].mean(axis=1).values
    c_avg = df[c_cols].mean(axis=1).values

    ax.plot(t, t1, color=color, linewidth=1.0, label='$T_1$ (heater)', zorder=5)
    ax.plot(t, b_avg, color=color_b, linewidth=0.9, linestyle='--',
            label='$T_B$ (interior)', zorder=4)
    ax.plot(t, c_avg, color=color_c, linewidth=0.9, linestyle='-.',
            label='$T_C$ (surface)', zorder=3)

    ax.axhline(PCM_MELTING_POINT, color='#666666', linewidth=0.6,
               linestyle=':', alpha=0.7, zorder=2)

    if show_ylabel:
        ax.set_ylabel('Temperature (°C)')
    if show_xlabel:
        ax.set_xlabel('Time (min)')

    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.grid(True, which='major', alpha=0.25, linewidth=0.4)
    ax.grid(True, which='minor', alpha=0.1, linewidth=0.3)

    if power == 10:
        ax.set_ylim(20, 115)
    elif power == 20:
        ax.set_ylim(20, 125)
    else:
        ax.set_ylim(20, 140)

    ax.set_xlim(0, None)

    if show_legend:
        ax.legend(loc='upper left', frameon=True, framealpha=0.85,
                  edgecolor='#cccccc', fontsize=5.5, handlelength=1.5,
                  borderpad=0.3, labelspacing=0.3)

    for spine in ax.spines.values():
        spine.set_linewidth(0.6)


def main():
    datasets = {}
    for (power, structure), fname in DATA_FILES.items():
        path = fname
        print(f"Loading {structure} {power}W: {path}")
        if fname.endswith('.xlsx'):
            df = load_xlsx_data(path, structure)
        elif 'iwp20w' in fname.lower() or 'iwp30w' in fname.lower():
            df = load_iwp_csv_data(path, structure)
        else:
            df = load_csv_data(path, structure)
        
        # Primitive 30W: truncate at T1 maximum (remove cooling section)
        if structure == 'Primitive' and power == 30:
            max_idx = df['T1'].idxmax()
            df = df.iloc[:max_idx + 1].reset_index(drop=True)
            print(f"  -> Truncated at T1 max (row {max_idx}), keeping {len(df)} rows")
        
        datasets[(power, structure)] = downsample(df, factor=3)
        print(f"  -> {len(df)} rows, {df['elapsed_min'].max():.1f} min")

    fig, axes = plt.subplots(3, 3, figsize=(FIG_W, FIG_H),
                             constrained_layout=True)

    powers = [10, 20, 30]
    structures = ['Gyroid', 'IWP', 'Primitive']
    power_labels = ['(a) 10 W', '(b) 20 W', '(c) 30 W']

    for j, structure in enumerate(structures):
        color = STRUCTURE_COLORS[structure]
        axes[0, j].set_title(f'{structure}', color=color, fontweight='bold',
                             pad=5)

    for i, power in enumerate(powers):
        axes[i, 0].text(-0.35, 0.5, power_labels[i], transform=axes[i, 0].transAxes,
                         rotation=90, va='center', ha='center',
                         fontsize=8, fontweight='bold')

    for i, power in enumerate(powers):
        for j, structure in enumerate(structures):
            ax = axes[i, j]
            df = datasets[(power, structure)]
            show_xlabel = (i == 2)
            show_ylabel = (j == 0)
            show_legend = (i == 0 and j == 2)
            plot_subplot(ax, df, structure, power,
                         show_xlabel, show_ylabel, show_legend)

    fig.text(0.54, 0.01, 'Time (min)', ha='center', fontsize=7.5)
    fig.text(0.02, 0.52, 'Temperature (°C)', va='center', rotation=90,
             fontsize=7.5)

    fig.text(0.92, 0.92, '$T_{melt}$ = 42 \u00b0C  (:)',
             fontsize=6, color='#666666', ha='right', va='top',
             transform=fig.transFigure,
             bbox=dict(boxstyle='round,pad=0.2', facecolor='#f5f5f5',
                       edgecolor='#cccccc', linewidth=0.4))

    out_png = 'output/paper/figures/temperature_curves.png'
    out_pdf = 'output/paper/figures/temperature_curves.pdf'
    fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    print(f"\nSaved: {out_png}")
    print(f"Saved: {out_pdf}")


if __name__ == '__main__':
    main()
