import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df = load_and_process('temperature_record_20260802_203604.csv')

print('=== 数据概览 ===')
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

print(f'\n=== 离群传感器剔除 ===')
print(f'方法: 在整个时间序列上，找出与组均值平均偏差最大的传感器，在所有时间点都去掉它，剩余3个取均值')
print(f'B组 (T2-T5): 去掉 {worst_b}, 使用 {remaining_b}')
print(f'C组 (T6-T9): 去掉 {worst_c}, 使用 {remaining_c}')

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
for g in summary:
    s = summary[g]
    print(f'{g}: 初始={s["initial"]:.2f}°C, 最终={s["final"]:.2f}°C, 温升={s["final"]-s["initial"]:.2f}°C')

fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df['elapsed'], df['T1'], color='red', linewidth=2, label='T1 (A组)')
ax.plot(gb['elapsed'], gb['mean'], color='blue', linewidth=2, label=f'T2-T5 均值 (B组, EMA α={EMA_ALPHA})')
ax.plot(gc['elapsed'], gc['mean'], color='green', linewidth=2, label=f'T6-T9 均值 (C组, EMA α={EMA_ALPHA})')

ax.set_xlabel('时间 (秒)', fontsize=12)
ax.set_ylabel('温度 (°C)', fontsize=12)
ax.set_title('温度变化曲线 (三组对比)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

final_t1 = summary['T1']['final']
final_b = summary['T2-T5']['final']
final_c = summary['T6-T9']['final']
ax.annotate(f'T1: {final_t1:.1f}°C', xy=(df['elapsed'].iloc[-1], final_t1), 
            xytext=(10, 10), textcoords='offset points', fontsize=10, color='red')
ax.annotate(f'T2-T5: {final_b:.1f}°C', xy=(gb['elapsed'].iloc[-1], final_b), 
            xytext=(10, -15), textcoords='offset points', fontsize=10, color='blue')
ax.annotate(f'T6-T9: {final_c:.1f}°C', xy=(gc['elapsed'].iloc[-1], final_c), 
            xytext=(10, -15), textcoords='offset points', fontsize=10, color='green')

plt.tight_layout()
plt.savefig('analysis_new_data.png', dpi=300, bbox_inches='tight')
print(f'\n图表已保存: analysis_new_data.png')

stats_df = pd.DataFrame(summary).T
stats_df.to_csv('stats_new_data.csv', encoding='utf-8-sig')
print(f'统计数据已保存: stats_new_data.csv')
