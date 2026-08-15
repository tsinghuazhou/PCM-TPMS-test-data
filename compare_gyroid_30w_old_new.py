"""比较新旧30W Gyroid数据"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
new_data = pd.read_csv('temperature_record_20260808_203206.csv')
old_data = pd.read_csv('temperature_record_20260803_171111.csv')

# 处理时间列（旧数据列名可能是中文"时间"）
if 'time' in new_data.columns:
    new_data['time'] = pd.to_datetime(new_data['time'])
else:
    new_data['time'] = pd.to_datetime(new_data.iloc[:, 0])

if 'time' in old_data.columns:
    old_data['time'] = pd.to_datetime(old_data['time'])
else:
    # 旧数据第一列是"时间"
    old_data.rename(columns={old_data.columns[0]: 'time'}, inplace=True)
    old_data['time'] = pd.to_datetime(old_data['time'])

# 计算相对时间（分钟）
new_data['elapsed_min'] = (new_data['time'] - new_data['time'].iloc[0]).dt.total_seconds() / 60
old_data['elapsed_min'] = (old_data['time'] - old_data['time'].iloc[0]).dt.total_seconds() / 60

print("=" * 80)
print("新旧30W Gyroid数据对比")
print("=" * 80)
print(f"\n旧数据: temperature_record_20260803_171111.csv")
print(f"  时间范围: {old_data['time'].iloc[0]} 到 {old_data['time'].iloc[-1]}")
print(f"  总时长: {old_data['elapsed_min'].iloc[-1]:.2f} 分钟")
print(f"  数据点数: {len(old_data)}")

print(f"\n新数据: temperature_record_20260808_203206.csv")
print(f"  时间范围: {new_data['time'].iloc[0]} 到 {new_data['time'].iloc[-1]}")
print(f"  总时长: {new_data['elapsed_min'].iloc[-1]:.2f} 分钟")
print(f"  数据点数: {len(new_data)}")

# 计算统计量
def calc_stats(df, name):
    print(f"\n{name} 统计:")
    print(f"  T1最终温度: {df['T1'].iloc[-1]:.1f}°C")
    print(f"  T9最终温度: {df['T9'].iloc[-1]:.1f}°C")
    
    # 计算B组（T2/T3/T5，去掉T4）
    df['B_avg'] = df[['T2', 'T3', 'T5']].mean(axis=1)
    
    # 计算A-B和A-C梯度
    df['A-B'] = df['T1'] - df['B_avg']
    df['A-C'] = df['T1'] - df['T9']
    
    # 找到T1=42°C和T1=50°C时的梯度
    t1_42_idx = (df['T1'] - 42).abs().idxmin()
    t1_50_idx = (df['T1'] - 50).abs().idxmin()
    
    print(f"  T1=42°C时: A-B={df['A-B'].iloc[t1_42_idx]:.1f}°C, A-C={df['A-C'].iloc[t1_42_idx]:.1f}°C")
    print(f"  T1=50°C时: A-B={df['A-B'].iloc[t1_50_idx]:.1f}°C, A-C={df['A-C'].iloc[t1_50_idx]:.1f}°C")
    
    # 计算到达42°C的时间
    t1_42_time = df[df['T1'] >= 42]['elapsed_min'].iloc[0] if len(df[df['T1'] >= 42]) > 0 else np.nan
    t9_42_time = df[df['T9'] >= 42]['elapsed_min'].iloc[0] if len(df[df['T9'] >= 42]) > 0 else np.nan
    
    print(f"  T1到达42°C: {t1_42_time:.2f} min")
    print(f"  T9到达42°C: {t9_42_time:.2f} min")
    
    # 计算熔融时长（T1在42-52°C的时间）
    melting_duration = df[(df['T1'] >= 42) & (df['T1'] <= 52)]['elapsed_min'].iloc[-1] - df[(df['T1'] >= 42) & (df['T1'] <= 52)]['elapsed_min'].iloc[0] if len(df[(df['T1'] >= 42) & (df['T1'] <= 52)]) > 1 else 0
    print(f"  熔融时长(42-52°C): {melting_duration:.2f} min")
    
    return df

new_data = calc_stats(new_data, "新数据")
old_data = calc_stats(old_data, "旧数据")

# 绘制对比图
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1: T1温度曲线对比
ax1 = axes[0, 0]
ax1.plot(old_data['elapsed_min'], old_data['T1'], 'b-', label='旧数据 T1', linewidth=2)
ax1.plot(new_data['elapsed_min'], new_data['T1'], 'r-', label='新数据 T1', linewidth=2)
ax1.axhline(y=42, color='g', linestyle='--', label='熔点 42°C')
ax1.set_xlabel('时间 (min)')
ax1.set_ylabel('温度 (°C)')
ax1.set_title('T1 温度曲线对比')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 图2: T9温度曲线对比
ax2 = axes[0, 1]
ax2.plot(old_data['elapsed_min'], old_data['T9'], 'b-', label='旧数据 T9', linewidth=2)
ax2.plot(new_data['elapsed_min'], new_data['T9'], 'r-', label='新数据 T9', linewidth=2)
ax2.axhline(y=42, color='g', linestyle='--', label='熔点 42°C')
ax2.set_xlabel('时间 (min)')
ax2.set_ylabel('温度 (°C)')
ax2.set_title('T9 温度曲线对比')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 图3: A-B梯度对比
ax3 = axes[1, 0]
ax3.plot(old_data['elapsed_min'], old_data['A-B'], 'b-', label='旧数据 A-B', linewidth=2)
ax3.plot(new_data['elapsed_min'], new_data['A-B'], 'r-', label='新数据 A-B', linewidth=2)
ax3.set_xlabel('时间 (min)')
ax3.set_ylabel('A-B 梯度 (°C)')
ax3.set_title('A-B 梯度随时间变化')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 图4: A-C梯度对比
ax4 = axes[1, 1]
ax4.plot(old_data['elapsed_min'], old_data['A-C'], 'b-', label='旧数据 A-C', linewidth=2)
ax4.plot(new_data['elapsed_min'], new_data['A-C'], 'r-', label='新数据 A-C', linewidth=2)
ax4.set_xlabel('时间 (min)')
ax4.set_ylabel('A-C 梯度 (°C)')
ax4.set_title('A-C 梯度随时间变化')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/paper/figures/gyroid_30w_old_vs_new.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/gyroid_30w_old_vs_new.pdf', bbox_inches='tight')
print(f"\n对比图已保存: output/paper/figures/gyroid_30w_old_vs_new.png/pdf")
