"""新旧Gyroid 30W对比（只统计加热阶段，T1峰值之前）"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
new_df = pd.read_csv('tpms_gyroid30w_20260808_203206.csv', encoding='utf-8-sig')
old_df = pd.read_csv('tpms_gyroid30w_20260803_171111.csv', encoding='utf-8-sig')

new_df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
old_df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']

new_df['time'] = pd.to_datetime(new_df['time'])
old_df['time'] = pd.to_datetime(old_df['time'])

new_df['elapsed_min'] = (new_df['time'] - new_df['time'].iloc[0]).dt.total_seconds() / 60
old_df['elapsed_min'] = (old_df['time'] - old_df['time'].iloc[0]).dt.total_seconds() / 60

# 找T1峰值位置，只取峰值之前的数据（加热阶段）
new_peak_idx = new_df['T1'].idxmax()
old_peak_idx = old_df['T1'].idxmax()

# 只取加热阶段数据
new_heat = new_df.iloc[:new_peak_idx+1].copy()
old_heat = old_df.iloc[:old_peak_idx+1].copy()

# 计算B组（去掉T4）和C组（只取T9）
new_heat['B_avg'] = new_heat[['T2','T3','T5']].mean(axis=1)
old_heat['B_avg'] = old_heat[['T2','T3','T5']].mean(axis=1)

new_heat['A-B'] = new_heat['T1'] - new_heat['B_avg']
old_heat['A-B'] = old_heat['T1'] - old_heat['B_avg']

new_heat['A-C'] = new_heat['T1'] - new_heat['T9']
old_heat['A-C'] = old_heat['T1'] - old_heat['T9']

print("=" * 80)
print("新旧Gyroid 30W对比（仅加热阶段，T1峰值之前）")
print("=" * 80)

print("\n【基本信息】")
print(f"新数据: {len(new_heat)} 行, T1峰值 {new_heat['T1'].iloc[-1]:.1f}°C, 时长 {new_heat['elapsed_min'].iloc[-1]:.2f} min")
print(f"旧数据: {len(old_heat)} 行, T1峰值 {old_heat['T1'].iloc[-1]:.1f}°C, 时长 {old_heat['elapsed_min'].iloc[-1]:.2f} min")

print("\n【到达42°C时间】")
for name, df in [('新', new_heat), ('旧', old_heat)]:
    t1_42 = df[df['T1'] >= 42]['elapsed_min'].iloc[0] if len(df[df['T1'] >= 42]) > 0 else np.nan
    t9_42 = df[df['T9'] >= 42]['elapsed_min'].iloc[0] if len(df[df['T9'] >= 42]) > 0 else np.nan
    print(f"  {name}数据: T1={t1_42:.2f} min, T9={t9_42:.2f} min")

print("\n【熔融时长 (T1在42-52°C)】")
for name, df in [('新', new_heat), ('旧', old_heat)]:
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
        print(f"  {name}数据: {dur:.2f} min")
    else:
        print(f"  {name}数据: 无有效熔融窗口")

print("\n【梯度对比 (T1=42°C, 50°C)】")
for t1_target in [42, 50]:
    print(f"\n  T1={t1_target}°C:")
    for name, df in [('新', new_heat), ('旧', old_heat)]:
        idx = (df['T1'] - t1_target).abs().idxmin()
        ab = df.loc[idx, 'A-B']
        ac = df.loc[idx, 'A-C']
        print(f"    {name}数据: A-B={ab:.1f}°C, A-C={ac:.1f}°C")

print("\n【B组一致性 (T1=45°C时 T2/T3/T5 spread)】")
for name, df in [('新', new_heat), ('旧', old_heat)]:
    idx = (df['T1'] - 45).abs().idxmin()
    spread = df.loc[idx, ['T2','T3','T5']].max() - df.loc[idx, ['T2','T3','T5']].min()
    print(f"  {name}数据: {spread:.1f}°C")

print("\n【C组接触 (T1=45°C时相对T9偏差)】")
for name, df in [('新', new_heat), ('旧', old_heat)]:
    idx = (df['T1'] - 45).abs().idxmin()
    t9_ref = df.loc[idx, 'T9']
    t6_off = df.loc[idx, 'T6'] - t9_ref
    t7_off = df.loc[idx, 'T7'] - t9_ref
    t8_off = df.loc[idx, 'T8'] - t9_ref
    print(f"  {name}数据: T6={t6_off:+.1f}°C, T7={t7_off:+.1f}°C, T8={t8_off:+.1f}°C")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: T1温度曲线
ax = axes[0, 0]
ax.plot(new_heat['elapsed_min'], new_heat['T1'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat['elapsed_min'], old_heat['T1'], 'r-', label='旧数据', linewidth=2)
ax.axhline(y=42, color='g', linestyle='--', alpha=0.5, label='熔点42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('T1温度曲线（加热阶段）')
ax.legend()
ax.grid(True, alpha=0.3)

# 图2: T9温度曲线
ax = axes[0, 1]
ax.plot(new_heat['elapsed_min'], new_heat['T9'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat['elapsed_min'], old_heat['T9'], 'r-', label='旧数据', linewidth=2)
ax.axhline(y=42, color='g', linestyle='--', alpha=0.5, label='熔点42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('温度 (°C)')
ax.set_title('T9温度曲线（加热阶段）')
ax.legend()
ax.grid(True, alpha=0.3)

# 图3: A-B梯度对比
ax = axes[0, 2]
ax.plot(new_heat['elapsed_min'], new_heat['A-B'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat['elapsed_min'], old_heat['A-B'], 'r-', label='旧数据', linewidth=2)
ax.set_xlabel('时间 (min)')
ax.set_ylabel('A-B梯度 (°C)')
ax.set_title('A-B梯度随时间变化')
ax.legend()
ax.grid(True, alpha=0.3)

# 图4: A-C梯度对比
ax = axes[1, 0]
ax.plot(new_heat['elapsed_min'], new_heat['A-C'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat['elapsed_min'], old_heat['A-C'], 'r-', label='旧数据', linewidth=2)
ax.set_xlabel('时间 (min)')
ax.set_ylabel('A-C梯度 (°C)')
ax.set_title('A-C梯度随时间变化')
ax.legend()
ax.grid(True, alpha=0.3)

# 图5: A-B梯度 vs T1
ax = axes[1, 1]
mask_new = (new_heat['T1'] >= 38) & (new_heat['T1'] <= 60)
mask_old = (old_heat['T1'] >= 38) & (old_heat['T1'] <= 60)
ax.plot(new_heat.loc[mask_new, 'T1'], new_heat.loc[mask_new, 'A-B'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat.loc[mask_old, 'T1'], old_heat.loc[mask_old, 'A-B'], 'r-', label='旧数据', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-B梯度 (°C)')
ax.set_title('A-B梯度 vs T1')
ax.legend()
ax.grid(True, alpha=0.3)

# 图6: A-C梯度 vs T1
ax = axes[1, 2]
ax.plot(new_heat.loc[mask_new, 'T1'], new_heat.loc[mask_new, 'A-C'], 'b-', label='新数据', linewidth=2)
ax.plot(old_heat.loc[mask_old, 'T1'], old_heat.loc[mask_old, 'A-C'], 'r-', label='旧数据', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-C梯度 (°C)')
ax.set_title('A-C梯度 vs T1')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_30w_old_vs_new_heating_only.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_30w_old_vs_new_heating_only.pdf', bbox_inches='tight')
print("\n[图表已保存] output/paper/figures/gyroid_30w_old_vs_new_heating_only.png/pdf")
