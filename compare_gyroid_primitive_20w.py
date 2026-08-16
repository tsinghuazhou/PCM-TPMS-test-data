"""
Gyroid vs Primitive 20W comparison
Gyroid 20W: tpms_gyroid20w_20260731_195755.csv (603 rows, 11.12 min)
Primitive 20W: tpms_primitive20w_20260806_214551.csv (702 rows, 11.93 min)

Note: Gyroid 20W data has contact issues (T1-B gap 64.8°C), conclusions are for reference only
"""
import pandas as pd
import numpy as np

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

G = load('tpms_gyroid20w_20260731_195755.csv')
P = load('tpms_primitive20w_20260806_214551.csv')

print("=" * 70)
print("GYROID vs PRIMITIVE at 20W - Comparative Analysis")
print("=" * 70)
print(f"\nGyroid:    {len(G)} rows, {G['elapsed'].iloc[-1]/60:.2f} min")
print(f"Primitive: {len(P)} rows, {P['elapsed'].iloc[-1]/60:.2f} min")

# Process groups
raw_b_g, worst_b_g, rem_b_g = remove_worst_and_avg(G, ['T2','T3','T4','T5'])
raw_c_g, worst_c_g, rem_c_g = remove_worst_and_avg(G, ['T6','T7','T8','T9'])

raw_b_p, worst_b_p, rem_b_p = remove_worst_and_avg(P, ['T2','T3','T4','T5'])
raw_c_p, worst_c_p, rem_c_p = remove_worst_and_avg(P, ['T6','T7','T8','T9'])

print(f"\nOutlier removal:")
print(f"  Gyroid:    B removed {worst_b_g} (kept {rem_b_g}), C removed {worst_c_g} (kept {rem_c_g})")
print(f"  Primitive: B removed {worst_b_p} (kept {rem_b_p}), C removed {worst_c_p} (kept {rem_c_p})")

# Peak temperatures
g_idx = G['T1'].idxmax()
p_idx = P['T1'].idxmax()

print(f"\n{'='*70}")
print("PEAK TEMPERATURES")
print(f"{'='*70}")
print(f"\n{'Group':<20s} {'Gyroid':>10s} {'Primitive':>10s} {'Diff':>10s}")
print("-" * 55)

a_g = G['T1'].iloc[g_idx]
a_p = P['T1'].iloc[p_idx]
print(f"{'A (T1)':<20s} {a_g:>10.2f} {a_p:>10.2f} {a_p-a_g:>+10.2f}")

b_g = raw_b_g[g_idx]
b_p = raw_b_p[p_idx]
print(f"{'B (mid, 3avg)':<20s} {b_g:>10.2f} {b_p:>10.2f} {b_p-b_g:>+10.2f}")

c_g = raw_c_g[g_idx]
c_p = raw_c_p[p_idx]
print(f"{'C (top)':<20s} {c_g:>10.2f} {c_p:>10.2f} {c_p-c_g:>+10.2f}")

# Individual sensor peaks
print(f"\n{'='*70}")
print("INDIVIDUAL SENSOR PEAKS")
print(f"{'='*70}")
print(f"\n{'Sensor':<8s} {'Gyroid':>10s} {'Primitive':>10s} {'Diff':>10s}")
print("-" * 42)
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    gv = G[c].max()
    pv = P[c].max()
    print(f"{c:<8s} {gv:>10.2f} {pv:>10.2f} {pv-gv:>+10.2f}")

# Temperature gradients
print(f"\n{'='*70}")
print("TEMPERATURE GRADIENTS (at T1 peak)")
print(f"{'='*70}")
print(f"\n{'Gradient':<12s} {'Gyroid':>10s} {'Primitive':>10s} {'Ratio':>10s}")
print("-" * 45)
for label, gv, pv in [('A-B', a_g-b_g, a_p-b_p),
                       ('A-C', a_g-c_g, a_p-c_p),
                       ('B-C', b_g-c_g, b_p-c_p)]:
    ratio = pv/gv if gv != 0 else float('inf')
    print(f"{label:<12s} {gv:>10.2f} {pv:>10.2f} {ratio:>9.2f}x")

# Time to reach 42C
print(f"\n{'='*70}")
print("TIME TO REACH 42C (PCM MELTING)")
print(f"{'='*70}")
def time_to_temp(df, vals, temp=42):
    above = df.loc[vals >= temp, 'elapsed']
    return above.iloc[0] if len(above) > 0 else float('inf')

print(f"\n{'Signal':<15s} {'Gyroid (s)':>12s} {'Prim (s)':>12s} {'Speedup':>10s}")
print("-" * 52)
for name, g_vals, p_vals in [
    ('T1 (A)', G['T1'], P['T1']),
    ('B group', pd.Series(raw_b_g), pd.Series(raw_b_p)),
    ('C group', pd.Series(raw_c_g), pd.Series(raw_c_p))]:
    gt = time_to_temp(G, g_vals)
    pt = time_to_temp(P, p_vals)
    speedup = gt/pt if pt < float('inf') else float('inf')
    print(f"{name:<15s} {gt:>12.0f} {pt:>12.0f} {speedup:>9.2f}x")

# Heating rates (first 3 min)
print(f"\n{'='*70}")
print("HEATING RATE (first 3 min, EMA smoothed)")
print(f"{'='*70}")
t3 = 180
g_mask = (G['elapsed'] <= t3).values
p_mask = (P['elapsed'] <= t3).values

def calc_rate(vals, mask, df):
    s = apply_ema(vals if isinstance(vals, np.ndarray) else vals.values)
    return (s[mask][-1] - s[mask][0]) / (df.loc[mask, 'elapsed'].iloc[-1] / 60)

print(f"\n{'Signal':<15s} {'Gyroid':>10s} {'Primitive':>10s} {'Ratio':>10s}")
print("-" * 48)
for name, g_vals, p_vals in [
    ('T1 (A)', G['T1'].values, P['T1'].values),
    ('B group', raw_b_g, raw_b_p),
    ('C group', raw_c_g, raw_c_p)]:
    gr = calc_rate(g_vals, g_mask, G)
    pr = calc_rate(p_vals, p_mask, P)
    ratio = pr/gr if gr != 0 else float('inf')
    print(f"{name:<15s} {gr:>10.3f} {pr:>10.3f} {ratio:>9.2f}x")
print(f"{'(unit: C/min)':<15s}")

# Group averages at key timepoints
print(f"\n{'='*70}")
print("GROUP AVERAGES AT KEY TIMEPOINTS")
print(f"{'='*70}")
for t_target in [120, 240, 360, 480, 600, 660]:
    g_i = G['elapsed'].sub(t_target).abs().idxmin()
    p_i = P['elapsed'].sub(t_target).abs().idxmin()
    a_g_t = G['T1'].iloc[g_i]
    b_g_t = raw_b_g[g_i]
    c_g_t = raw_c_g[g_i]
    a_p_t = P['T1'].iloc[p_i]
    b_p_t = raw_b_p[p_i]
    c_p_t = raw_c_p[p_i]
    print(f"\n--- t = {t_target}s ({t_target//60}min) ---")
    print(f"  Gyroid:    A={a_g_t:.1f}C, B={b_g_t:.1f}C, C={c_g_t:.1f}C | A-B={a_g_t-b_g_t:.1f}, A-C={a_g_t-c_g_t:.1f}")
    print(f"  Primitive: A={a_p_t:.1f}C, B={b_p_t:.1f}C, C={c_p_t:.1f}C | A-B={a_p_t-b_p_t:.1f}, A-C={a_p_t-c_p_t:.1f}")

# Energy analysis
print(f"\n{'='*70}")
print("ENERGY INPUT COMPARISON")
print(f"{'='*70}")
g_dur = G['elapsed'].iloc[-1]
p_dur = P['elapsed'].iloc[-1]
g_energy = 20 * g_dur
p_energy = 20 * p_dur
print(f"\n  Duration:    Gyroid={g_dur/60:.2f}min, Primitive={p_dur/60:.2f}min")
print(f"  Energy in:   Gyroid={g_energy/1000:.2f}kJ, Primitive={p_energy/1000:.2f}kJ")
print(f"  Energy ratio: Primitive/Gyroid = {p_energy/g_energy:.2f}x")

# T1 rise
g_t1_rise = G['T1'].max() - G['T1'].iloc[0]
p_t1_rise = P['T1'].max() - P['T1'].iloc[0]
print(f"\n  T1 rise:     Gyroid={g_t1_rise:.1f}C, Primitive={p_t1_rise:.1f}C")
print(f"  T1 rise ratio: Primitive/Gyroid = {p_t1_rise/g_t1_rise:.2f}x")

# Key findings
print(f"\n{'='*70}")
print("KEY FINDINGS SUMMARY")
print(f"{'='*70}")
print(f"""
1. T1 (heater contact):
   - Gyroid: {a_g:.1f}C, Primitive: {a_p:.1f}C
   - Gyroid runs {a_g-a_p:.1f}C HOTTER at heater surface
   - This is surprising - Gyroid transfers heat MORE efficiently to heater?
   - OR: Primitive's lower T1 suggests better heat spreading away from heater

2. B group (mid layer):
   - Gyroid: {b_g:.1f}C, Primitive: {b_p:.1f}C
   - Primitive runs {b_p-b_g:+.1f}C vs Gyroid
   
3. C group (top surface):
   - Gyroid: {c_g:.1f}C, Primitive: {c_p:.1f}C (T7 only)
   - Primitive top surface is {c_p-c_g:+.1f}C vs Gyroid

4. Temperature uniformity (A-C gradient):
   - Gyroid: {a_g-c_g:.1f}C, Primitive: {a_p-c_p:.1f}C
   - Gyroid gradient is {(a_g-c_g)/(a_p-c_p):.2f}x of Primitive
   - {'Gyroid is LESS uniform' if (a_g-c_g) > (a_p-c_p) else 'Primitive is LESS uniform'}

5. PCM melting speed:
   - Gyroid reaches 42C at B-group in {time_to_temp(G, pd.Series(raw_b_g)):.0f}s
   - Primitive reaches 42C at B-group in {time_to_temp(P, pd.Series(raw_b_p)):.0f}s
""")

print(f"{'='*70}")
print("Analysis complete.")
print(f"{'='*70}")
