"""IWP vs Gyroid vs Primitive 10W对比分析"""
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
    df['B_avg'] = df[['T2','T3','T5']].mean(axis=1)
    df['A-B'] = df['T1'] - df['B_avg']
    df['A-C'] = df['T1'] - df['T9']
    return df

# 加载数据
iwp = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
iwp.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
iwp['time'] = pd.to_datetime(iwp['time'])
iwp['elapsed'] = (iwp['time'] - iwp['time'].iloc[0]).dt.total_seconds()
iwp['elapsed_min'] = iwp['elapsed'] / 60
iwp['B_avg'] = iwp[['T2','T3','T5']].mean(axis=1)
iwp['A-B'] = iwp['T1'] - iwp['B_avg']
iwp['A-C'] = iwp['T1'] - iwp['T9']

gyroid = load_csv('temperature_record_20260808_165138gyroid10w.csv')
primitive = load_csv('temperature_record_20260805_200423.csv')

print("=" * 80)
print("IWP vs Gyroid vs Primitive 10W 对比")
print("=" * 80)

print("\n[A-B梯度对比 (T1=42°C, 50°C, 55°C)]")
print(f"{'T1(°C)':>8} | {'IWP':>8} | {'Gyroid':>8} | {'Primitive':>8}")
for t1 in [42, 50, 55]:
    iwp_val = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-B']
    gyro_val = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-B']
    prim_val = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-B']
    print(f"{t1:>8} | {iwp_val:>8.1f} | {gyro_val:>8.1f} | {prim_val:>8.1f}")

print("\n[A-C梯度对比 (T1=42°C, 50°C, 55°C)]")
print(f"{'T1(°C)':>8} | {'IWP':>8} | {'Gyroid':>8} | {'Primitive':>8}")
for t1 in [42, 50, 55]:
    iwp_val = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-C']
    gyro_val = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-C']
    prim_val = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-C']
    print(f"{t1:>8} | {iwp_val:>8.1f} | {gyro_val:>8.1f} | {prim_val:>8.1f}")

print("\n[熔融时长 (T1在42-52°C)]")
for name, df in [('IWP', iwp), ('Gyroid', gyroid), ('Primitive', primitive)]:
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
        print(f"  {name}: {dur:.1f} min")

print("\n[到达42°C时间]")
print(f"{'传感器':>8} | {'IWP':>8} | {'Gyroid':>8} | {'Primitive':>8}")
for c in ['T1', 'T9']:
    iwp_t = iwp.loc[iwp[c] >= 42, 'elapsed_min'].iloc[0] if len(iwp.loc[iwp[c] >= 42]) > 0 else np.nan
    gyro_t = gyroid.loc[gyroid[c] >= 42, 'elapsed_min'].iloc[0] if len(gyroid.loc[gyroid[c] >= 42]) > 0 else np.nan
    prim_t = primitive.loc[primitive[c] >= 42, 'elapsed_min'].iloc[0] if len(primitive.loc[primitive[c] >= 42]) > 0 else np.nan
    print(f"{c:>8} | {iwp_t:>8.1f} | {gyro_t:>8.1f} | {prim_t:>8.1f}")

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1: A-B梯度 vs T1
ax = axes[0, 0]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], df.loc[mask, 'A-B'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-B 梯度 (°C)')
ax.set_title('A-B 梯度 vs T1 (10W)')
ax.legend()
ax.grid(True, alpha=0.3)

# 图2: A-C梯度 vs T1
ax = axes[0, 1]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], df.loc[mask, 'A-C'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='相变窗口')
ax.set_xlabel('T1 (°C)')
ax.set_ylabel('A-C 梯度 (°C)')
ax.set_title('A-C 梯度 vs T1 (10W, C=T9)')
ax.legend()
ax.grid(True, alpha=0.3)

# 图3: 温度-时间曲线 (T1)
ax = axes[1, 0]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    ax.plot(df.elapsed_min, df.T1, color=color, label=name, linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5, label='熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('T1 温度 (°C)')
ax.set_title('T1 温度-时间曲线 (10W)')
ax.legend()
ax.grid(True, alpha=0.3)

# 图4: 温度-时间曲线 (T9)
ax = axes[1, 1]
for name, df, color in [('IWP', iwp, 'purple'), ('Gyroid', gyroid, 'blue'), ('Primitive', primitive, 'red')]:
    ax.plot(df.elapsed_min, df.T9, color=color, label=name, linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5, label='熔点 42°C')
ax.set_xlabel('时间 (min)')
ax.set_ylabel('T9 温度 (°C)')
ax.set_title('T9 温度-时间曲线 (10W)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/iwp_vs_gyroid_primitive_10w.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/iwp_vs_gyroid_primitive_10w.pdf', bbox_inches='tight')
print(f"\n[对比图已保存] output/paper/figures/iwp_vs_gyroid_primitive_10w.png/pdf")
