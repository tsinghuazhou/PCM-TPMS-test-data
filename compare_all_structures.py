"""三种TPMS结构全面对比分析 (Gyroid/IWP/Primitive, 10W/20W/30W)"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_csv(path, encoding='utf-8-sig'):
    df = pd.read_csv(path, encoding=encoding)
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df = df.dropna(subset=['T1']).reset_index(drop=True)
    df['elapsed'] = df.index.astype(float)  # 秒
    df['elapsed_min'] = df['elapsed'] / 60.0
    return df

def calc_metrics(df, structure):
    """计算关键指标"""
    # B组和C组定义
    if structure == 'IWP':
        df['B_avg'] = df[['T2','T3']].mean(axis=1)  # 剔除T5
        if 'C_avg' in df.columns:
            pass  # 20W使用T8/T9平均
        else:
            df['C_val'] = df['T9']  # 10W/30W使用T9单点
    else:  # Gyroid/Primitive
        df['B_avg'] = df[['T2','T3','T5']].mean(axis=1)
        df['C_val'] = df['T9']
    
    # 计算梯度
    df['A-B'] = df['T1'] - df['B_avg']
    if structure == 'IWP' and 'C_avg' in df.columns:
        df['A-C'] = df['T1'] - df['C_avg']
    else:
        df['A-C'] = df['T1'] - df['C_val']
    
    # 熔融时长
    mask = (df['T1'] >= 42) & (df['T1'] <= 52)
    if mask.sum() > 1:
        melting_duration = df.loc[mask, 'elapsed_min'].iloc[-1] - df.loc[mask, 'elapsed_min'].iloc[0]
    else:
        melting_duration = 0
    
    # 到达42°C时间
    t1_42 = df.loc[df['T1'] >= 42, 'elapsed_min'].iloc[0] if len(df.loc[df['T1'] >= 42]) > 0 else np.nan
    t9_42 = df.loc[df['T9'] >= 42, 'elapsed_min'].iloc[0] if len(df.loc[df['T9'] >= 42]) > 0 else np.nan
    
    # 梯度关键值
    ab_42 = df.loc[df['T1'].sub(42).abs().idxmin(), 'A-B']
    ab_50 = df.loc[df['T1'].sub(50).abs().idxmin(), 'A-B']
    ab_55 = df.loc[df['T1'].sub(55).abs().idxmin(), 'A-B']
    ac_42 = df.loc[df['T1'].sub(42).abs().idxmin(), 'A-C']
    ac_50 = df.loc[df['T1'].sub(50).abs().idxmin(), 'A-C']
    ac_55 = df.loc[df['T1'].sub(55).abs().idxmin(), 'A-C']
    
    # 梯度稳定性
    ab_expansion = (ab_55 - ab_42) / ab_42 * 100
    
    return {
        'melting_duration': melting_duration,
        't1_42': t1_42,
        't9_42': t9_42,
        'ab_42': ab_42,
        'ab_50': ab_50,
        'ab_55': ab_55,
        'ac_42': ac_42,
        'ac_50': ac_50,
        'ac_55': ac_55,
        'ab_expansion': ab_expansion,
        'duration': df['elapsed_min'].iloc[-1],
        't1_end': df['T1'].iloc[-1]
    }

# 加载所有数据
print("=" * 80)
print("三种TPMS结构全面对比分析")
print("=" * 80)

# 10W数据
gyroid_10w = load_csv('temperature_record_20260808_165138gyroid10w.csv')
iwp_10w = pd.read_excel('temperature_record_20260809_170915 (1).xlsx')
iwp_10w.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
iwp_10w['time'] = pd.to_datetime(iwp_10w['time'])
iwp_10w['elapsed'] = (iwp_10w['time'] - iwp_10w['time'].iloc[0]).dt.total_seconds()
iwp_10w['elapsed_min'] = iwp_10w['elapsed'] / 60
iwp_10w['C_avg'] = iwp_10w[['T8','T9']].mean(axis=1)  # 10W使用T8/T9平均
primitive_10w = load_csv('temperature_record_20260805_200423.csv')

# 20W数据
gyroid_20w = load_csv('temperature_record_20260808_190451 (4).csv')
iwp_20w = load_csv('temperature_record_20260809_201218iwp20w.csv', encoding='gbk')
iwp_20w['C_avg'] = iwp_20w[['T8','T9']].mean(axis=1)  # 20W使用T8/T9平均
primitive_20w = load_csv('temperature_record_20260806_214551.csv')

# 30W数据
gyroid_30w = load_csv('temperature_record_20260808_203206.csv')
iwp_30w = load_csv('temperature_record_20260810_152336iwp30w.csv')
primitive_30w = load_csv('temperature_record_20260807_193935.csv')

# 计算所有指标
results = {}
for power, data in [('10W', [(gyroid_10w, 'Gyroid'), (iwp_10w, 'IWP'), (primitive_10w, 'Primitive')]),
                     ('20W', [(gyroid_20w, 'Gyroid'), (iwp_20w, 'IWP'), (primitive_20w, 'Primitive')]),
                     ('30W', [(gyroid_30w, 'Gyroid'), (iwp_30w, 'IWP'), (primitive_30w, 'Primitive')])]:
    results[power] = {}
    for df, structure in data:
        results[power][structure] = calc_metrics(df, structure)

# 打印对比表
print("\n【10W功率对比】")
print(f"{'指标':<20} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10}")
print("-" * 60)
for metric, label in [('melting_duration', '熔融时长(min)'), ('ab_42', 'A-B@42°C'), 
                       ('ab_55', 'A-B@55°C'), ('ab_expansion', 'A-B膨胀率(%)'),
                       ('t1_42', 'T1达42°C(min)'), ('t9_42', 'T9达42°C(min)')]:
    g = results['10W']['Gyroid'][metric]
    i = results['10W']['IWP'][metric]
    p = results['10W']['Primitive'][metric]
    print(f"{label:<20} | {g:>10.2f} | {i:>10.2f} | {p:>10.2f}")

print("\n【20W功率对比】")
print(f"{'指标':<20} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10}")
print("-" * 60)
for metric, label in [('melting_duration', '熔融时长(min)'), ('ab_42', 'A-B@42°C'), 
                       ('ab_55', 'A-B@55°C'), ('ab_expansion', 'A-B膨胀率(%)'),
                       ('t1_42', 'T1达42°C(min)'), ('t9_42', 'T9达42°C(min)')]:
    g = results['20W']['Gyroid'][metric]
    i = results['20W']['IWP'][metric]
    p = results['20W']['Primitive'][metric]
    print(f"{label:<20} | {g:>10.2f} | {i:>10.2f} | {p:>10.2f}")

print("\n【30W功率对比】")
print(f"{'指标':<20} | {'Gyroid':>10} | {'IWP':>10} | {'Primitive':>10}")
print("-" * 60)
for metric, label in [('melting_duration', '熔融时长(min)'), ('ab_42', 'A-B@42°C'), 
                       ('ab_55', 'A-B@55°C'), ('ab_expansion', 'A-B膨胀率(%)'),
                       ('t1_42', 'T1达42°C(min)'), ('t9_42', 'T9达42°C(min)')]:
    g = results['30W']['Gyroid'][metric]
    i = results['30W']['IWP'][metric]
    p = results['30W']['Primitive'][metric]
    print(f"{label:<20} | {g:>10.2f} | {i:>10.2f} | {p:>10.2f}")

# 功率效应对比
print("\n【功率效应：10W→20W→30W】")
print(f"{'结构':<10} | {'熔融时长缩短':>15} | {'A-B@42增大':>15} | {'膨胀率增加':>15}")
print("-" * 60)
for structure in ['Gyroid', 'IWP', 'Primitive']:
    melt_10 = results['10W'][structure]['melting_duration']
    melt_20 = results['20W'][structure]['melting_duration']
    melt_30 = results['30W'][structure]['melting_duration']
    
    ab_10 = results['10W'][structure]['ab_42']
    ab_20 = results['20W'][structure]['ab_42']
    ab_30 = results['30W'][structure]['ab_42']
    
    exp_10 = results['10W'][structure]['ab_expansion']
    exp_20 = results['20W'][structure]['ab_expansion']
    exp_30 = results['30W'][structure]['ab_expansion']
    
    melt_ratio = f"{melt_10/melt_20:.1f}x / {melt_10/melt_30:.1f}x"
    ab_ratio = f"{ab_20/ab_10:.1f}x / {ab_30/ab_10:.1f}x"
    exp_ratio = f"{exp_20/exp_10:.1f}x / {exp_30/exp_10:.1f}x"
    
    print(f"{structure:<10} | {melt_ratio:>15} | {ab_ratio:>15} | {exp_ratio:>15}")

# 生成综合对比图表
fig = plt.figure(figsize=(20, 12))

# 图1: 熔融时长对比 (3x3网格)
ax1 = plt.subplot(3, 3, 1)
powers = ['10W', '20W', '30W']
structures = ['Gyroid', 'IWP', 'Primitive']
colors = {'Gyroid': 'blue', 'IWP': 'purple', 'Primitive': 'red'}

x = np.arange(len(powers))
width = 0.25
for i, struct in enumerate(structures):
    values = [results[p][struct]['melting_duration'] for p in powers]
    ax1.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax1.set_ylabel('Melting Duration (min)')
ax1.set_title('Melting Duration')
ax1.set_xticks(x + width)
ax1.set_xticklabels(powers)
ax1.legend()
ax1.grid(True, alpha=0.3)

# 图2: A-B@42°C梯度对比
ax2 = plt.subplot(3, 3, 2)
for i, struct in enumerate(structures):
    values = [results[p][struct]['ab_42'] for p in powers]
    ax2.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax2.set_ylabel('A-B Gradient @ 42°C (°C)')
ax2.set_title('A-B Gradient @ 42°C')
ax2.set_xticks(x + width)
ax2.set_xticklabels(powers)
ax2.legend()
ax2.grid(True, alpha=0.3)

# 图3: A-B梯度膨胀率对比
ax3 = plt.subplot(3, 3, 3)
for i, struct in enumerate(structures):
    values = [results[p][struct]['ab_expansion'] for p in powers]
    ax3.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax3.set_ylabel('A-B Expansion Rate (%)')
ax3.set_title('A-B Gradient Expansion (42→55°C)')
ax3.set_xticks(x + width)
ax3.set_xticklabels(powers)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 图4: T1达42°C时间对比
ax4 = plt.subplot(3, 3, 4)
for i, struct in enumerate(structures):
    values = [results[p][struct]['t1_42'] for p in powers]
    ax4.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax4.set_ylabel('Time to 42°C (min)')
ax4.set_title('T1 Reaches 42°C')
ax4.set_xticks(x + width)
ax4.set_xticklabels(powers)
ax4.legend()
ax4.grid(True, alpha=0.3)

# 图5: T9达42°C时间对比
ax5 = plt.subplot(3, 3, 5)
for i, struct in enumerate(structures):
    values = [results[p][struct]['t9_42'] for p in powers]
    ax5.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax5.set_ylabel('Time to 42°C (min)')
ax5.set_title('T9 Reaches 42°C')
ax5.set_xticks(x + width)
ax5.set_xticklabels(powers)
ax5.legend()
ax5.grid(True, alpha=0.3)

# 图6: A-B@55°C梯度对比
ax6 = plt.subplot(3, 3, 6)
for i, struct in enumerate(structures):
    values = [results[p][struct]['ab_55'] for p in powers]
    ax6.bar(x + i*width, values, width, label=struct, color=colors[struct], alpha=0.7)
ax6.set_ylabel('A-B Gradient @ 55°C (°C)')
ax6.set_title('A-B Gradient @ 55°C')
ax6.set_xticks(x + width)
ax6.set_xticklabels(powers)
ax6.legend()
ax6.grid(True, alpha=0.3)

# 图7-9: 温度曲线对比 (10W/20W/30W)
for idx, power in enumerate(['10W', '20W', '30W']):
    ax = plt.subplot(3, 3, 7 + idx)
    dfs = [(gyroid_10w, 'Gyroid', 'blue'), (iwp_10w, 'IWP', 'purple'), (primitive_10w, 'Primitive', 'red')] if power == '10W' else \
          [(gyroid_20w, 'Gyroid', 'blue'), (iwp_20w, 'IWP', 'purple'), (primitive_20w, 'Primitive', 'red')] if power == '20W' else \
          [(gyroid_30w, 'Gyroid', 'blue'), (iwp_30w, 'IWP', 'purple'), (primitive_30w, 'Primitive', 'red')]
    
    for df, struct, color in dfs:
        ax.plot(df['elapsed_min'], df['T1'], label=struct, color=color, linewidth=2)
    ax.axhline(y=42, color='green', linestyle='--', alpha=0.5, label='Melting 42°C')
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('T1 (°C)')
    ax.set_title(f'T1 Temperature - {power}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/tpms_comprehensive_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/tpms_comprehensive_comparison.pdf', bbox_inches='tight')
print("\n[图表已保存] output/paper/figures/tpms_comprehensive_comparison.png/pdf")

# 保存详细数据到CSV
summary_data = []
for power in ['10W', '20W', '30W']:
    for struct in ['Gyroid', 'IWP', 'Primitive']:
        row = {'Power': power, 'Structure': struct}
        row.update(results[power][struct])
        summary_data.append(row)

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('output/paper/data/tpms_comprehensive_comparison.csv', index=False)
print("[数据已保存] output/paper/data/tpms_comprehensive_comparison.csv")
