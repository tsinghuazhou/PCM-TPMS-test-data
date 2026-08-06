"""
Gyroid 10W vs 20W 综合对比
- Gyroid 10W: 2026-08-04 (1239 rows, 25.38 min)
- Gyroid 20W old: 2026-08-03 (436 rows, 8.50 min)
- Gyroid 20W new: 2026-08-06 (730 rows, 12.35 min, C组仅T7)
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

# Load data
G10 = load('temperature_record_20260804_163501.csv')
G20_old = load('temperature_record_20260803_171111.csv')
G20_new = load('temperature_record_20260806_162603.csv')

print("=" * 80)
print("GYROID 10W vs 20W 综合对比")
print("=" * 80)
print(f"\n数据概览:")
print(f"  Gyroid 10W:    {len(G10)} rows, {G10['elapsed'].iloc[-1]/60:.2f} min")
print(f"  Gyroid 20W旧:  {len(G20_old)} rows, {G20_old['elapsed'].iloc[-1]/60:.2f} min (2026-08-03)")
print(f"  Gyroid 20W新:  {len(G20_new)} rows, {G20_new['elapsed'].iloc[-1]/60:.2f} min (2026-08-06, C组仅T7)")

# Process each dataset
# 10W: standard grouping
raw_b_10, worst_b_10, rem_b_10 = remove_worst_and_avg(G10, ['T2','T3','T4','T5'])
raw_c_10, worst_c_10, rem_c_10 = remove_worst_and_avg(G10, ['T6','T7','T8','T9'])

# 20W old: standard grouping
raw_b_20o, worst_b_20o, rem_b_20o = remove_worst_and_avg(G20_old, ['T2','T3','T4','T5'])
raw_c_20o, worst_c_20o, rem_c_20o = remove_worst_and_avg(G20_old, ['T6','T7','T8','T9'])

# 20W new: B组标准，C组仅T7
raw_b_20n, worst_b_20n, rem_b_20n = remove_worst_and_avg(G20_new, ['T2','T3','T4','T5'])
# C组仅T7
raw_c_20n = G20_new['T7'].values

print(f"\n离群剔除:")
print(f"  10W:    B组去掉 {worst_b_10}，C组去掉 {worst_c_10}")
print(f"  20W旧:  B组去掉 {worst_b_20o}，C组去掉 {worst_c_20o}")
print(f"  20W新:  B组去掉 {worst_b_20n}，C组仅T7（表面接触不良）")

# Peak temperatures
print(f"\n{'='*80}")
print("峰值温度对比")
print(f"{'='*80}")

g10_idx = G10['T1'].idxmax()
g20o_idx = G20_old['T1'].idxmax()
g20n_idx = G20_new['T1'].idxmax()

print(f"\n{'指标':<20s} {'10W':>12s} {'20W旧':>12s} {'20W新':>12s}")
print("-" * 60)
print(f"{'时长 (min)':<20s} {G10['elapsed'].iloc[-1]/60:>12.2f} {G20_old['elapsed'].iloc[-1]/60:>12.2f} {G20_new['elapsed'].iloc[-1]/60:>12.2f}")
print(f"{'A组 T1 (°C)':<20s} {G10['T1'].iloc[g10_idx]:>12.2f} {G20_old['T1'].iloc[g20o_idx]:>12.2f} {G20_new['T1'].iloc[g20n_idx]:>12.2f}")
print(f"{'B组 均值 (°C)':<20s} {raw_b_10[g10_idx]:>12.2f} {raw_b_20o[g20o_idx]:>12.2f} {raw_b_20n[g20n_idx]:>12.2f}")
print(f"{'C组 均值/T7 (°C)':<20s} {raw_c_10[g10_idx]:>12.2f} {raw_c_20o[g20o_idx]:>12.2f} {raw_c_20n[g20n_idx]:>12.2f}")

# Temperature gradients
print(f"\n{'='*80}")
print("温度梯度（T1峰值时刻）")
print(f"{'='*80}")

a10 = G10['T1'].iloc[g10_idx]
b10 = raw_b_10[g10_idx]
c10 = raw_c_10[g10_idx]

a20o = G20_old['T1'].iloc[g20o_idx]
b20o = raw_b_20o[g20o_idx]
c20o = raw_c_20o[g20o_idx]

a20n = G20_new['T1'].iloc[g20n_idx]
b20n = raw_b_20n[g20n_idx]
c20n = raw_c_20n[g20n_idx]

print(f"\n{'梯度':<15s} {'10W':>10s} {'20W旧':>10s} {'20W新':>10s}")
print("-" * 50)
print(f"{'A-B (°C)':<15s} {a10-b10:>10.2f} {a20o-b20o:>10.2f} {a20n-b20n:>10.2f}")
print(f"{'A-C (°C)':<15s} {a10-c10:>10.2f} {a20o-c20o:>10.2f} {a20n-c20n:>10.2f}")
print(f"{'B-C (°C)':<15s} {b10-c10:>10.2f} {b20o-c20o:>10.2f} {b20n-c20n:>10.2f}")

# Time to reach 42°C
print(f"\n{'='*80}")
print("达到42°C（PCM熔点）的时间")
print(f"{'='*80}")

def time_to_temp(df, vals, temp=42):
    above = df.loc[vals >= temp, 'elapsed']
    return above.iloc[0] if len(above) > 0 else float('inf')

print(f"\n{'信号':<15s} {'10W (s)':>12s} {'20W旧 (s)':>12s} {'20W新 (s)':>12s}")
print("-" * 55)

t1_10 = time_to_temp(G10, G10['T1'])
t1_20o = time_to_temp(G20_old, G20_old['T1'])
t1_20n = time_to_temp(G20_new, G20_new['T1'])
print(f"{'T1 (A)':<15s} {t1_10:>12.0f} {t1_20o:>12.0f} {t1_20n:>12.0f}")

b_10 = time_to_temp(G10, pd.Series(raw_b_10))
b_20o = time_to_temp(G20_old, pd.Series(raw_b_20o))
b_20n = time_to_temp(G20_new, pd.Series(raw_b_20n))
print(f"{'B组均值':<15s} {b_10:>12.0f} {b_20o:>12.0f} {b_20n:>12.0f}")

c_10 = time_to_temp(G10, pd.Series(raw_c_10))
c_20o = time_to_temp(G20_old, pd.Series(raw_c_20o))
c_20n = time_to_temp(G20_new, pd.Series(raw_c_20n))
print(f"{'C组/T7':<15s} {c_10:>12.0f} {c_20o:>12.0f} {c_20n:>12.0f}")

# Heating rate (first 3 min for 20W, first 5 min for 10W)
print(f"\n{'='*80}")
print("升温速率")
print(f"{'='*80}")

def heating_rate(df, vals, t_max=180):
    mask = (df['elapsed'] <= t_max).values
    if mask.sum() < 2:
        return 0
    v = vals if isinstance(vals, np.ndarray) else vals.values
    smoothed = apply_ema(v)
    return (smoothed[mask][-1] - smoothed[mask][0]) / (df.loc[mask, 'elapsed'].iloc[-1]/60)

print(f"\n{'信号':<15s} {'10W (5min)':>12s} {'20W旧 (3min)':>12s} {'20W新 (3min)':>12s}")
print("-" * 55)

r_t1_10 = heating_rate(G10, G10['T1'], 300)
r_t1_20o = heating_rate(G20_old, G20_old['T1'], 180)
r_t1_20n = heating_rate(G20_new, G20_new['T1'], 180)
print(f"{'T1 (A)':<15s} {r_t1_10:>12.3f} {r_t1_20o:>12.3f} {r_t1_20n:>12.3f}")

r_b_10 = heating_rate(G10, raw_b_10, 300)
r_b_20o = heating_rate(G20_old, raw_b_20o, 180)
r_b_20n = heating_rate(G20_new, raw_b_20n, 180)
print(f"{'B组均值':<15s} {r_b_10:>12.3f} {r_b_20o:>12.3f} {r_b_20n:>12.3f}")

r_c_10 = heating_rate(G10, raw_c_10, 300)
r_c_20o = heating_rate(G20_old, raw_c_20o, 180)
r_c_20n = heating_rate(G20_new, raw_c_20n, 180)
print(f"{'C组/T7':<15s} {r_c_10:>12.3f} {r_c_20o:>12.3f} {r_c_20n:>12.3f}")
print(f"{'单位':<15s} {'°C/min':>12s} {'°C/min':>12s} {'°C/min':>12s}")

# Key observations
print(f"\n{'='*80}")
print("关键观察")
print(f"{'='*80}")

print(f"""
1. 实验时长:
   - 10W: 25.38 min（最长，充分观察相变）
   - 20W旧: 8.50 min（较短）
   - 20W新: 12.35 min（比旧版长45%，数据更充分）

2. T1峰值温度:
   - 10W: {G10['T1'].iloc[g10_idx]:.1f}°C
   - 20W旧: {G20_old['T1'].iloc[g20o_idx]:.1f}°C
   - 20W新: {G20_new['T1'].iloc[g20n_idx]:.1f}°C
   → 20W功率翻倍，T1温度增加约 {(G20_new['T1'].iloc[g20n_idx]-G10['T1'].iloc[g10_idx])/G10['T1'].iloc[g10_idx]*100:.0f}%

3. 温度梯度（A-C）:
   - 10W: {a10-c10:.1f}°C
   - 20W旧: {a20o-c20o:.1f}°C
   - 20W新: {a20n-c20n:.1f}°C
   → 20W梯度显著增大，说明高功率下热扩散跟不上

4. B组升温速率:
   - 10W: {r_b_10:.2f}°C/min
   - 20W新: {r_b_20n:.2f}°C/min
   → 20W升温速率是10W的 {r_b_20n/r_b_10:.1f} 倍

5. C组（T7）升温速率:
   - 10W: {r_c_10:.2f}°C/min
   - 20W新: {r_c_20n:.2f}°C/min
   → 20W升温速率是10W的 {r_c_20n/r_c_10:.1f} 倍
""")

print(f"\n{'='*80}")
print("分析完成")
print(f"{'='*80}")
