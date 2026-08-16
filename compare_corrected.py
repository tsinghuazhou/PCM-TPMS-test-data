import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def remove_worst_and_avg(df, cols):
    """Remove the sensor with largest mean absolute deviation from group mean, average remaining 3."""
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

G = load('tpms_gyroid10w_20260804_163501.csv')
P = load('tpms_primitive10w_20260805_200423.csv')

print("=" * 70)
print("PRIMITIVE vs GYROID at 10W — Corrected Statistical Method")
print("Sensor layout:")
print("  T1: bottom center (heater contact)")
print("  T2-T5: 10mm below top surface (symmetric)")
print("  T6-T9: top surface (symmetric)")
print("Method: remove worst-deviation sensor from each 4-sensor layer, avg remaining 3")
print("=" * 70)

# --- Primitive: remove worst, average remaining ---
raw_b_p, worst_b_p, rem_b_p = remove_worst_and_avg(P, ['T2','T3','T4','T5'])
smooth_b_p = apply_ema(raw_b_p)
raw_c_p, worst_c_p, rem_c_p = remove_worst_and_avg(P, ['T6','T7','T8','T9'])
smooth_c_p = apply_ema(raw_c_p)

# --- Gyroid: remove worst, average remaining ---
raw_b_g, worst_b_g, rem_b_g = remove_worst_and_avg(G, ['T2','T3','T4','T5'])
smooth_b_g = apply_ema(raw_b_g)
raw_c_g, worst_c_g, rem_c_g = remove_worst_and_avg(G, ['T6','T7','T8','T9'])
smooth_c_g = apply_ema(raw_c_g)

print(f"\n--- Outlier Removal ---")
print(f"Gyroid:    B group removed {worst_b_g} (kept {rem_b_g})")
print(f"           C group removed {worst_c_g} (kept {rem_c_g})")
print(f"Primitive: B group removed {worst_b_p} (kept {rem_b_p})")
print(f"           C group removed {worst_c_p} (kept {rem_c_p})")

# --- Basic info ---
print(f"\n{'='*70}")
print("BASIC INFO")
print(f"{'='*70}")
print(f"{'':25s} {'Gyroid':>12s} {'Primitive':>12s}")
print(f"{'Records':25s} {len(G):>12d} {len(P):>12d}")
print(f"{'Duration (min)':25s} {G['elapsed'].iloc[-1]/60:>12.2f} {P['elapsed'].iloc[-1]/60:>12.2f}")

# --- Peak temps ---
print(f"\n{'='*70}")
print("PEAK TEMPERATURES (raw sensor values)")
print(f"{'='*70}")
print(f"{'Sensor':8s} {'Gyroid':>10s} {'Prim':>10s} {'Δ(P-G)':>10s}")
print("-" * 42)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    gp = G[c].max()
    pp = P[c].max()
    print(f"{c:8s} {gp:>10.2f} {pp:>10.2f} {pp-gp:>+10.2f}")

# --- Group stats (corrected) ---
print(f"\n{'='*70}")
print("GROUP STATISTICS (corrected: worst removed, avg of 3)")
print(f"{'='*70}")

# Peak values of group averages
g_a_peak = G['T1'].max()
p_a_peak = P['T1'].max()
g_b_peak = raw_b_g.max()
p_b_peak = raw_b_p.max()
g_c_peak = raw_c_g.max()
p_c_peak = raw_c_p.max()

print(f"\n--- Peak group averages ---")
print(f"{'Group':8s} {'Gyroid':>10s} {'Prim':>10s} {'Δ(P-G)':>10s}")
print("-" * 42)
for name, gv, pv in [('A (T1)', g_a_peak, p_a_peak), 
                       ('B (mid)', g_b_peak, p_b_peak),
                       ('C (top)', g_c_peak, p_c_peak)]:
    print(f"{name:8s} {gv:>10.2f} {pv:>10.2f} {pv-gv:>+10.2f}")

# --- Temperature gradients at T1 peak ---
print(f"\n--- Temperature gradients at T1 peak ---")
g_idx = G['T1'].idxmax()
p_idx = P['T1'].idxmax()

g_a = G['T1'].iloc[g_idx]
p_a = P['T1'].iloc[p_idx]
g_b = raw_b_g[g_idx]
p_b = raw_b_p[p_idx]
g_c = raw_c_g[g_idx]
p_c = raw_c_p[p_idx]

print(f"{'Gradient':12s} {'Gyroid':>10s} {'Prim':>10s} {'Ratio':>8s}")
print("-" * 45)
for label, gv, pv in [('A-B', g_a-g_b, p_a-p_b), ('A-C', g_a-g_c, p_a-p_c), ('B-C', g_b-g_c, p_b-p_c)]:
    ratio = pv/gv if gv != 0 else float('inf')
    print(f"{label:12s} {gv:>10.2f} {pv:>10.2f} {ratio:>7.2f}x")

# --- Time to 42°C ---
print(f"\n{'='*70}")
print("TIME TO REACH 42°C (PCM MELTING)")
print(f"{'='*70}")
print(f"{'Sensor':8s} {'Gyroid (s)':>12s} {'Prim (s)':>12s} {'Δ (s)':>10s}")
print("-" * 45)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    gt = G.loc[G[c] >= 42, 'elapsed']
    pt = P.loc[P[c] >= 42, 'elapsed']
    g_t = gt.iloc[0] if len(gt) > 0 else float('inf')
    p_t = pt.iloc[0] if len(pt) > 0 else float('inf')
    g_s = f"{g_t:.0f}" if g_t < float('inf') else "never"
    p_s = f"{p_t:.0f}" if p_t < float('inf') else "never"
    d = p_t - g_t if (g_t < float('inf') and p_t < float('inf')) else float('nan')
    d_s = f"{d:+.0f}" if not np.isnan(d) else "—"
    print(f"{c:8s} {g_s:>12s} {p_s:>12s} {d_s:>10s}")

# --- Heating rate first 5 min ---
print(f"\n{'='*70}")
print("HEATING RATE (°C/min) — first 5 min (EMA)")
print(f"{'='*70}")
t5 = 300
print(f"{'Signal':12s} {'Gyroid':>10s} {'Prim':>10s} {'Δ':>10s}")
print("-" * 45)

g_t1_rate = (G.loc[G['elapsed']<=t5, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[-1] - 
             G.loc[G['elapsed']<=t5, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[0]) / (G.loc[G['elapsed']<=t5,'elapsed'].iloc[-1]/60)
p_t1_rate = (P.loc[P['elapsed']<=t5, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[-1] - 
             P.loc[P['elapsed']<=t5, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[0]) / (P.loc[P['elapsed']<=t5,'elapsed'].iloc[-1]/60)
print(f"{'T1 (A)':12s} {g_t1_rate:>10.3f} {p_t1_rate:>10.3f} {p_t1_rate-g_t1_rate:>+10.3f}")

g_mask = (G['elapsed']<=t5).values
p_mask = (P['elapsed']<=t5).values
g_b_rate = (smooth_b_g[g_mask][-1] - smooth_b_g[g_mask][0]) / (G.loc[G['elapsed']<=t5,'elapsed'].iloc[-1]/60)
p_b_rate = (smooth_b_p[p_mask][-1] - smooth_b_p[p_mask][0]) / (P.loc[P['elapsed']<=t5,'elapsed'].iloc[-1]/60)
print(f"{'B (mid)':12s} {g_b_rate:>10.3f} {p_b_rate:>10.3f} {p_b_rate-g_b_rate:>+10.3f}")

g_c_rate = (smooth_c_g[g_mask][-1] - smooth_c_g[g_mask][0]) / (G.loc[G['elapsed']<=t5,'elapsed'].iloc[-1]/60)
p_c_rate = (smooth_c_p[p_mask][-1] - smooth_c_p[p_mask][0]) / (P.loc[P['elapsed']<=t5,'elapsed'].iloc[-1]/60)
print(f"{'C (top)':12s} {g_c_rate:>10.3f} {p_c_rate:>10.3f} {p_c_rate-g_c_rate:>+10.3f}")

# --- Group averages at key timepoints ---
print(f"\n{'='*70}")
print("GROUP AVERAGES AT KEY TIMEPOINTS (corrected)")
print(f"{'='*70}")
for t_target in [300, 600, 900, 1200, 1500]:
    g_i = G['elapsed'].sub(t_target).abs().idxmin()
    p_i = P['elapsed'].sub(t_target).abs().idxmin()
    g_a_t = G['T1'].iloc[g_i]
    p_a_t = P['T1'].iloc[p_i]
    g_b_t = raw_b_g[g_i]
    p_b_t = raw_b_p[p_i]
    g_c_t = raw_c_g[g_i]
    p_c_t = raw_c_p[p_i]
    print(f"\n--- t = {t_target}s ({t_target//60}min) ---")
    print(f"{'Group':8s} {'Gyroid':>10s} {'Prim':>10s} {'Δ':>10s}")
    for name, gv, pv in [('A', g_a_t, p_a_t), ('B', g_b_t, p_b_t), ('C', g_c_t, p_c_t)]:
        print(f"{name:8s} {gv:>10.2f} {pv:>10.2f} {pv-gv:>+10.2f}")
    print(f"{'A-B':8s} {g_a_t-g_b_t:>10.2f} {p_a_t-p_b_t:>10.2f}")
    print(f"{'A-C':8s} {g_a_t-g_c_t:>10.2f} {p_a_t-p_c_t:>10.2f}")

# --- Plateau detection ---
print(f"\n{'='*70}")
print("PLATEAU DETECTION (T1, |dT/dt| < 0.05°C/s for ≥30s)")
print(f"{'='*70}")
for name, df in [('Gyroid', G), ('Primitive', P)]:
    dt = df['elapsed'].diff()
    dT1 = df['T1'].ewm(alpha=0.4, adjust=False).mean().diff()
    rate = dT1 / dt
    plateau = rate.abs() < 0.05
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
            t1s = df.loc[df['elapsed'] >= s, 'T1'].ewm(alpha=0.4, adjust=False).mean().iloc[0]
            t1e = df.loc[df['elapsed'] <= e, 'T1'].ewm(alpha=0.4, adjust=False).mean().iloc[-1]
            print(f"  {s:.0f}s - {e:.0f}s (dur={d:.0f}s={d/60:.1f}min), T1: {t1s:.1f}→{t1e:.1f}°C")
    else:
        print("  No plateau detected")

# --- Energy analysis ---
print(f"\n{'='*70}")
print("ENERGY ABSORPTION")
print(f"{'='*70}")
g_t1_rise = G['T1'].max() - G['T1'].iloc[0]
p_t1_rise = P['T1'].max() - P['T1'].iloc[0]
g_all_rise = np.mean([G[c].max()-G[c].iloc[0] for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']])
p_all_rise = np.mean([P[c].max()-P[c].iloc[0] for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']])
print(f"T1 rise:           Gyroid={g_t1_rise:.2f}°C  Primitive={p_t1_rise:.2f}°C  ratio={p_t1_rise/g_t1_rise:.2f}x")
print(f"Mean all-sensor:   Gyroid={g_all_rise:.2f}°C  Primitive={p_all_rise:.2f}°C")
print(f"T1/mean ratio:     Gyroid={g_t1_rise/g_all_rise:.2f}  Primitive={p_t1_rise/p_all_rise:.2f}")

# --- T7 analysis ---
print(f"\n{'='*70}")
print("T7 OUTLIER ANALYSIS")
print(f"{'='*70}")
print(f"Gyroid T7:    peak={G['T7'].max():.2f}°C, mean={G['T7'].mean():.2f}°C")
print(f"Primitive T7: peak={P['T7'].max():.2f}°C, mean={P['T7'].mean():.2f}°C")
print(f"\nGyroid C-group (all 4 at peak):")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: {G[c].iloc[g_idx]:.2f}°C")
print(f"  C avg (raw): {G[['T6','T7','T8','T9']].iloc[g_idx].mean():.2f}°C")
print(f"  C avg (corrected, removed {worst_c_g}): {raw_c_g[g_idx]:.2f}°C")
print(f"\nPrimitive C-group (all 4 at peak):")
for c in ['T6','T7','T8','T9']:
    print(f"  {c}: {P[c].iloc[p_idx]:.2f}°C")
print(f"  C avg (raw): {P[['T6','T7','T8','T9']].iloc[p_idx].mean():.2f}°C")
print(f"  C avg (corrected, removed {worst_c_p}): {raw_c_p[p_idx]:.2f}°C")
