"""IWP 20W 数据分析
B组 = T2/T3（剔除T5）
C组 = T8/T9（仅保留T8、T9）
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('temperature_record_20260809_201218iwp20w.csv', encoding='utf-8')
df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']

# 清理NaN行
df = df.dropna(subset=['T1']).reset_index(drop=True)

# 时间列只有分钟精度，用行号作为秒数（1Hz采样）
df['elapsed'] = df.index.astype(float)  # 秒
df['elapsed_min'] = df['elapsed'] / 60.0

# B组 = T2/T3（剔除T5）
df['B_avg'] = df[['T2','T3']].mean(axis=1)
# C组 = T8/T9
df['C_avg'] = df[['T8','T9']].mean(axis=1)

df['A-B'] = df['T1'] - df['B_avg']
df['A-C'] = df['T1'] - df['C_avg']

print("=" * 80)
print("IWP 20W 数据分析 (B=T2/T3, C=T8/T9)")
print("=" * 80)

# 基本信息
print(f"\n[基本信息]")
print(f"行数: {len(df)}")
print(f"时长: {df.elapsed_min.iloc[-1]:.2f} min")
print(f"T1末值: {df.T1.iloc[-1]:.1f}°C")
print(f"T8末值: {df.T8.iloc[-1]:.1f}°C")
print(f"T9末值: {df.T9.iloc[-1]:.1f}°C")

# 到达42°C时间
print(f"\n[到达42°C时间]")
for c in ['T1', 'T2', 'T3', 'T8', 'T9']:
    idx = df.loc[df[c] >= 42, 'elapsed_min']
    t = idx.iloc[0] if len(idx) > 0 else np.nan
    print(f"  {c}: {t:.2f} min")

# B组均值到达42°C
b42 = df.loc[df['B_avg'] >= 42, 'elapsed_min']
print(f"  B_avg(T2/T3): {b42.iloc[0]:.2f} min" if len(b42) > 0 else "  B_avg: N/A")

# 熔融时长
mask = (df['T1'] >= 42) & (df['T1'] <= 52)
if mask.sum() > 1:
    dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
    print(f"\n[熔融时长 (T1在42-52°C)]")
    print(f"  {dur:.2f} min")

# 梯度关键值
print(f"\n[梯度关键值]")
print(f"{'T1(°C)':>8} | {'A-B':>8} | {'A-C':>8}")
for t1 in [42, 45, 50, 55]:
    idx = df.T1.sub(t1).abs().idxmin()
    ab = df['A-B'].iloc[idx]
    ac = df['A-C'].iloc[idx]
    print(f"{t1:>8} | {ab:>8.1f} | {ac:>8.1f}")

# B组一致性
print(f"\n[B组一致性 T2/T3 (T1=45°C)]")
idx45 = df.T1.sub(45).abs().idxmin()
spread = abs(df.loc[idx45, 'T2'] - df.loc[idx45, 'T3'])
print(f"  T2={df.loc[idx45,'T2']:.1f}°C, T3={df.loc[idx45,'T3']:.1f}°C, spread={spread:.1f}°C")

# C组一致性
print(f"\n[C组一致性 T8/T9 (T1=45°C)]")
spread_c = abs(df.loc[idx45, 'T8'] - df.loc[idx45, 'T9'])
print(f"  T8={df.loc[idx45,'T8']:.1f}°C, T9={df.loc[idx45,'T9']:.1f}°C, spread={spread_c:.1f}°C")

# 梯度稳定性
print(f"\n[梯度稳定性 (42°C→55°C)]")
ab42 = df.loc[df.T1.sub(42).abs().idxmin(), 'A-B']
ab55 = df.loc[df.T1.sub(55).abs().idxmin(), 'A-B']
print(f"  A-B: {ab42:.1f} → {ab55:.1f}°C ({(ab55-ab42)/ab42*100:+.1f}%)")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: 所有传感器温度曲线
ax = axes[0, 0]
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    ax.plot(df.elapsed_min, df[c], label=c, linewidth=1.5, alpha=0.8)
ax.axhline(y=42, color='red', linestyle='--', alpha=0.5, label='Melting 42°C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (°C)')
ax.set_title('IWP 20W All Sensors'); ax.legend(fontsize=7, ncol=3); ax.grid(alpha=0.3)

# 图2: T1, B, C
ax = axes[0, 1]
ax.plot(df.elapsed_min, df.T1, 'r-', label='T1', linewidth=2.5)
ax.plot(df.elapsed_min, df.B_avg, 'g-', label='B (T2/T3)', linewidth=2.5)
ax.plot(df.elapsed_min, df.C_avg, 'b-', label='C (T8/T9)', linewidth=2.5)
ax.axhline(y=42, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (°C)')
ax.set_title('IWP 20W Key Positions'); ax.legend(); ax.grid(alpha=0.3)

# 图3: 梯度 vs 时间
ax = axes[0, 2]
ax.plot(df.elapsed_min, df['A-B'], 'g-', label='A-B', linewidth=2)
ax.plot(df.elapsed_min, df['A-C'], 'b-', label='A-C', linewidth=2)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (°C)')
ax.set_title('IWP 20W Gradients vs Time'); ax.legend(); ax.grid(alpha=0.3)

# 图4: A-B vs T1
ax = axes[1, 0]
mask_38_60 = (df.T1 >= 38) & (df.T1 <= 60)
ax.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-B'], 'g-', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('IWP 20W A-B Gradient vs T1'); ax.legend(); ax.grid(alpha=0.3)

# 图5: A-C vs T1
ax = axes[1, 1]
ax.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-C'], 'b-', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C Gradient (°C)')
ax.set_title('IWP 20W A-C Gradient vs T1'); ax.legend(); ax.grid(alpha=0.3)

# 图6: 升温速率
ax = axes[1, 2]
dt = df.elapsed.diff()
dT1 = df.T1.diff()
dT9 = df.T9.diff()
rate_T1 = (dT1 / dt * 60).fillna(0)
rate_T9 = (dT9 / dt * 60).fillna(0)
ax.plot(df.elapsed_min, rate_T1, 'r-', label='T1 rate', linewidth=1.5, alpha=0.7)
ax.plot(df.elapsed_min, rate_T9, 'b-', label='T9 rate', linewidth=1.5, alpha=0.7)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Rate (°C/min)')
ax.set_title('IWP 20W Heating Rate'); ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/iwp_20w_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/iwp_20w_analysis.pdf', bbox_inches='tight')
print(f"\n[图表已保存] output/paper/figures/iwp_20w_analysis.png/pdf")
