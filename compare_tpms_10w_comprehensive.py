"""三种TPMS晶格10W功率综合对比分析"""
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

# 加载数据
gyroid = load_csv('temperature_record_20260808_165138gyroid10w.csv')
gyroid['B_avg'] = gyroid[['T2','T3','T5']].mean(axis=1)
gyroid['A-B'] = gyroid['T1'] - gyroid['B_avg']
gyroid['A-C'] = gyroid['T1'] - gyroid['T9']

primitive = load_csv('temperature_record_20260805_200423.csv')
primitive['B_avg'] = primitive[['T2','T3','T5']].mean(axis=1)
primitive['A-B'] = primitive['T1'] - primitive['B_avg']
primitive['A-C'] = primitive['T1'] - primitive['T9']

iwp = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
iwp.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
iwp['time'] = pd.to_datetime(iwp['time'])
iwp['elapsed'] = (iwp['time'] - iwp['time'].iloc[0]).dt.total_seconds()
iwp['elapsed_min'] = iwp['elapsed'] / 60
iwp['B_avg'] = iwp[['T2','T3']].mean(axis=1)  # IWP: T2/T3
iwp['C_avg'] = iwp[['T8','T9']].mean(axis=1)  # IWP: T8/T9
iwp['A-B'] = iwp['T1'] - iwp['B_avg']
iwp['A-C'] = iwp['T1'] - iwp['C_avg']

print("=" * 80)
print("三种TPMS晶格10W功率综合对比")
print("=" * 80)

# 1. 梯度对比表
print("\n[1] A-B梯度对比 (B组定义不同，注意口径)")
print(f"{'T1(°C)':>8} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10} | {'IWP排名':>8}")
print(f"{'':>8} | {'(T2/T3/T5)':>10} | {'(T2/T3)':>10} | {'(T2/T3/T5)':>10} | {'':>8}")
for t1 in [42, 45, 50, 55]:
    g = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-B']
    i = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-B']
    p = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-B']
    rank = sorted([g, i, p]).index(i) + 1
    rank_str = ['1st', '2nd', '3rd'][rank-1]
    print(f"{t1:>8} | {g:>10.1f} | {i:>10.1f} | {p:>10.1f} | {rank_str:>8}")

print("\n[2] A-C梯度对比")
print(f"{'T1(°C)':>8} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10} | {'IWP排名':>8}")
print(f"{'':>8} | {'(T9)':>10} | {'(T8/T9)':>10} | {'(T9)':>10} | {'':>8}")
for t1 in [42, 45, 50, 55]:
    g = gyroid.loc[gyroid.T1.sub(t1).abs().idxmin(), 'A-C']
    i = iwp.loc[iwp.T1.sub(t1).abs().idxmin(), 'A-C']
    p = primitive.loc[primitive.T1.sub(t1).abs().idxmin(), 'A-C']
    rank = sorted([g, i, p]).index(i) + 1
    rank_str = ['1st', '2nd', '3rd'][rank-1]
    print(f"{t1:>8} | {g:>10.1f} | {i:>10.1f} | {p:>10.1f} | {rank_str:>8}")

# 3. 梯度稳定性（相变窗口内膨胀率）
print("\n[3] 梯度稳定性（42°C→55°C膨胀率）")
g_ab_42 = gyroid.loc[gyroid.T1.sub(42).abs().idxmin(), 'A-B']
g_ab_55 = gyroid.loc[gyroid.T1.sub(55).abs().idxmin(), 'A-B']
i_ab_42 = iwp.loc[iwp.T1.sub(42).abs().idxmin(), 'A-B']
i_ab_55 = iwp.loc[iwp.T1.sub(55).abs().idxmin(), 'A-B']
p_ab_42 = primitive.loc[primitive.T1.sub(42).abs().idxmin(), 'A-B']
p_ab_55 = primitive.loc[primitive.T1.sub(55).abs().idxmin(), 'A-B']

print(f"  Gyroid:    {g_ab_42:.1f} → {g_ab_55:.1f}°C ({(g_ab_55-g_ab_42)/g_ab_42*100:+.1f}%)")
print(f"  IWP:       {i_ab_42:.1f} → {i_ab_55:.1f}°C ({(i_ab_55-i_ab_42)/i_ab_42*100:+.1f}%)")
print(f"  Primitive: {p_ab_42:.1f} → {p_ab_55:.1f}°C ({(p_ab_55-p_ab_42)/p_ab_42*100:+.1f}%)")

# 4. 熔融时长
print("\n[4] 熔融时长 (T1在42-52°C)")
for name, df in [('Gyroid', gyroid), ('IWP', iwp), ('Primitive', primitive)]:
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
        print(f"  {name}: {dur:.1f} min")

# 5. 到达42°C时间
print("\n[5] 到达42°C时间")
print(f"{'传感器':>8} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10}")
for c in ['T1', 'T8/T9', 'B_avg']:
    g_t = gyroid.loc[gyroid[c] >= 42, 'elapsed_min'].iloc[0] if c != 'T8/T9' else gyroid.loc[gyroid['T9'] >= 42, 'elapsed_min'].iloc[0]
    i_t = iwp.loc[iwp[c] >= 42, 'elapsed_min'].iloc[0] if c != 'T8/T9' else iwp.loc[iwp['C_avg'] >= 42, 'elapsed_min'].iloc[0]
    p_t = primitive.loc[primitive[c] >= 42, 'elapsed_min'].iloc[0] if c != 'T8/T9' else primitive.loc[primitive['T9'] >= 42, 'elapsed_min'].iloc[0]
    print(f"{c:>8} | {g_t:>10.1f} | {i_t:>10.1f} | {p_t:>10.1f}")

# 6. 新发现：IWP的A-B梯度在55°C时下降
print("\n[6] 新发现：IWP的A-B梯度异常行为")
print(f"  IWP A-B梯度: 42°C={i_ab_42:.1f}°C, 50°C={iwp.loc[iwp.T1.sub(50).abs().idxmin(), 'A-B']:.1f}°C, 55°C={i_ab_55:.1f}°C")
print(f"  → IWP在50-55°C区间A-B梯度下降({iwp.loc[iwp.T1.sub(50).abs().idxmin(), 'A-B']:.1f}→{i_ab_55:.1f}°C)")
print(f"  → Gyroid和Primitive的A-B梯度持续上升或持平")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: A-B梯度 vs T1
ax = axes[0, 0]
for name, df, color in [('Gyroid', gyroid, 'blue'), ('IWP', iwp, 'purple'), ('Primitive', primitive, 'red')]:
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], df.loc[mask, 'A-B'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('A-B Gradient vs T1 (10W)'); ax.legend(); ax.grid(alpha=0.3)

# 图2: A-C梯度 vs T1
ax = axes[0, 1]
for name, df, color in [('Gyroid', gyroid, 'blue'), ('IWP', iwp, 'purple'), ('Primitive', primitive, 'red')]:
    mask = (df['T1'] >= 38) & (df['T1'] <= 60)
    ax.plot(df.loc[mask, 'T1'], df.loc[mask, 'A-C'], color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C Gradient (°C)')
ax.set_title('A-C Gradient vs T1 (10W)'); ax.legend(); ax.grid(alpha=0.3)

# 图3: 梯度稳定性对比
ax = axes[0, 2]
t1_range = np.linspace(42, 55, 50)
for name, df, color in [('Gyroid', gyroid, 'blue'), ('IWP', iwp, 'purple'), ('Primitive', primitive, 'red')]:
    ab_vals = []
    for t1 in t1_range:
        idx = df.T1.sub(t1).abs().idxmin()
        ab_vals.append(df['A-B'].iloc[idx])
    ax.plot(t1_range, ab_vals, color=color, label=name, linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('Gradient Stability (42-55°C)'); ax.legend(); ax.grid(alpha=0.3)

# 图4: 熔融时长对比
ax = axes[1, 0]
durations = []
for name, df in [('Gyroid', gyroid), ('IWP', iwp), ('Primitive', primitive)]:
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
        durations.append(dur)
bars = ax.bar(['Gyroid', 'IWP', 'Primitive'], durations, color=['blue', 'purple', 'red'], alpha=0.7, edgecolor='k')
ax.set_ylabel('Melting Duration (min)')
ax.set_title('Melting Duration (T1 in 42-52°C)')
for bar, dur in zip(bars, durations):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{dur:.1f}', ha='center', va='bottom', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

# 图5: 温度-时间曲线 (T1)
ax = axes[1, 1]
for name, df, color in [('Gyroid', gyroid, 'blue'), ('IWP', iwp, 'purple'), ('Primitive', primitive, 'red')]:
    ax.plot(df.elapsed_min, df.T1, color=color, label=name, linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5, label='Melting 42°C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('T1 (°C)')
ax.set_title('T1 Temperature vs Time (10W)'); ax.legend(); ax.grid(alpha=0.3)

# 图6: 梯度膨胀率对比
ax = axes[1, 2]
structures = ['Gyroid', 'IWP', 'Primitive']
expansion_rates = [(g_ab_55-g_ab_42)/g_ab_42*100, (i_ab_55-i_ab_42)/i_ab_42*100, (p_ab_55-p_ab_42)/p_ab_42*100]
colors = ['blue', 'purple', 'red']
bars = ax.bar(structures, expansion_rates, color=colors, alpha=0.7, edgecolor='k')
ax.set_ylabel('A-B Gradient Expansion (%)')
ax.set_title('Gradient Expansion Rate (42→55°C)')
ax.axhline(0, color='k', linestyle='-', linewidth=0.5)
for bar, rate in zip(bars, expansion_rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{rate:+.1f}%', ha='center', va='bottom', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/tpms_10w_comprehensive_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/tpms_10w_comprehensive_comparison.pdf', bbox_inches='tight')
print(f"\n[图表已保存] output/paper/figures/tpms_10w_comprehensive_comparison.png/pdf")
