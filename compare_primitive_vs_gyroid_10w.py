import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

G = load('temperature_record_20260804_163501.csv')  # Gyroid 10W
P = load('temperature_record_20260805_200423.csv')  # Primitive 10W

EMA = 0.4
def ema(s, a=EMA): return s.ewm(alpha=a, adjust=False).mean()

for name, df in [('Gyroid', G), ('Primitive', P)]:
    for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
        df[f'{c}_ema'] = ema(df[c])

# --- 1. Basic info ---
print("=" * 70)
print("PRIMITIVE vs GYROID at 10W — Detailed Comparison")
print("=" * 70)
print(f"\n{'':20s} {'Gyroid':>12s} {'Primitive':>12s} {'Ratio':>8s}")
print("-" * 55)
print(f"{'Records':20s} {len(G):>12d} {len(P):>12d}")
print(f"{'Duration (s)':20s} {G['elapsed'].iloc[-1]:>12.0f} {P['elapsed'].iloc[-1]:>12.0f} {P['elapsed'].iloc[-1]/G['elapsed'].iloc[-1]:>7.2f}x")
print(f"{'Duration (min)':20s} {G['elapsed'].iloc[-1]/60:>12.2f} {P['elapsed'].iloc[-1]/60:>12.2f}")

# --- 2. Peak temperatures ---
print(f"\n{'='*70}")
print("PEAK TEMPERATURES")
print(f"{'='*70}")
print(f"{'Sensor':8s} {'Gyroid peak':>12s} {'Prim peak':>12s} {'Δ (P-G)':>10s}")
print("-" * 45)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    gp = G[c].max()
    pp = P[c].max()
    print(f"{c:8s} {gp:>12.2f} {pp:>12.2f} {pp-gp:>+10.2f}")

# --- 3. Time to reach 42°C (PCM melting point) ---
print(f"\n{'='*70}")
print("TIME TO REACH 42°C (PCM MELTING POINT)")
print(f"{'='*70}")
print(f"{'Sensor':8s} {'Gyroid (s)':>12s} {'Prim (s)':>12s} {'Δ (s)':>10s}")
print("-" * 45)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    gt = G.loc[G[c] >= 42, 'elapsed']
    pt = P.loc[P[c] >= 42, 'elapsed']
    g_time = gt.iloc[0] if len(gt) > 0 else float('inf')
    p_time = pt.iloc[0] if len(pt) > 0 else float('inf')
    delta = p_time - g_time if (g_time < float('inf') and p_time < float('inf')) else float('nan')
    g_str = f"{g_time:.0f}" if g_time < float('inf') else "never"
    p_str = f"{p_time:.0f}" if p_time < float('inf') else "never"
    d_str = f"{delta:+.0f}" if not np.isnan(delta) else "—"
    print(f"{c:8s} {g_str:>12s} {p_str:>12s} {d_str:>10s}")

# --- 4. Heating rate (°C/min) in first 5 minutes ---
print(f"\n{'='*70}")
print("HEATING RATE (°C/min) — first 5 minutes (EMA smoothed)")
print(f"{'='*70}")
t5 = 300  # 5 min
print(f"{'Sensor':8s} {'Gyroid':>12s} {'Prim':>12s} {'Δ':>10s}")
print("-" * 45)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    g_mask = G['elapsed'] <= t5
    p_mask = P['elapsed'] <= t5
    g_rate = (G.loc[g_mask, f'{c}_ema'].iloc[-1] - G.loc[g_mask, f'{c}_ema'].iloc[0]) / (G.loc[g_mask, 'elapsed'].iloc[-1] / 60)
    p_rate = (P.loc[p_mask, f'{c}_ema'].iloc[-1] - P.loc[p_mask, f'{c}_ema'].iloc[0]) / (P.loc[p_mask, 'elapsed'].iloc[-1] / 60)
    print(f"{c:8s} {g_rate:>12.3f} {p_rate:>12.3f} {p_rate-g_rate:>+10.3f}")

# --- 5. Group averages at key timepoints ---
print(f"\n{'='*70}")
print("GROUP AVERAGES AT KEY TIMEPOINTS")
print(f"{'='*70}")
groups = {'A': ['T1'], 'B': ['T2','T3','T4','T5'], 'C': ['T6','T7','T8','T9']}

# At T=300s (5min), T=600s (10min), T=900s (15min), T=1200s (20min)
for t_target in [300, 600, 900, 1200, 1500]:
    print(f"\n--- t = {t_target}s ({t_target/60:.0f}min) ---")
    print(f"{'Group':8s} {'Gyroid':>10s} {'Prim':>10s} {'Δ':>10s}")
    for gname, cols in groups.items():
        g_idx = G['elapsed'].sub(t_target).abs().idxmin()
        p_idx = P['elapsed'].sub(t_target).abs().idxmin()
        g_avg = G.loc[g_idx, cols].mean()
        p_avg = P.loc[p_idx, cols].mean()
        print(f"{gname:8s} {g_avg:>10.2f} {p_avg:>10.2f} {p_avg-g_avg:>+10.2f}")

# --- 6. Temperature gradients over time ---
print(f"\n{'='*70}")
print("TEMPERATURE GRADIENTS — AT T1 PEAK")
print(f"{'='*70}")
g_peak_idx = G['T1'].idxmax()
p_peak_idx = P['T1'].idxmax()
print(f"{'Gradient':12s} {'Gyroid':>10s} {'Prim':>10s} {'Ratio':>8s}")
print("-" * 45)
for gname, cols in groups.items():
    pass
g_a = G['T1'].iloc[g_peak_idx]
p_a = P['T1'].iloc[p_peak_idx]
g_b = G[['T2','T3','T4','T5']].iloc[g_peak_idx].mean()
p_b = P[['T2','T3','T4','T5']].iloc[p_peak_idx].mean()
g_c = G[['T6','T7','T8','T9']].iloc[g_peak_idx].mean()
p_c = P[['T6','T7','T8','T9']].iloc[p_peak_idx].mean()

for label, gv, pv in [('A-B', g_a-g_b, p_a-p_b), ('A-C', g_a-g_c, p_a-p_c), ('B-C', g_b-g_c, p_b-p_c)]:
    ratio = pv/gv if gv != 0 else float('inf')
    print(f"{label:12s} {gv:>10.2f} {pv:>10.2f} {ratio:>7.2f}x")

# --- 7. Within-group uniformity (std) ---
print(f"\n{'='*70}")
print("WITHIN-GROUP UNIFORMITY — std at T1 peak")
print(f"{'='*70}")
print(f"{'Group':8s} {'Gyroid std':>12s} {'Prim std':>12s}")
print("-" * 35)
for gname, cols in groups.items():
    g_std = G.loc[g_peak_idx, cols].std()
    p_std = P.loc[p_peak_idx, cols].std()
    print(f"{gname:8s} {g_std:>12.2f} {p_std:>12.2f}")

# --- 8. Plateau detection (dT/dt near zero = phase change) ---
print(f"\n{'='*70}")
print("PLATEAU DETECTION — dT/dt < 0.05°C/s for ≥30s")
print(f"{'='*70}")
for name, df in [('Gyroid', G), ('Primitive', P)]:
    dt = df['elapsed'].diff()
    dT1 = df['T1_ema'].diff()
    rate = dT1 / dt
    plateau = rate.abs() < 0.05
    # Find contiguous plateau segments >= 30s
    segments = []
    start = None
    for i in range(len(plateau)):
        if plateau.iloc[i] and start is None:
            start = i
        elif not plateau.iloc[i] and start is not None:
            dur = df['elapsed'].iloc[i-1] - df['elapsed'].iloc[start]
            if dur >= 30:
                segments.append((df['elapsed'].iloc[start], df['elapsed'].iloc[i-1], dur))
            start = None
    if start is not None:
        dur = df['elapsed'].iloc[-1] - df['elapsed'].iloc[start]
        if dur >= 30:
            segments.append((df['elapsed'].iloc[start], df['elapsed'].iloc[-1], dur))
    print(f"\n{name}:")
    if segments:
        for s, e, d in segments:
            t1_start = df.loc[df['elapsed'] >= s, 'T1_ema'].iloc[0]
            t1_end = df.loc[df['elapsed'] <= e, 'T1_ema'].iloc[-1]
            print(f"  Plateau: {s:.0f}s - {e:.0f}s (dur={d:.0f}s={d/60:.1f}min), T1: {t1_start:.1f}→{t1_end:.1f}°C")
    else:
        print("  No plateau detected (dT/dt < 0.05°C/s for ≥30s)")

# --- 9. T7 outlier analysis ---
print(f"\n{'='*70}")
print("T7 OUTLIER ANALYSIS")
print(f"{'='*70}")
print(f"\nGyroid T7 at peak: {G['T7'].iloc[g_peak_idx]:.2f}°C (C group avg: {g_c:.2f}°C)")
print(f"Primitive T7 at peak: {P['T7'].iloc[p_peak_idx]:.2f}°C (C group avg: {p_c:.2f}°C)")
print(f"\nGyroid T7 deviation from C avg: {G['T7'].iloc[g_peak_idx] - g_c:+.2f}°C")
print(f"Primitive T7 deviation from C avg: {P['T7'].iloc[p_peak_idx] - p_c:+.2f}°C")

# Check if T7 is consistently low in Primitive
print(f"\nPrimitive C-group sensor averages over entire experiment:")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: mean={P[c].mean():.2f}°C, max={P[c].max():.2f}°C")
print(f"\nGyroid C-group sensor averages over entire experiment:")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: mean={G[c].mean():.2f}°C, max={G[c].max():.2f}°C")

# --- 10. Energy absorption efficiency ---
print(f"\n{'='*70}")
print("ENERGY ABSORPTION COMPARISON")
print(f"{'='*70}")
print(f"Same input power (10W), same duration proxy:")
print(f"  Gyroid T1 rise: {G['T1'].max() - G['T1'].iloc[0]:.2f}°C")
print(f"  Primitive T1 rise: {P['T1'].max() - P['T1'].iloc[0]:.2f}°C")
print(f"  → Primitive T1 rises {(P['T1'].max()-P['T1'].iloc[0])/(G['T1'].max()-G['T1'].iloc[0]):.2f}x more for same power")
print(f"  → Suggests Primitive stores less energy in PCM (less effective heat spreading)")
print(f"")
print(f"  Gyroid mean all-sensor rise: {np.mean([G[c].max()-G[c].iloc[0] for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']]):.2f}°C")
print(f"  Primitive mean all-sensor rise: {np.mean([P[c].max()-P[c].iloc[0] for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']]):.2f}°C")
