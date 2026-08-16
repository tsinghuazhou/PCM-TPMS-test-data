import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

EMA_ALPHA = 0.4

def load_and_process(filepath, is_csv=False):
    if is_csv:
        df = pd.read_csv(filepath, parse_dates=[0])
    else:
        df = pd.read_excel(filepath)
    df.columns = ['时间', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
    elapsed = (df['时间'] - df['时间'].min()).dt.total_seconds()
    df['elapsed'] = elapsed
    return df

def remove_worst_sensor_and_average(df, cols):
    g = df[cols].values
    group_mean = np.mean(g, axis=1)
    sensor_devs = []
    for i in range(len(cols)):
        dev = np.mean(np.abs(g[:, i] - group_mean))
        sensor_devs.append(dev)
    worst_sensor_idx = np.argmax(sensor_devs)
    worst_sensor = cols[worst_sensor_idx]
    remaining_cols = [c for i, c in enumerate(cols) if i != worst_sensor_idx]
    remaining_vals = np.delete(g, worst_sensor_idx, axis=1)
    raw_means = np.mean(remaining_vals, axis=1)
    return raw_means, worst_sensor, remaining_cols

def apply_ema(values, alpha):
    smoothed = [values[0]]
    for i in range(1, len(values)):
        smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
    return smoothed

def process_dataset(df):
    ga = df[['elapsed', 'T1']].rename(columns={'T1': 'mean'})
    
    raw_b, worst_b, remaining_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
    smooth_b = apply_ema(raw_b, EMA_ALPHA)
    gb = pd.DataFrame({'mean': smooth_b, 'elapsed': df['elapsed']})
    
    raw_c, worst_c, remaining_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
    smooth_c = apply_ema(raw_c, EMA_ALPHA)
    gc = pd.DataFrame({'mean': smooth_c, 'elapsed': df['elapsed']})
    
    summary = {
        'T1': {'mean': df['T1'].mean(), 'std': df['T1'].std(), 'min': df['T1'].min(),
               'max': df['T1'].max(), 'initial': df['T1'].iloc[0], 'final': df['T1'].iloc[-1]},
        'T2-T5': {'mean': gb['mean'].mean(), 'std': gb['mean'].std(),
                  'min': gb['mean'].min(), 'max': gb['mean'].max(),
                  'initial': gb['mean'].iloc[0], 'final': gb['mean'].iloc[-1]},
        'T6-T9': {'mean': gc['mean'].mean(), 'std': gc['mean'].std(),
                  'min': gc['mean'].min(), 'max': gc['mean'].max(),
                  'initial': gc['mean'].iloc[0], 'final': gc['mean'].iloc[-1]}
    }
    return ga, gb, gc, worst_b, remaining_b, worst_c, remaining_c, summary

df_10w = load_and_process('tpms_gyroid10w_20260730_193152.xlsx', is_csv=False)
df_20w = load_and_process('tpms_gyroid20w_20260731_195755.csv', is_csv=True)

ga_10, gb_10, gc_10, worst_b_10, remaining_b_10, worst_c_10, remaining_c_10, sum_10 = process_dataset(df_10w)
ga_20, gb_20, gc_20, worst_b_20, remaining_b_20, worst_c_20, remaining_c_20, sum_20 = process_dataset(df_20w)

print('=== 10W 数据 ===')
print(f'记录数: {len(df_10w)}, 时长: {df_10w["elapsed"].iloc[-1]:.0f}s ({df_10w["elapsed"].iloc[-1]/60:.1f}min)')
print(f'T2-T5: 去掉 {worst_b_10}, 使用 {remaining_b_10}')
print(f'T6-T9: 去掉 {worst_c_10}, 使用 {remaining_c_10}')

print('\n=== 20W 数据 ===')
print(f'记录数: {len(df_20w)}, 时长: {df_20w["elapsed"].iloc[-1]:.0f}s ({df_20w["elapsed"].iloc[-1]/60:.1f}min)')
print(f'T2-T5: 去掉 {worst_b_20}, 使用 {remaining_b_20}')
print(f'T6-T9: 去掉 {worst_c_20}, 使用 {remaining_c_20}')

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(ga_10['elapsed'], ga_10['mean'], color='red', linewidth=1.5, label='10W T1')
axes[0, 0].set_xlabel('时间 (秒)')
axes[0, 0].set_ylabel('温度 (°C)')
axes[0, 0].set_title('A组: T1 (10W)', fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(gb_10['elapsed'], gb_10['mean'], color='blue', linewidth=1.5, label=f'10W T2-T5 (EMA α={EMA_ALPHA})')
axes[0, 1].set_xlabel('时间 (秒)')
axes[0, 1].set_ylabel('温度 (°C)')
axes[0, 1].set_title('B组: T2-T5 (10W)', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(gc_10['elapsed'], gc_10['mean'], color='green', linewidth=1.5, label=f'10W T6-T9 (EMA α={EMA_ALPHA})')
axes[0, 2].set_xlabel('时间 (秒)')
axes[0, 2].set_ylabel('温度 (°C)')
axes[0, 2].set_title('C组: T6-T9 (10W)', fontweight='bold')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(ga_20['elapsed'], ga_20['mean'], color='darkred', linewidth=1.5, label='20W T1')
axes[1, 0].set_xlabel('时间 (秒)')
axes[1, 0].set_ylabel('温度 (°C)')
axes[1, 0].set_title('A组: T1 (20W)', fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(gb_20['elapsed'], gb_20['mean'], color='darkblue', linewidth=1.5, label=f'20W T2-T5 (EMA α={EMA_ALPHA})')
axes[1, 1].set_xlabel('时间 (秒)')
axes[1, 1].set_ylabel('温度 (°C)')
axes[1, 1].set_title('B组: T2-T5 (20W)', fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].plot(gc_20['elapsed'], gc_20['mean'], color='darkgreen', linewidth=1.5, label=f'20W T6-T9 (EMA α={EMA_ALPHA})')
axes[1, 2].set_xlabel('时间 (秒)')
axes[1, 2].set_ylabel('温度 (°C)')
axes[1, 2].set_title('C组: T6-T9 (20W)', fontweight='bold')
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temperature_analysis.png', dpi=300, bbox_inches='tight')
print('\n图表已保存: temperature_analysis.png')

fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
groups = ['T1', 'T2-T5', 'T6-T9']
x = np.arange(len(groups))
width = 0.35
bars1 = ax.bar(x - width/2, [sum_10[g]['final'] for g in groups], width, label='10W', color=['red','blue','green'], alpha=0.6)
bars2 = ax.bar(x + width/2, [sum_20[g]['final'] for g in groups], width, label='20W', color=['darkred','darkblue','darkgreen'], alpha=0.6)
ax.set_xlabel('分组')
ax.set_ylabel('最终温度 (°C)')
ax.set_title('10W vs 20W 各组最终温度对比', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(groups)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('temperature_comparison.png', dpi=300, bbox_inches='tight')
print('对比图已保存: temperature_comparison.png')

all_stats = []
for power, s in [('10W', sum_10), ('20W', sum_20)]:
    for g in groups:
        all_stats.append({'功率': power, '组别': g, **s[g]})
stats_df = pd.DataFrame(all_stats)
stats_df.to_csv('stats_gyroid10w_20w.csv', encoding='utf-8-sig', index=False)
print('\n统计数据已保存: stats_gyroid10w_20w.csv')

print('\n=== 10W 分组统计 ===')
for g in groups:
    s = sum_10[g]
    print(f'{g}: 初始={s["initial"]:.2f}°C, 最终={s["final"]:.2f}°C, 温升={s["final"]-s["initial"]:.2f}°C')

print('\n=== 20W 分组统计 ===')
for g in groups:
    s = sum_20[g]
    print(f'{g}: 初始={s["initial"]:.2f}°C, 最终={s["final"]:.2f}°C, 温升={s["final"]-s["initial"]:.2f}°C')

print('\n=== 10W vs 20W 对比 ===')
for g in groups:
    rise_10 = sum_10[g]['final'] - sum_10[g]['initial']
    rise_20 = sum_20[g]['final'] - sum_20[g]['initial']
    print(f'{g}: 10W温升={rise_10:.2f}°C, 20W温升={rise_20:.2f}°C, 比值={rise_20/rise_10:.2f}')
