"""
Primitive 10W vs 20W 综合对比

Primitive 10W: tpms_primitive10w_20260805_200423.csv (1341 rows, 26.93 min)
Primitive 20W: tpms_primitive20w_20260806_214551.csv (702 rows, 11.93 min, C组T7/T8/T9)
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

P10 = load('tpms_primitive10w_20260805_200423.csv')
P20 = load('tpms_primitive20w_20260806_214551.csv')

print("=" * 70)
print("PRIMITIVE 10W vs 20W 综合对比")
print("=" * 70)
print(f"\n数据概览:")
print(f"  Primitive 10W: {len(P10)} rows, {P10['elapsed'].iloc[-1]/60:.2f} min")
print(f"  Primitive 20W: {len(P20)} rows, {P20['elapsed'].iloc[-1]/60:.2f} min")

# 10W: B组去离群, C组去离群
raw_b_10, worst_b_10, rem_b_10 = remove_worst_and_avg(P10, ['T2','T3','T4','T5'])
raw_c_10, worst_c_10, rem_c_10 = remove_worst_and_avg(P10, ['T6','T7','T8','T9'])

# 20W: B组去离群, C组去离群 (T6异常，保留T7/T8/T9)
raw_b_20, worst_b_20, rem_b_20 = remove_worst_and_avg(P20, ['T2','T3','T4','T5'])
raw_c_20, worst_c_20, rem_c_20 = remove_worst_and_avg(P20, ['T6','T7','T8','T9'])

print(f"\n离群剔除:")
print(f"  10W: B组去掉 {worst_b_10} (保留{rem_b_10}), C组去掉 {worst_c_10} (保留{rem_c_10})")
print(f"  20W: B组去掉 {worst_b_20} (保留{rem_b_20}), C组去掉 {worst_c_20} (保留{rem_c_20})")

# 峰值
p10_idx = P10['T1'].idxmax()
p20_idx = P20['T1'].idxmax()

a10 = P10['T1'].iloc[p10_idx]
b10 = raw_b_10[p10_idx]
c10 = raw_c_10[p10_idx]

a20 = P20['T1'].iloc[p20_idx]
b20 = raw_b_20[p20_idx]
c20 = raw_c_20[p20_idx]

print(f"\n{'='*70}")
print("峰值温度")
print(f"{'='*70}")
print(f"\n{'组别':<20s} {'10W':>10s} {'20W':>10s} {'Δ':>10s} {'20W/10W':>10s}")
print("-" * 65)
print(f"{'A (T1)':<20s} {a10:>10.2f} {a20:>10.2f} {a20-a10:>+10.2f} {a20/a10:>10.2f}x")
print(f"{'B (mid, 3avg)':<20s} {b10:>10.2f} {b20:>10.2f} {b20-b10:>+10.2f} {b20/b10:>10.2f}x")
print(f"{'C (top)':<20s} {c10:>10.2f} {c20:>10.2f} {c20-c10:>+10.2f} {c20/c10:>10.2f}x")

# 温度梯度
print(f"\n{'='*70}")
print("温度梯度（T1峰值时刻）")
print(f"{'='*70}")
print(f"\n{'梯度':<12s} {'10W':>10s} {'20W':>10s} {'Δ':>10s} {'20W/10W':>10s}")
print("-" * 55)
for label, g10, g20 in [
    ('A-B', a10-b10, a20-b20),
    ('A-C', a10-c10, a20-c20),
    ('B-C', b10-c10, b20-c20)]:
    ratio = g20/g10 if g10 != 0 else float('inf')
    print(f"{label:<12s} {g10:>10.2f} {g20:>10.2f} {g20-g10:>+10.2f} {ratio:>9.2f}x")

# 达到42°C时间
print(f"\n{'='*70}")
print("达到42°C的时间")
print(f"{'='*70}")
def time_to_temp(df, vals, temp=42):
    above = df.loc[vals >= temp, 'elapsed']
    return above.iloc[0] if len(above) > 0 else float('inf')

t1_10 = time_to_temp(P10, P10['T1'])
t1_20 = time_to_temp(P20, P20['T1'])
b_10 = time_to_temp(P10, pd.Series(raw_b_10))
b_20 = time_to_temp(P20, pd.Series(raw_b_20))
c_10 = time_to_temp(P10, pd.Series(raw_c_10))
c_20 = time_to_temp(P20, pd.Series(raw_c_20))

print(f"\n{'信号':<15s} {'10W (s)':>10s} {'20W (s)':>10s} {'加速比':>10s}")
print("-" * 48)
print(f"{'T1 (A)':<15s} {t1_10:>10.0f} {t1_20:>10.0f} {t1_10/t1_20:>9.1f}x")
print(f"{'B组均值':<15s} {b_10:>10.0f} {b_20:>10.0f} {b_10/b_20:>9.1f}x")
print(f"{'C组均值':<15s} {c_10:>10.0f} {c_20:>10.0f} {c_10/c_20:>9.1f}x")

# 升温速率
print(f"\n{'='*70}")
print("升温速率（前3分钟）")
print(f"{'='*70}")
t3 = 180
m10 = (P10['elapsed']<=t3).values
m20 = (P20['elapsed']<=t3).values

def rate(vals, mask, df):
    s = apply_ema(vals if isinstance(vals, np.ndarray) else vals.values)
    return (s[mask][-1] - s[mask][0]) / (df.loc[mask,'elapsed'].iloc[-1]/60)

r_t1_10 = rate(P10['T1'].values, m10, P10)
r_t1_20 = rate(P20['T1'].values, m20, P20)
r_b_10 = rate(raw_b_10, m10, P10)
r_b_20 = rate(raw_b_20, m20, P20)
r_c_10 = rate(raw_c_10, m10, P10)
r_c_20 = rate(raw_c_20, m20, P20)

print(f"\n{'信号':<15s} {'10W':>10s} {'20W':>10s} {'20W/10W':>10s}")
print("-" * 48)
print(f"{'T1 (A)':<15s} {r_t1_10:>10.3f} {r_t1_20:>10.3f} {r_t1_20/r_t1_10:>9.2f}x")
print(f"{'B组均值':<15s} {r_b_10:>10.3f} {r_b_20:>10.3f} {r_b_20/r_b_10:>9.2f}x")
print(f"{'C组均值':<15s} {r_c_10:>10.3f} {r_c_20:>10.3f} {r_c_20/r_c_10:>9.2f}x")
print(f"{'单位':<15s} {'°C/min':>10s} {'°C/min':>10s}")

# 时间序列对比
print(f"\n{'='*70}")
print("分组均值随时间变化")
print(f"{'='*70}")
for t_target in [120, 240, 360, 480, 600, 720]:
    i10 = P10['elapsed'].sub(t_target).abs().idxmin()
    i20 = P20['elapsed'].sub(t_target).abs().idxmin()
    a10_t = P10['T1'].iloc[i10]
    b10_t = raw_b_10[i10]
    c10_t = raw_c_10[i10]
    a20_t = P20['T1'].iloc[i20]
    b20_t = raw_b_20[i20]
    c20_t = raw_c_20[i20]
    print(f"\n--- t = {t_target}s ({t_target//60}min) ---")
    print(f"  10W: A={a10_t:.1f}°C, B={b10_t:.1f}°C, C={c10_t:.1f}°C | A-B={a10_t-b10_t:.1f}, A-C={a10_t-c10_t:.1f}")
    print(f"  20W: A={a20_t:.1f}°C, B={b20_t:.1f}°C, C={c20_t:.1f}°C | A-B={a20_t-b20_t:.1f}, A-C={a20_t-c20_t:.1f}")

# C组离群值对比
print(f"\n{'='*70}")
print("C组离群值对比")
print(f"{'='*70}")
print(f"\n  10W: C组剔除 {worst_c_10}（峰值 {P10[worst_c_10].max():.1f}°C），保留 {rem_c_10}")
print(f"  20W: C组剔除 {worst_c_20}（峰值 {P20[worst_c_20].max():.1f}°C），保留 {rem_c_20}")
print(f"\n  ★ T6 在 20W 下持续异常，可能是该位置传感器固有接触问题")

# 能量分析
print(f"\n{'='*70}")
print("能量吸收")
print(f"{'='*70}")
t1r10 = P10['T1'].max() - P10['T1'].iloc[0]
t1r20 = P20['T1'].max() - P20['T1'].iloc[0]
print(f"\n  T1温升: 10W={t1r10:.1f}°C, 20W={t1r20:.1f}°C (20W高{(t1r20-t1r10)/t1r10*100:.0f}%)")
print(f"  时长:   10W={P10['elapsed'].iloc[-1]/60:.1f}min, 20W={P20['elapsed'].iloc[-1]/60:.1f}min (20W短{(1-P20['elapsed'].iloc[-1]/P10['elapsed'].iloc[-1])*100:.0f}%)")
print(f"  输入能量比: 20W/10W = {(20*P20['elapsed'].iloc[-1])/(10*P10['elapsed'].iloc[-1]):.2f}x")

print(f"\n{'='*70}")
print("分析完成")
print(f"{'='*70}")
