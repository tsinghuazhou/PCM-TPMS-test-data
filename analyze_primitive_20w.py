"""
Gyroid 20W 新数据分析（2026-08-06）
C组（上表面）仅使用T7（其他传感器接触不良）
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

# Load new Gyroid 20W data
G20 = load('deprecated/tpms_primitive20w_20260806_162603.csv')

print("=" * 70)
print("GYROID 20W 新数据分析（2026-08-06）")
print("=" * 70)
print(f"\n记录数: {len(G20)}")
print(f"时长: {G20['elapsed'].iloc[-1]:.0f}s = {G20['elapsed'].iloc[-1]/60:.2f}min")

# B组：T2-T5 去离群
raw_b, worst_b, rem_b = remove_worst_and_avg(G20, ['T2','T3','T4','T5'])
smooth_b = apply_ema(raw_b)

# C组：仅T7
c_vals = G20['T7'].values
smooth_c = apply_ema(c_vals)

print(f"\nB组离群剔除: 去掉 {worst_b}，保留 {rem_b}")
print(f"C组: 仅使用 T7（上表面接触不良，其他传感器不可信）")

# 峰值
print(f"\n{'='*70}")
print("峰值温度")
print(f"{'='*70}")
g20_idx = G20['T1'].idxmax()
print(f"\nA组 (T1):         {G20['T1'].iloc[g20_idx]:.2f}°C")
print(f"B组 (3点均值):    {raw_b[g20_idx]:.2f}°C")
print(f"C组 (T7):         {G20['T7'].iloc[g20_idx]:.2f}°C")

# 温度梯度
print(f"\n{'='*70}")
print("温度梯度（T1峰值时刻）")
print(f"{'='*70}")
a_peak = G20['T1'].iloc[g20_idx]
b_peak = raw_b[g20_idx]
c_peak = G20['T7'].iloc[g20_idx]
print(f"\nA-B: {a_peak - b_peak:.2f}°C")
print(f"A-C: {a_peak - c_peak:.2f}°C")
print(f"B-C: {b_peak - c_peak:.2f}°C")

# 时间序列关键点
print(f"\n{'='*70}")
print("分组均值随时间变化")
print(f"{'='*70}")
for t_target in [120, 240, 360, 480, 600, 720]:
    if t_target > G20['elapsed'].iloc[-1]:
        break
    idx = G20['elapsed'].sub(t_target).abs().idxmin()
    a_t = G20['T1'].iloc[idx]
    b_t = raw_b[idx]
    c_t = G20['T7'].iloc[idx]
    print(f"\nt = {t_target}s ({t_target//60}min):")
    print(f"  A={a_t:.2f}°C, B={b_t:.2f}°C, C={c_t:.2f}°C")
    print(f"  A-B={a_t-b_t:.2f}°C, A-C={a_t-c_t:.2f}°C")

# 达到42°C时间
print(f"\n{'='*70}")
print("达到42°C（PCM熔点）的时间")
print(f"{'='*70}")
for name, vals in [('T1 (A)', G20['T1']), ('B组均值', pd.Series(raw_b)), ('T7 (C)', G20['T7'])]:
    above = G20.loc[vals >= 42, 'elapsed']
    if len(above) > 0:
        print(f"{name}: {above.iloc[0]:.0f}s ({above.iloc[0]/60:.2f}min)")
    else:
        print(f"{name}: 未达到42°C")

# 升温速率（前3分钟）
print(f"\n{'='*70}")
print("升温速率（前3分钟）")
print(f"{'='*70}")
t3 = 180
mask = G20['elapsed'] <= t3
if mask.sum() > 0:
    t1_rate = (G20.loc[mask, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[-1] - 
               G20.loc[mask, 'T1'].ewm(alpha=0.4,adjust=False).mean().iloc[0]) / (G20.loc[mask,'elapsed'].iloc[-1]/60)
    b_rate = (smooth_b[mask.values][:][-1] - smooth_b[mask.values][:][0]) / (G20.loc[mask,'elapsed'].iloc[-1]/60)
    c_rate = (smooth_c[mask.values][:][-1] - smooth_c[mask.values][:][0]) / (G20.loc[mask,'elapsed'].iloc[-1]/60)
    print(f"T1 (A): {t1_rate:.3f}°C/min")
    print(f"B组:    {b_rate:.3f}°C/min")
    print(f"T7 (C): {c_rate:.3f}°C/min")

print(f"\n{'='*70}")
print("分析完成")
print(f"{'='*70}")
