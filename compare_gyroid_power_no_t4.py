"""Gyroid 10W/20W/30W 功率梯度对比 (去掉T4, B组=T2/T3/T5)"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def b_avg_no_t4(df):
    """B组 = T2/T3/T5 直接平均（去掉T4）"""
    return df[['T2','T3','T5']].mean(axis=1)

# Load NEW data
g10 = load('temperature_record_20260808_165138gyroid10w.csv')
g20 = load('temperature_record_20260808_190451 (4).csv')
g30 = load('temperature_record_20260808_203206.csv')

b10 = b_avg_no_t4(g10)
b20 = b_avg_no_t4(g20)
b30 = b_avg_no_t4(g30)

# 计算梯度
def calc_gradient(df, b, t1_target):
    i = df.T1.sub(t1_target).abs().idxmin()
    ab = df.T1.iloc[i] - b.iloc[i]
    ac = df.T1.iloc[i] - df.T9.iloc[i]
    return ab, ac

# 对比表
print("=" * 80)
print("GYROID 功率梯度对比 (10W/20W/30W) - B组=T2/T3/T5 (去掉T4)")
print("=" * 80)

print("\n[1] A-B 梯度 (T1=42°C, 50°C, 55°C)")
print(f"{'T1(°C)':>8} | {'10W':>8} | {'20W':>8} | {'30W':>8}")
for t1 in [42, 50, 55]:
    ab10, _ = calc_gradient(g10, b10, t1)
    ab20, _ = calc_gradient(g20, b20, t1)
    ab30, _ = calc_gradient(g30, b30, t1)
    print(f"{t1:>8} | {ab10:>8.1f} | {ab20:>8.1f} | {ab30:>8.1f}")

print("\n[2] A-C 梯度 (C=T9, T1=42°C, 50°C, 55°C)")
print(f"{'T1(°C)':>8} | {'10W':>8} | {'20W':>8} | {'30W':>8}")
for t1 in [42, 50, 55]:
    _, ac10 = calc_gradient(g10, b10, t1)
    _, ac20 = calc_gradient(g20, b20, t1)
    _, ac30 = calc_gradient(g30, b30, t1)
    print(f"{t1:>8} | {ac10:>8.1f} | {ac20:>8.1f} | {ac30:>8.1f}")

print("\n[3] 熔融时长 (T1 in 42-52°C)")
for name, df in [('10W', g10), ('20W', g20), ('30W', g30)]:
    win = df.elapsed.loc[(df.T1 >= 42) & (df.T1 <= 52)]
    dur = (win.iloc[-1] - win.iloc[0]) / 60 if len(win) > 0 else 0
    print(f"  {name}: {dur:.1f} min")

print("\n[4] 到达42°C时间")
print(f"{'传感器':>8} | {'10W':>8} | {'20W':>8} | {'30W':>8}")
for c in ['T1', 'T9']:
    t10 = g10.loc[g10[c] >= 42, 'elapsed'].iloc[0] / 60 if len(g10.loc[g10[c] >= 42]) > 0 else np.nan
    t20 = g20.loc[g20[c] >= 42, 'elapsed'].iloc[0] / 60 if len(g20.loc[g20[c] >= 42]) > 0 else np.nan
    t30 = g30.loc[g30[c] >= 42, 'elapsed'].iloc[0] / 60 if len(g30.loc[g30[c] >= 42]) > 0 else np.nan
    print(f"{c:>8} | {t10:>8.1f} | {t20:>8.1f} | {t30:>8.1f}")

print("\n[5] C组接触检查 (T1=45°C时相对T9偏差)")
print(f"{'传感器':>8} | {'10W':>8} | {'20W':>8} | {'30W':>8}")
for c in ['T6', 'T7', 'T8']:
    i10 = g10.T1.sub(45).abs().idxmin()
    i20 = g20.T1.sub(45).abs().idxmin()
    i30 = g30.T1.sub(45).abs().idxmin()
    off10 = g10[c].iloc[i10] - g10.T9.iloc[i10]
    off20 = g20[c].iloc[i20] - g20.T9.iloc[i20]
    off30 = g30[c].iloc[i30] - g30.T9.iloc[i30]
    print(f"{c:>8} | {off10:>+7.1f} | {off20:>+7.1f} | {off30:>+7.1f}")

print("\n[6] B组一致性 (T1=45°C时T2/T3/T5 spread)")
for name, df in [('10W', g10), ('20W', g20), ('30W', g30)]:
    i = df.T1.sub(45).abs().idxmin()
    vals = df.loc[i, ['T2','T3','T5']]
    spread = vals.max() - vals.min()
    print(f"  {name}: spread={spread:.1f}°C (T2={vals['T2']:.1f}, T3={vals['T3']:.1f}, T5={vals['T5']:.1f})")

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# (1) A-B vs T1
ax = axes[0, 0]
for name, df, b, color in [('10W', g10, b10, 'blue'), ('20W', g20, b20, 'orange'), ('30W', g30, b30, 'red')]:
    t1_range = df.T1[(df.T1 >= 38) & (df.T1 <= 60)]
    ab = t1_range - b.loc[t1_range.index]
    ax.plot(t1_range, ab, label=name, color=color, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change window')
ax.set_xlabel('T1 (°C)', fontsize=12)
ax.set_ylabel('A-B gradient (°C)', fontsize=12)
ax.set_title('A-B gradient vs T1', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

# (2) A-C vs T1
ax = axes[0, 1]
for name, df, b, color in [('10W', g10, b10, 'blue'), ('20W', g20, b20, 'orange'), ('30W', g30, b30, 'red')]:
    t1_range = df.T1[(df.T1 >= 38) & (df.T1 <= 60)]
    ac = t1_range - df.T9.loc[t1_range.index]
    ax.plot(t1_range, ac, label=name, color=color, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change window')
ax.set_xlabel('T1 (°C)', fontsize=12)
ax.set_ylabel('A-C gradient (°C)', fontsize=12)
ax.set_title('A-C gradient vs T1 (C=T9)', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

# (3) 温度-时间曲线 (T1, B均值, T9)
ax = axes[1, 0]
for name, df, b, color in [('10W', g10, b10, 'blue'), ('20W', g20, b20, 'orange'), ('30W', g30, b30, 'red')]:
    ax.plot(df.elapsed/60, df.T1, '--', color=color, label=f'{name} T1', linewidth=1.5)
    ax.plot(df.elapsed/60, b, '-', color=color, label=f'{name} B', linewidth=2)
    ax.plot(df.elapsed/60, df.T9, ':', color=color, label=f'{name} T9', linewidth=1.5)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5, label='Melting point 42°C')
ax.set_xlabel('Time (min)', fontsize=12)
ax.set_ylabel('Temperature (°C)', fontsize=12)
ax.set_title('Temperature-time curves', fontsize=14)
ax.legend(fontsize=8, ncol=3)
ax.grid(True, alpha=0.3)

# (4) 梯度-功率关系 (T1=50°C)
ax = axes[1, 1]
powers = [10, 20, 30]
ab50 = []
ac50 = []
for df, b in [(g10, b10), (g20, b20), (g30, b30)]:
    ab, ac = calc_gradient(df, b, 50)
    ab50.append(ab)
    ac50.append(ac)
ax.plot(powers, ab50, 'o-', label='A-B', color='blue', linewidth=2, markersize=8)
ax.plot(powers, ac50, 's-', label='A-C', color='red', linewidth=2, markersize=8)
ax.set_xlabel('Heating power (W)', fontsize=12)
ax.set_ylabel('Gradient (°C)', fontsize=12)
ax.set_title('Gradient vs Power at T1=50°C', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_power_comparison_no_t4.png', dpi=300)
plt.savefig('output/paper/figures/gyroid_power_comparison_no_t4.pdf')
print("\n[图已保存] output/paper/figures/gyroid_power_comparison_no_t4.png/pdf")
