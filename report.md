# 温度记录数据分析报告

**数据文件**: 
- 10W: `temperature_record_20260730_193152.xlsx`
- 20W: `temperature_record_20260731_195755.csv`

**分析日期**: 2026-07-30  
**分析脚本**: `analyze_temperature.py`

---

## 1. 数据概览

### 10W 加热功率

| 指标 | 数值 | 代码来源 |
|------|------|----------|
| 总记录数 | 1160 | `len(df_10w)` |
| 传感器数量 | 9 | `len(temp_cols)` |
| 实验开始时间 | 2026-07-30 19:31:53 | `df_10w['时间'].min()` |
| 实验结束时间 | 2026-07-30 19:53:53 | `df_10w['时间'].max()` |
| 实验时长 | 1320.0 秒 (22.0 分钟) | `df_10w['elapsed'].iloc[-1]` |

### 20W 加热功率

| 指标 | 数值 | 代码来源 |
|------|------|----------|
| 总记录数 | 603 | `len(df_20w)` |
| 传感器数量 | 9 | `len(temp_cols)` |
| 实验开始时间 | 2026-07-31 19:57:55 | `df_20w['时间'].min()` |
| 实验结束时间 | 2026-07-31 20:09:02 | `df_20w['时间'].max()` |
| 实验时长 | 667.0 秒 (11.1 分钟) | `df_20w['elapsed'].iloc[-1]` |

**数据结构**: 10列 × 1160行 (10W) / 603行 (20W)  
- 第1列: 时间戳 (datetime64)
- 第2-10列: T1-T9 温度传感器读数 (float64, 单位: °C)

---

## 2. 数据分组与离群值处理

### 2.1 分组方案

| 组别 | 传感器 | 处理方式 |
|------|--------|----------|
| A组 | T1 | 单独分析 |
| B组 | T2, T3, T4, T5 | 去离群值后取均值 |
| C组 | T6, T7, T8, T9 | 去离群值后取均值 |

### 2.2 离群值剔除方法

**方法**: 两个维度的数据处理：

1. **空间维度（整体去离群传感器）**: 在整个时间序列上，计算每个传感器与组均值的平均偏差，找出偏差最大的传感器，在所有时间点都去掉它，剩余3个传感器取均值。

2. **时间维度（EMA平滑）**: 对均值序列应用指数移动平均（Exponential Moving Average）：
   - 公式：`smoothed[t] = α × raw[t] + (1-α) × smoothed[t-1]`
   - 参数：α = 0.4（时间常数约2.5秒）
   - 作用：抑制高频波动，保持温度变化的趋势特征

**代码来源**: `analyze_temperature.py` 中的 `remove_worst_sensor_and_average()` 和 `apply_ema()` 函数

### 2.3 离群传感器剔除结果

**10W 数据**:
| 组别 | 去掉的传感器 | 使用的传感器 |
|------|--------------|--------------|
| T2-T5 | T2 | T3, T4, T5 |
| T6-T9 | T8 | T6, T7, T9 |

**20W 数据**:
| 组别 | 去掉的传感器 | 使用的传感器 |
|------|--------------|--------------|
| T2-T5 | T4 | T2, T3, T5 |
| T6-T9 | T9 | T6, T7, T8 |

**观察**: 10W数据中T2和T8被剔除，20W数据中T4和T9被剔除，表明这些传感器在整个实验过程中系统性偏离组均值。

---

## 3. 关键发现

### 3.1 各组温度统计 (去离群后均值)

#### 10W 加热功率

| 组别 | 平均温度 (°C) | 标准差 (°C) | 最低温度 (°C) | 最高温度 (°C) | 初始温度 (°C) | 最终温度 (°C) |
|------|---------------|-------------|---------------|---------------|---------------|---------------|
| T1 | 78.64 | 17.55 | 28.53 | 109.41 | 28.63 | 109.40 |
| T2-T5 | 46.38 | 13.08 | 28.86 | 76.28 | 28.86 | 76.28 |
| T6-T9 | 44.49 | 12.04 | 28.47 | 71.53 | 28.47 | 71.53 |

#### 20W 加热功率

| 组别 | 平均温度 (°C) | 标准差 (°C) | 最低温度 (°C) | 最高温度 (°C) | 初始温度 (°C) | 最终温度 (°C) |
|------|---------------|-------------|---------------|---------------|---------------|---------------|
| T1 | 109.57 | 19.07 | 25.16 | 144.71 | 25.16 | 144.71 |
| T2-T5 | 46.20 | 14.50 | 25.43 | 80.77 | 25.43 | 80.77 |
| T6-T9 | 45.45 | 13.53 | 25.49 | 78.72 | 25.49 | 78.72 |

**代码来源**: `temperature_stats.csv` (由 `stats_df.to_csv()` 生成)

### 3.2 升温行为分析

#### 10W 加热功率

**A组 (T1 单独)**:
- 初始温度: 28.63°C
- 最终温度: 109.40°C
- 温升: 80.77°C (`109.40 - 28.63`)
- **显著高于其他组**

**B组 (T2-T5 去离群后均值)**:
- 初始温度: 28.86°C
- 最终温度: 76.28°C
- 温升: 47.42°C (`76.28 - 28.86`)

**C组 (T6-T9 去离群后均值)**:
- 初始温度: 28.47°C
- 最终温度: 71.53°C
- 温升: 43.07°C (`71.53 - 28.47`)

#### 20W 加热功率

**A组 (T1 单独)**:
- 初始温度: 25.16°C
- 最终温度: 144.71°C
- 温升: 119.55°C (`144.71 - 25.16`)
- **显著高于其他组**

**B组 (T2-T5 去离群后均值)**:
- 初始温度: 25.43°C
- 最终温度: 80.77°C
- 温升: 55.34°C (`80.77 - 25.43`)

**C组 (T6-T9 去离群后均值)**:
- 初始温度: 25.49°C
- 最终温度: 78.72°C
- 温升: 53.24°C (`78.72 - 25.49`)

### 3.3 10W vs 20W 对比

| 组别 | 10W温升 (°C) | 20W温升 (°C) | 20W/10W 比值 |
|------|--------------|--------------|--------------|
| T1 | 80.77 | 119.55 | 1.48 |
| T2-T5 | 47.42 | 55.34 | 1.17 |
| T6-T9 | 43.06 | 53.24 | 1.24 |

**结论**: 
- 20W功率下，各组温升均高于10W，但增幅不同
- T1温升增加48% (1.48倍)，T2-T5增加19% (1.19倍)，T6-T9增加24% (1.24倍)
- T1对功率变化最敏感，表明其位置最靠近热源
- 20W实验时长仅11.1分钟，是10W的一半，但温升更大

---

## 4. 可视化

### 4.1 分组温度变化图

**图表文件**: `temperature_analysis.png`

图表包含6个子图 (2行×3列):
- **第一行 (10W)**: A组T1、B组T2-T5均值、C组T6-T9均值
- **第二行 (20W)**: A组T1、B组T2-T5均值、C组T6-T9均值

**代码来源**: `analyze_temperature.py` 中的 `plt.savefig('temperature_analysis.png', dpi=300)`

### 4.2 功率对比图

**图表文件**: `temperature_comparison.png`

柱状图对比10W和20W下各组的最终温度。

**代码来源**: `analyze_temperature.py` 中的 `plt.savefig('temperature_comparison.png', dpi=300)`

---

## 5. 结论

1. **T1 传感器异常**: 两种功率下，T1均达到最高温度 (10W: 109.40°C, 20W: 144.71°C)，温升远超其他两组，表明其位置最靠近热源。

2. **温度分层**: 两种功率下均存在明显的温度分层：T1 > T2-T5 > T6-T9。

3. **功率影响**: 20W功率下，各组温升均高于10W，但增幅不同：
   - T1温升增加48% (80.77°C → 119.55°C)
   - T2-T5温升增加17% (47.42°C → 55.34°C)
   - T6-T9温升增加24% (43.06°C → 53.24°C)
   - T1对功率变化最敏感。

4. **实验时长**: 20W实验时长仅11.1分钟，是10W (22.0分钟) 的一半，但温升更大，表明加热效率更高。

5. **离群传感器**: 10W数据中T2和T8被整体剔除，20W数据中T4和T9被整体剔除，表明这些传感器在整个实验过程中系统性偏离组均值，可能位置特殊或传感器特性不同。

---

## 6. 数据溯源

所有数值均可通过以下代码复现:

```python
import pandas as pd
import numpy as np

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

# 加载数据
df_10w = load_and_process('temperature_record_20260730_193152.xlsx', is_csv=False)
df_20w = load_and_process('temperature_record_20260731_195755.csv', is_csv=True)

# 处理各组
for name, df in [('10W', df_10w), ('20W', df_20w)]:
    print(f'\n=== {name} ===')
    print(f"T1 最终温度: {df['T1'].iloc[-1]:.2f}°C")
    
    raw_b, worst_b, remaining_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
    smooth_b = apply_ema(raw_b, EMA_ALPHA)
    print(f"T2-T5: 去掉 {worst_b}, 使用 {remaining_b}, 最终均值: {smooth_b[-1]:.2f}°C")
    
    raw_c, worst_c, remaining_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
    smooth_c = apply_ema(raw_c, EMA_ALPHA)
    print(f"T6-T9: 去掉 {worst_c}, 使用 {remaining_c}, 最终均值: {smooth_c[-1]:.2f}°C")
```

完整分析代码: `analyze_temperature.py`  
统计数据: `temperature_stats.csv`  
可视化图表: `temperature_analysis.png`, `temperature_comparison.png`
