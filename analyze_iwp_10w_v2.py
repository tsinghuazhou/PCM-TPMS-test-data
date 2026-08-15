"""IWP 10W 重新分析
B组 = T2/T3 平均（剔除T5）
C组 = T8/T9 平均（只保留T8、T9）
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_csv(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    df['elapsed_min'] = df['elapsed'] / 60
    return df

# IWP
iwp = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
iwp.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
iwp['time'] = pd.to_datetime(iwp['time'])
iwp['elapsed'] = (iwp['time'] - iwp['time'].iloc[0]).dt.total_seconds()
iwp['elapsed_min'] = iwp['elapsed'] / 60

# 新规则
iwp['B_avg'] = iwp[['T2','T3']].mean(axis=1)
iwp['C_avg'] = iwp[['T8','T9']].mean(axis=1)
iwp['A-B'] = iwp['T1'] - iwp['B_avg']
iwp['A-C'] = iwp['T1'] - iwp['C_avg']

# Gyroid / Primitive 保持原规则用于对比
gyroid = load_csv('temperature_record_20260808_165138gyroid10w.csv')
gyroid['B_avg'] = gyroid[['T2','T3','T5']].mean(axis=1)
gyroid['A-B'] = gyroid['T1'] - gyroid['B_avg']
gyroid['A-C'] = gyroid['T1'] - gyroid['T9']

primitive = load_csv('temperature_record_20260805_200423.csv')
primitive['B_avg'] = primitive[['T2','T3','T5']].mean(axis=1)
primitive['A-B'] = primitive['T1'] - primitive['B_avg']
primitive['A-C'] = primitive['T1'] - primitive['T9']

print("=" * 80)
print("IWP 10W 重新分析 (B=T2/T3, C=T8/T9)")
print("=" * 80)

print(f"\n[基本信息]")
print(f"行数: {len(iwp)}, 时长: {iwp.elapsed_min.iloc[-1]:.2f} min")
print(f"T1末值: {iwp.T1.iloc[-1]:.1f}°C, T8末值: {iwp.T8.iloc[-1]:.1f}°C, T9末值: {iwp.T9.iloc[-1]:.1f}°C")

# 到达42°C时间
print(f"\n[到达42°C时间]")
for c in ['T1', 'T2', 'T3', 'T8', 'T9']:
    idx = iwp.loc[iwp[c] >= 42, 'elapsed_min']
    t = idx.iloc[0] if len(idx) > 0 else np.nan
    print(f"  {c}: {t:.2f} min")

# B组均值到达42°C
iwp_b42 = iwp.loc[iwp['B_avg'] >= 42, 'elapsed_min']
print(f"  B_avg(T2/T3): {iwp_b42.iloc[0]:.2f} min" if len(iwp_b42) > 0 else "  B_avg: N/A")

# 熔融时长
mask = (iwp['T1'] >= 42) & (iwp['T1'] <= 52)
if mask.sum() > 1:
    dur = iwp.loc[mask, 'elapsed_min'].iloc[-1] - iwp.loc[mask, 'elapsed_min'].iloc[0]
    print(f"\n[熔融时长 (T1在42-52°C)]")
    print(f"  {dur:.2f} min")

# 梯度关键值
print(f"\n[梯度关键值]")
print(f"{'T1(°C)':>8} | {'A-B':>8} | {'A-C':>8}")
for t1 in [42, 45, 50, 55]:
    idx = iwp.T1.sub(t1).abs().idxmin()
    ab = iwp['A-B'].iloc[idx]
    ac = iwp['A-C'].iloc[idx]
    print(f"{t1:>8} | {ab:>8.1f} | {ac:>8.1f}")

# B组一致性
print(f"\n[B组一致性 T2/T3 (T1=45°C)]")
idx45 = iwp.T1.sub(45).abs().idxmin()
spread = abs(iwp.loc[idx45, 'T2'] - iwp.loc[idx45, 'T3'])
print(f"  T2={iwp.loc[idx45,'T2']:.1f}°C, T3={iwp.loc[idx45,'T3']:.1f}°C, spread={spread:.1f}°C")

# C组一致性
print(f"\n[C组一致性 T8/T9 (T1=45°C)]")
spread_c = abs(iwp.loc[idx45, 'T8'] - iwp.loc[idx45, 'T9'])
print(f"  T8={iwp.loc[idx45,'T8']:.1f}°C, T9={iwp.loc[idx45,'T9']:.1f}°C, spread={spread_c:.1f}°C")

# 三结构对比
print(f"\n{'='*80}")
print(f"IWP vs Gyroid vs Primitive 10W 对比")
print(f"{'='*80}")

print(f"\n[A-B梯度]")
print(f"{'T1(°C)':>8} | {'IWP':>8} | {'Gyroid':>8} | {'Primitive':>8}")
for t1 in [42, 50, 55]:
    iwp_val = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-B']
    gyro_val = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-B']
    prim_val = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-B']
    print(f"{t1:>8} | {iwp_val:>8.1f} | {gyro_val:>8.1f} | {prim_val:>8.1f}")

print(f"\n[A-C梯度]")
print(f"{'T1(°C)':>8} | {'IWP':>8} | {'Gyroid':>8} | {'Primitive':>8}")
for t1 in [42, 50, 55]:
    iwp_val = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-C']
    gyro_val = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-C']
    prim_val = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-C']
    print(f"{t1:>8} | {iwp_val:>8.1f} | {gyro_val:>8.1f} | {prim_val:>8.1f}")

# 熔融时长对比
print(f"\n[熔融时长]")
for name, df in [('IWP', iwp), ('Gyroid', gyroid), ('Primitive', primitive)]:
    m = (df['T1'] >= 42) & (df['T1'] <= 52)
    if m.sum() > 1:
        d = df.loc[m, 'elapsed_min'].iloc[-1] - df.loc[m, 'elapsed_min'].iloc[0]
        print(f"  {name}: {d:.1f} min")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: 所有传感器
ax = axes[0, 0]
for c in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    ax.plot(iwp.elapsed_min, iwp[c], label=c, linewidth=1.5, alpha=0.8)
ax.axhline(y=42, color='red', linestyle='--', alpha=0.5, label='Melting 42°C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (°C)')
ax.set_title('IWP 10W All Sensors'); ax.legend(fontsize=7, ncol=3); ax.grid(alpha=0.3)

# 图2: T1, B, C
ax = axes[0, 1]
ax.plot(iwp.elapsed_min, iwp.T1, 'r-', label='T1', linewidth=2.5)
ax.plot(iwp.elapsed_min, iwp.B_avg, 'g-', label='B (T2/T3)', linewidth=2.5)
ax.plot(iwp.elapsed_min, iwp.C_avg, 'b-', label='C (T8/T9)', linewidth=2.5)
ax.axhline(y=42, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Temperature (°C)')
ax.set_title('IWP 10W Key Positions'); ax.legend(); ax.grid(alpha=0.3)

# 图3: 梯度 vs 时间
ax = axes[0, 2]
ax.plot(iwp.elapsed_min, iwp['A-B'], 'g-', label='A-B', linewidth=2)
ax.plot(iwp.elapsed_min, iwp['A-C'], 'b-', label='A-C', linewidth=2)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Gradient (°C)')
ax.set_title('IWP 10W Gradients vs Time'); ax.legend(); ax.grid(alpha=0.3)

# 图4: A-B vs T1 三结构对比
ax = axes[1, 0]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    m = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[m, 'T1'], df.loc[m, 'A-B'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('A-B Gradient vs T1 (10W)'); ax.legend(); ax.grid(alpha=0.3)

# 图5: A-C vs T1 三结构对比
ax = axes[1, 1]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    m = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[m, 'T1'], df.loc[m, 'A-C'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C Gradient (°C)')
ax.set_title('A-C Gradient vs T1 (10W)'); ax.legend(); ax.grid(alpha=0.3)

# 图6: T1温度曲线三结构对比
ax = axes[1, 2]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    ax.plot(df.elapsed_min, df.T1, color=color, label=name, linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('T1 (°C)')
ax.set_title('T1 Temperature (10W)'); ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/iwp_10w_reanalysis.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/iwp_10w_reanalysis.pdf', bbox_inches='tight')
print(f"\n[图表已保存] output/paper/figures/iwp_10w_reanalysis.png/pdf")
