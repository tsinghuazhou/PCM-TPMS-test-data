import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

EMA_ALPHA = 0.4

def load_and_process(filepath):
    df = pd.read_csv(filepath, parse_dates=[0])
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

df = load_and_process('temperature_record_20260731_195755.csv')

print(f'=== 20W 数据概览 ===')
print(f'记录数: {len(df)}')
print(f'时长: {df["elapsed"].iloc[-1]:.0f}s ({df["elapsed"].iloc[-1]/60:.1f}min)')
print(f'开始时间: {df["时间"].min()}')
print(f'结束时间: {df["时间"].max()}')

ga = df[['elapsed', 'T1']].rename(columns={'T1': 'mean'})

raw_b, worst_b, remaining_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
smooth_b = apply_ema(raw_b, EMA_ALPHA)
gb = pd.DataFrame({'mean': smooth_b, 'elapsed': df['elapsed']})

raw_c, worst_c, remaining_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
smooth_c = apply_ema(raw_c, EMA_ALPHA)
gc = pd.DataFrame({'mean': smooth_c, 'elapsed': df['elapsed']})

print(f'\n=== 离群值剔除统计 ===')
print(f'方法: 在整个时间序列上，找出与组均值平均偏差最大的传感器，在所有时间点都去掉它，剩余3个取均值')
print(f'B组 (T2-T5): 去掉 {worst_b}, 使用 {remaining_b}')
print(f'C组 (T6-T9): 去掉 {worst_c}, 使用 {remaining_c}')

nan_b = gb['mean'].isnull().sum()
nan_c = gc['mean'].isnull().sum()
print(f'\n均值NaN数量: B组={nan_b}, C组={nan_c}')

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

print(f'\n=== 分组统计 (去离群后均值) ===')
for g in ['T1', 'T2-T5', 'T6-T9']:
    s = summary[g]
    print(f'{g}: 初始={s["initial"]:.2f}°C, 最终={s["final"]:.2f}°C, 温升={s["final"]-s["initial"]:.2f}°C')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0, 0].plot(df['elapsed'], df['T1'], color='red', linewidth=1.5, label='T1')
axes[0, 0].set_xlabel('时间 (秒)')
axes[0, 0].set_ylabel('温度 (°C)')
axes[0, 0].set_title('A组: T1 (单独)', fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(df['elapsed'], df['T2'], '--', color='gray', alpha=0.4, linewidth=0.8, label='T2-T5 原始')
axes[0, 1].plot(df['elapsed'], df['T3'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[0, 1].plot(df['elapsed'], df['T4'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[0, 1].plot(df['elapsed'], df['T5'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[0, 1].plot(gb['elapsed'], gb['mean'], color='blue', linewidth=2, label=f'T2-T5 均值 (EMA α={EMA_ALPHA})')
axes[0, 1].set_xlabel('时间 (秒)')
axes[0, 1].set_ylabel('温度 (°C)')
axes[0, 1].set_title('B组: T2-T5 (去离群后均值)', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(df['elapsed'], df['T6'], '--', color='gray', alpha=0.4, linewidth=0.8, label='T6-T9 原始')
axes[1, 0].plot(df['elapsed'], df['T7'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[1, 0].plot(df['elapsed'], df['T8'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[1, 0].plot(df['elapsed'], df['T9'], '--', color='gray', alpha=0.4, linewidth=0.8)
axes[1, 0].plot(gc['elapsed'], gc['mean'], color='green', linewidth=2, label=f'T6-T9 均值 (EMA α={EMA_ALPHA})')
axes[1, 0].set_xlabel('时间 (秒)')
axes[1, 0].set_ylabel('温度 (°C)')
axes[1, 0].set_title('C组: T6-T9 (去离群后均值)', fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

groups = ['T1', 'T2-T5', 'T6-T9']
final_vals = [summary[g]['final'] for g in groups]
colors = ['red', 'blue', 'green']
axes[1, 1].bar(groups, final_vals, color=colors, alpha=0.7)
axes[1, 1].set_xlabel('分组')
axes[1, 1].set_ylabel('最终温度 (°C)')
axes[1, 1].set_title('各组最终温度对比 (去离群后均值)', fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(final_vals):
    axes[1, 1].text(i, v + 1, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('analysis_20w.png', dpi=300, bbox_inches='tight')
print(f'\n图表已保存: analysis_20w.png')

stats_df = pd.DataFrame(summary).T
stats_df.to_csv('stats_20w.csv', encoding='utf-8-sig')
print(f'统计数据已保存: stats_20w.csv')
