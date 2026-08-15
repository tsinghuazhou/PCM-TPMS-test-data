"""IWP结构10W加热数据分析"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
df['time'] = pd.to_datetime(df['time'])
df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
df['elapsed_min'] = df['elapsed'] / 60

# B组 = T2/T3/T5 (去掉T4，与Gyroid/Primitive一致)
df['B_avg'] = df[['T2','T3','T5']].mean(axis=1)
df['A-B'] = df['T1'] - df['B_avg']
df['A-C'] = df['T1'] - df['T9']

print("=" * 80)
print("IWP 10W 加热数据分析")
print("=" * 80)

# 基本信息
print(f"\n[基本信息]")
print(f"行数: {len(df)}")
print(f"时长: {df.elapsed_min.iloc[-1]:.2f} min")
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

# B组一致性检查
print(f"\n[B组一致性 (T1=45°C)]")
idx45 = df.T1.sub(45).abs().idxmin()
spread = df.loc[idx45, ['T2','T3','T5']].max() - df.loc[idx45, ['T2','T3','T5']].min()
print(f"  T2/T3/T5 spread: {spread:.1f}°C")
print(f"  T2={df.loc[idx45, 'T2']:.1f}°C, T3={df.loc[idx45, 'T3']:.1f}°C, T5={df.loc[idx45, 'T5']:.1f}°C")

# C组接触检查
print(f"\n[C组接触 (T1=45°C时相对T9偏差)]")
t9_ref = df.loc[idx45, 'T9']
for c in ['T6', 'T7', 'T8']:
    off = df.loc[idx45, c] - t9_ref
    print(f"  {c}: {df.loc[idx45, c]:.1f}°C (偏差{off:+.1f}°C)")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: 所有传感器温度曲线
ax = axes[0, 0]
for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']:
    ax.plot(df.elapsed_min, df[c], label=c, linewidth=1.5, alpha=0.8)
ax.axhline(y=42, color='red', linestyle='--', alpha=0.5, label='熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('IWP 10W 所有传感器温度曲线')
ax.legend(fontsize=8, ncol=3)
ax.grid(True, alpha=0.3)

# 图2: T1, B组均值, T9 对比
ax = axes[0, 1]
ax.plot(df.elapsed_min, df.T1, 'r-', label='T1 (底面)', linewidth=2.5)
ax.plot(df.elapsed_min, df.B_avg, 'g-', label='B组均值 (T2/T3/T5)', linewidth=2.5)
ax.plot(df.elapsed_min, df.T9, 'b-', label='T9 (顶层)', linewidth=2.5)
ax.axhline(y=42, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('IWP 10W 关键位置温度对比')
ax.legend()
ax.grid(True, alpha=0.3)

# 图3: A-B 和 A-C 梯度随时间变化
ax = axes[0, 2]
ax.plot(df.elapsed_min, df['A-B'], 'g-', label='A-B 梯度', linewidth=2)
ax.plot(df.elapsed_min, df['A-C'], 'b-', label='A-C 梯度', linewidth=2)
ax.set_xlabel('时间 (min)')
ax.set_ylabel('梯度 (°C)')
ax.set_title('IWP 10W 温度梯度随时间变化')
ax.legend()
ax.grid(True, alpha=0.3)

# 图4: A-B 梯度 vs T1
ax = axes[1, 0]
mask_38_60 = (df.T1 >= 38) & (df.T1 <= 60)
ax.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-B'], 'g-', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.axvline(x=42, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-B 梯度 (°C)')
ax.set_title('IWP 10W A-B 梯度 vs T1')
ax.legend()
ax.grid(True, alpha=0.3)

# 图5: A-C 梯度 vs T1
ax = axes[1, 1]
ax.plot(df.loc[mask_38_60, 'T1'], df.loc[mask_38_60, 'A-C'], 'b-', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.axvline(x=42, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-C 梯度 (°C)')
ax.set_title('IWP 10W A-C 梯度 vs T1 (C=T9)')
ax.legend()
ax.grid(True, alpha=0.3)

# 图6: 升温速率 dT/dt
ax = axes[1, 2]
dt = df.elapsed.diff()
dT1 = df.T1.diff()
dT9 = df.T9.diff()
rate_T1 = (dT1 / dt * 60).fillna(0)  # °C/min
rate_T9 = (dT9 / dt * 60).fillna(0)
ax.plot(df.elapsed_min, rate_T1, 'r-', label='T1 升温速率', linewidth=1.5, alpha=0.7)
ax.plot(df.elapsed_min, rate_T9, 'b-', label='T9 升温速率', linewidth=1.5, alpha=0.7)
ax.set_xlabel('时间 (min)')
ax.set_ylabel('升温速率 (°C/min)')
ax.set_title('IWP 10W 升温速率')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/iwp_10w_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/iwp_10w_analysis.pdf', bbox_inches='tight')
print(f"\n[图表已保存] output/paper/figures/iwp_10w_analysis.png/pdf")
