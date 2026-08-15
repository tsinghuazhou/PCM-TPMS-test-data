"""IWP 10W vs 20W 功率效应对比分析"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_iwp_10w():
    iwp = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
    iwp.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    iwp['time'] = pd.to_datetime(iwp['time'])
    iwp['elapsed'] = (iwp['time'] - iwp['time'].iloc[0]).dt.total_seconds()
    iwp['elapsed_min'] = iwp['elapsed'] / 60
    iwp['B_avg'] = iwp[['T2','T3']].mean(axis=1)
    iwp['C_avg'] = iwp[['T8','T9']].mean(axis=1)
    iwp['A-B'] = iwp['T1'] - iwp['B_avg']
    iwp['A-C'] = iwp['T1'] - iwp['C_avg']
    return iwp

def load_iwp_20w():
    df = pd.read_csv('temperature_record_20260809_201218iwp20w.csv', encoding='gbk')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df = df.dropna(subset=['T1']).reset_index(drop=True)
    # 时间列只有分钟精度，用行号作为秒数（1Hz采样）
    df['elapsed'] = df.index.astype(float)  # 秒
    df['elapsed_min'] = df['elapsed'] / 60.0
    df['B_avg'] = df[['T2','T3']].mean(axis=1)
    df['C_avg'] = df[['T8','T9']].mean(axis=1)
    df['A-B'] = df['T1'] - df['B_avg']
    df['A-C'] = df['T1'] - df['C_avg']
    return df

iwp10 = load_iwp_10w()
iwp20 = load_iwp_20w()

print("=" * 80)
print("IWP 10W vs 20W 功率效应对比")
print("=" * 80)

# 1. 基本信息对比
print("\n[1] 基本信息")
print(f"{'指标':>15} | {'10W':>10} | {'20W':>10} | {'倍数':>8}")
print(f"{'时长(min)':>15} | {iwp10.elapsed_min.iloc[-1]:>10.1f} | {iwp20.elapsed_min.iloc[-1]:>10.1f} | {iwp10.elapsed_min.iloc[-1]/iwp20.elapsed_min.iloc[-1]:>8.1f}x")
print(f"{'T1末值(°C)':>15} | {iwp10.T1.iloc[-1]:>10.1f} | {iwp20.T1.iloc[-1]:>10.1f} | {iwp20.T1.iloc[-1]/iwp10.T1.iloc[-1]:>8.1f}x")

# 2. 到达42°C时间对比
print("\n[2] 到达42°C时间")
print(f"{'传感器':>10} | {'10W':>10} | {'20W':>10} | {'倍数':>8}")
for c in ['T1', 'B_avg', 'C_avg']:
    t10 = iwp10.loc[iwp10[c] >= 42, 'elapsed_min'].iloc[0] if len(iwp10.loc[iwp10[c] >= 42]) > 0 else np.nan
    t20 = iwp20.loc[iwp20[c] >= 42, 'elapsed_min'].iloc[0] if len(iwp20.loc[iwp20[c] >= 42]) > 0 else np.nan
    ratio = t10/t20 if t20 > 0 else np.nan
    print(f"{c:>10} | {t10:>10.1f} | {t20:>10.1f} | {ratio:>8.1f}x")

# 3. 熔融时长对比
print("\n[3] 熔融时长 (T1在42-52°C)")
for name, df in [('10W', iwp10), ('20W', iwp20)]:
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        dur = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
        print(f"  {name}: {dur:.1f} min")

# 4. 梯度对比
print("\n[4] A-B梯度对比")
print(f"{'T1(°C)':>8} | {'10W':>8} | {'20W':>8} | {'倍数':>8}")
for t1 in [42, 45, 50, 55]:
    v10 = iwp10.loc[iwp10.T1.sub(t1).abs().idxmin(), 'A-B']
    v20 = iwp20.loc[iwp20.T1.sub(t1).abs().idxmin(), 'A-B']
    ratio = v20/v10 if v10 > 0 else np.nan
    print(f"{t1:>8} | {v10:>8.1f} | {v20:>8.1f} | {ratio:>8.1f}x")

print("\n[5] A-C梯度对比")
print(f"{'T1(°C)':>8} | {'10W':>8} | {'20W':>8} | {'倍数':>8}")
for t1 in [42, 45, 50, 55]:
    v10 = iwp10.loc[iwp10.T1.sub(t1).abs().idxmin(), 'A-C']
    v20 = iwp20.loc[iwp20.T1.sub(t1).abs().idxmin(), 'A-C']
    ratio = v20/v10 if v10 > 0 else np.nan
    print(f"{t1:>8} | {v10:>8.1f} | {v20:>8.1f} | {ratio:>8.1f}x")

# 5. 梯度稳定性对比
print("\n[6] 梯度稳定性 (42°C→55°C膨胀率)")
for name, df in [('10W', iwp10), ('20W', iwp20)]:
    ab42 = df.loc[df.T1.sub(42).abs().idxmin(), 'A-B']
    ab55 = df.loc[df.T1.sub(55).abs().idxmin(), 'A-B']
    rate = (ab55 - ab42) / ab42 * 100
    print(f"  {name}: {ab42:.1f} → {ab55:.1f}°C ({rate:+.1f}%)")

# 绘图
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 图1: T1温度曲线
ax = axes[0, 0]
ax.plot(iwp10.elapsed_min, iwp10.T1, 'b-', label='10W', linewidth=2)
ax.plot(iwp20.elapsed_min, iwp20.T1, 'r-', label='20W', linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5, label='Melting 42°C')
ax.set_xlabel('Time (min)'); ax.set_ylabel('T1 (°C)')
ax.set_title('T1 Temperature vs Time'); ax.legend(); ax.grid(alpha=0.3)

# 图2: B组温度曲线
ax = axes[0, 1]
ax.plot(iwp10.elapsed_min, iwp10.B_avg, 'b-', label='10W', linewidth=2)
ax.plot(iwp20.elapsed_min, iwp20.B_avg, 'r-', label='20W', linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('B_avg (°C)')
ax.set_title('B Group (T2/T3) Temperature'); ax.legend(); ax.grid(alpha=0.3)

# 图3: C组温度曲线
ax = axes[0, 2]
ax.plot(iwp10.elapsed_min, iwp10.C_avg, 'b-', label='10W', linewidth=2)
ax.plot(iwp20.elapsed_min, iwp20.C_avg, 'r-', label='20W', linewidth=2)
ax.axhline(42, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Time (min)'); ax.set_ylabel('C_avg (°C)')
ax.set_title('C Group (T8/T9) Temperature'); ax.legend(); ax.grid(alpha=0.3)

# 图4: A-B梯度 vs T1
ax = axes[1, 0]
mask10 = (iwp10.T1 >= 38) & (iwp10.T1 <= 60)
mask20 = (iwp20.T1 >= 38) & (iwp20.T1 <= 60)
ax.plot(iwp10.loc[mask10, 'T1'], iwp10.loc[mask10, 'A-B'], 'b-', label='10W', linewidth=2)
ax.plot(iwp20.loc[mask20, 'T1'], iwp20.loc[mask20, 'A-B'], 'r-', label='20W', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('A-B Gradient vs T1'); ax.legend(); ax.grid(alpha=0.3)

# 图5: A-C梯度 vs T1
ax = axes[1, 1]
ax.plot(iwp10.loc[mask10, 'T1'], iwp10.loc[mask10, 'A-C'], 'b-', label='10W', linewidth=2)
ax.plot(iwp20.loc[mask20, 'T1'], iwp20.loc[mask20, 'A-C'], 'r-', label='20W', linewidth=2)
ax.axvspan(42, 52, alpha=0.3, color='gray', label='Phase change')
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-C Gradient (°C)')
ax.set_title('A-C Gradient vs T1'); ax.legend(); ax.grid(alpha=0.3)

# 图6: 梯度柱状图对比
ax = axes[1, 2]
t1_vals = [42, 50, 55]
x = np.arange(len(t1_vals))
width = 0.35
ab10 = [iwp10.loc[iwp10.T1.sub(t).abs().idxmin(), 'A-B'] for t in t1_vals]
ab20 = [iwp20.loc[iwp20.T1.sub(t).abs().idxmin(), 'A-B'] for t in t1_vals]
bars1 = ax.bar(x - width/2, ab10, width, label='10W', color='blue', alpha=0.7)
bars2 = ax.bar(x + width/2, ab20, width, label='20W', color='red', alpha=0.7)
ax.set_xlabel('T1 (°C)'); ax.set_ylabel('A-B Gradient (°C)')
ax.set_title('A-B Gradient at Different T1')
ax.set_xticks(x); ax.set_xticklabels([f'{t}°C' for t in t1_vals])
ax.legend(); ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/paper/figures/iwp_10w_vs_20w_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/iwp_10w_vs_20w_comparison.pdf', bbox_inches='tight')
print(f"\n[对比图已保存] output/paper/figures/iwp_10w_vs_20w_comparison.png/pdf")
