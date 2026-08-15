"""Gyroid 30W 新数据完整分析 (2026-08-08)
数据: temperature_record_20260808_203206.csv
统计规则: B组=T2/T3/T5 (去掉T4), C组=T9
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('temperature_record_20260808_203206.csv', encoding='utf-8-sig')
df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
df['time'] = pd.to_datetime(df['time'])
df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
df['elapsed_min'] = df['elapsed'] / 60

# 计算B组均值 (T2/T3/T5, 去掉T4)
df['B_avg'] = df[['T2', 'T3', 'T5']].mean(axis=1)

# 计算梯度
df['A-B'] = df['T1'] - df['B_avg']
df['A-C'] = df['T1'] - df['T9']

print("=" * 80)
print("Gyroid 30W 新数据分析 (2026-08-08)")
print("=" * 80)

# 基本信息
print(f"\n[基本信息]")
print(f"行数: {len(df)}")
print(f"时长: {df.elapsed_min.iloc[-1]:.2f} min")
print(f"T1峰值: {df.T1.max():.1f}°C (行 {df.T1.idxmax()})")
print(f"T1末值: {df.T1.iloc[-1]:.1f}°C")
print(f"T9末值: {df.T9.iloc[-1]:.1f}°C")

# 到达42°C时间
print(f"\n[到达42°C时间]")
for c in ['T1', 'T2', 'T3', 'T5', 'T9']:
    idx = df.loc[df[c] >= 42, 'elapsed_min']
    t = idx.iloc[0] if len(idx) > 0 else np.nan
    print(f"  {c}: {t:.2f} min")

# 熔融时长
melting_mask = (df['T1'] >= 42) & (df['T1'] <= 52)
if melting_mask.sum() > 1:
    melting_duration = df.loc[melting_mask, 'elapsed_min'].iloc[-1] - df.loc[melting_mask, 'elapsed_min'].iloc[0]
    print(f"\n[熔融时长 (T1在42-52°C)]")
    print(f"  {melting_duration:.2f} min")

# 梯度关键值
print(f"\n[梯度关键值]")
for t1_target in [42, 45, 50, 55]:
    idx = df.T1.sub(t1_target).abs().idxmin()
    ab = df['A-B'].iloc[idx]
    ac = df['A-C'].iloc[idx]
    print(f"  T1={t1_target}°C: A-B={ab:.1f}°C, A-C={ac:.1f}°C")

# 绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(16, 12))

# 图1: 所有传感器温度-时间曲线
ax1 = plt.subplot(2, 3, 1)
for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']:
    ax1.plot(df.elapsed_min, df[c], label=c, linewidth=1.5, alpha=0.8)
ax1.axhline(y=42, color='red', linestyle='--', linewidth=1, alpha=0.5, label='熔点 42°C')
ax1.set_xlabel('时间 (min)')
ax1.set_ylabel('温度 (°C)')
ax1.set_title('所有传感器温度曲线')
ax1.legend(fontsize=8, ncol=3)
ax1.grid(True, alpha=0.3)

# 图2: T1, B组均值, T9 对比
ax2 = plt.subplot(2, 3, 2)
ax2.plot(df.elapsed_min, df.T1, 'r-', label='T1 (底面)', linewidth=2.5)
ax2.plot(df.elapsed_min, df.B_avg, 'g-', label='B组均值 (T2/T3/T5)', linewidth=2.5)
ax2.plot(df.elapsed_min, df.T9, 'b-', label='T9 (顶层)', linewidth=2.5)
ax2.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='熔点 42°C')
ax2.set_xlabel('时间 (min)')
ax2.set_ylabel('温度 (°C)')
ax2.set_title('关键位置温度对比')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 图3: A-B 和 A-C 梯度随时间变化
ax3 = plt.subplot(2, 3, 3)
ax3.plot(df.elapsed_min, df['A-B'], 'g-', label='A-B 梯度', linewidth=2)
ax3.plot(df.elapsed_min, df['A-C'], 'b-', label='A-C 梯度', linewidth=2)
ax3.set_xlabel('时间 (min)')
ax3.set_ylabel('梯度 (°C)')
ax3.set_title('温度梯度随时间变化')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 图4: A-B 梯度 vs T1
ax4 = plt.subplot(2, 3, 4)
mask_38_60 = (df.T1 >= 38) & (df.T1 <= 60)
ax4.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-B'], 'g-', linewidth=2)
ax4.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax4.axvline(x=42, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax4.set_xlabel('T1 (°C)')
ax4.set_ylabel('A-B 梯度 (°C)')
ax4.set_title('A-B 梯度 vs T1')
ax4.legend()
ax4.grid(True, alpha=0.3)

# 图5: A-C 梯度 vs T1
ax5 = plt.subplot(2, 3, 5)
ax5.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-C'], 'b-', linewidth=2)
ax5.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax5.axvline(x=42, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax5.set_xlabel('T1 (°C)')
ax5.set_ylabel('A-C 梯度 (°C)')
ax5.set_title('A-C 梯度 vs T1 (C=T9)')
ax5.legend()
ax5.grid(True, alpha=0.3)

# 图6: 升温速率 dT/dt
ax6 = plt.subplot(2, 3, 6)
dt = df.elapsed.diff()
dT1 = df.T1.diff()
dT9 = df.T9.diff()
rate_T1 = (dT1 / dt * 60).fillna(0)  # °C/min
rate_T9 = (dT9 / dt * 60).fillna(0)
ax6.plot(df.elapsed_min, rate_T1, 'r-', label='T1 升温速率', linewidth=1.5, alpha=0.7)
ax6.plot(df.elapsed_min, rate_T9, 'b-', label='T9 升温速率', linewidth=1.5, alpha=0.7)
ax6.set_xlabel('时间 (min)')
ax6.set_ylabel('升温速率 (°C/min)')
ax6.set_title('升温速率')
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_30w_new_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_30w_new_analysis.pdf', bbox_inches='tight')
print(f"\n[图表已保存] output/paper/figures/gyroid_30w_new_analysis.png/pdf")
