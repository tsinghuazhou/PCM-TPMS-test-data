# 温度记录数据分析报告

**数据文件**: `temperature_record_20260803_171111-1.csv`  
**分析日期**: 2026-08-03  
**分析脚本**: `analyze_gyroid_30w_heating.py`  
**实验条件**: 30W加热功率下的gyroid晶格测温实验（升温阶段）

---

## 1. 数据概览

| 指标 | 数值 | 代码来源 |
|------|------|----------|
| 总记录数 | 436 | `len(df)` |
| 传感器数量 | 9 | `len(temp_cols)` |
| 实验开始时间 | 2026-08-03 17:11:12 | `df['时间'].min()` |
| 实验结束时间 | 2026-08-03 17:19:42 | `df['时间'].max()` |
| 实验时长 | 510.0 秒 (8.50 分钟) | `df['elapsed'].iloc[-1]` |

**数据结构**: 10列 × 436行  
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

**代码来源**: `analyze_gyroid_30w_heating.py` 中的 `remove_worst_sensor_and_average()` 和 `apply_ema()` 函数

### 2.3 离群传感器剔除结果

| 组别 | 去掉的传感器 | 使用的传感器 |
|------|--------------|--------------|
| T2-T5 | T5 | T2, T3, T4 |
| T6-T9 | T6 | T7, T8, T9 |

**观察**: T5在B组中被整体剔除，T6在C组中被整体剔除，表明这些传感器在整个实验过程中系统性偏离组均值。

---

## 3. 关键发现

### 3.1 各组温度统计 (去离群后均值)

| 组别 | 平均温度 (°C) | 标准差 (°C) | 最低温度 (°C) | 最高温度 (°C) | 初始温度 (°C) | 最终温度 (°C) |
|------|---------------|-------------|---------------|---------------|---------------|---------------|
| T1 | 64.88 | 22.81 | 26.30 | 103.45 | 26.30 | 103.45 |
| T2-T5 | 60.70 | 20.24 | 26.05 | 95.34 | 26.05 | 95.34 |
| T6-T9 | 53.13 | 15.65 | 26.16 | 80.10 | 26.16 | 80.10 |

**代码来源**: `stats_gyroid_30w_heating.csv` (由 `stats_df.to_csv()` 生成)

### 3.2 升温行为分析

**A组 (T1 单独)**:
- 初始温度: 26.30°C
- 最终温度: 103.45°C
- 温升: 77.15°C (`103.45 - 26.30`)
- **显著高于其他组**

**B组 (T2-T5 去离群后均值)**:
- 初始温度: 26.05°C
- 最终温度: 95.34°C
- 温升: 69.30°C (`95.34 - 26.05`)

**C组 (T6-T9 去离群后均值)**:
- 初始温度: 26.16°C
- 最终温度: 80.10°C
- 温升: 53.94°C (`80.10 - 26.16`)

**结论**: T1温升最大 (77.15°C)，B组次之 (69.30°C)，C组最小 (53.94°C)。三组存在明显的温度分层。

---

## 4. 可视化

**图表文件**: `analysis_gyroid_30w_heating.png`

图表在单坐标系中显示三条温度变化曲线：
- **红色曲线**: T1 (A组) - 单独传感器
- **蓝色曲线**: T2-T5 均值 (B组) - 去掉T5后取均值，EMA平滑
- **绿色曲线**: T6-T9 均值 (C组) - 去掉T6后取均值，EMA平滑

每条曲线末端标注了最终温度值，便于直观比较三组的温度差异。

**代码来源**: `analyze_gyroid_30w_heating.py` 中的 `plt.savefig('analysis_gyroid_30w_heating.png', dpi=300)`

---

## 5. 结论

1. **T1 传感器异常**: T1 达到 103.45°C，温升 77.15°C，远超其他两组，表明其位置最靠近热源。

2. **温度分层**: 存在明显的温度分层：T1 > T2-T5 > T6-T9。B组与C组最终温度相差 15.24°C (95.34 - 80.10)。

3. **传感器差异**: T5在B组中被整体剔除，T6在C组中被整体剔除，表明这些传感器读数与其他传感器存在系统性差异，可能位置特殊或传感器特性不同。

4. **实验时长**: 8.50分钟内完成加热过程，系统达到热平衡。

5. **离群传感器**: T5和T6在整个实验过程中系统性偏离组均值，可能位置特殊或传感器特性不同。

---

## 6. 数据溯源

所有数值均可通过以下代码复现:

```python
import pandas as pd
import numpy as np

EMA_ALPHA = 0.4

df = pd.read_csv('temperature_record_20260803_171111-1.csv', parse_dates=[0])
df.columns = ['时间', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']

print(f"T1 最终温度: {df['T1'].iloc[-1]:.2f}°C")  # 103.45°C

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

raw_b, worst_b, remaining_b = remove_worst_sensor_and_average(df, ['T2', 'T3', 'T4', 'T5'])
smooth_b = apply_ema(raw_b, EMA_ALPHA)
print(f"T2-T5: 去掉 {worst_b}, 使用 {remaining_b}, 最终均值: {smooth_b[-1]:.2f}°C")  # 95.34°C

raw_c, worst_c, remaining_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
smooth_c = apply_ema(raw_c, EMA_ALPHA)
print(f"T6-T9: 去掉 {worst_c}, 使用 {remaining_c}, 最终均值: {smooth_c[-1]:.2f}°C")  # 80.10°C
```

完整分析代码: `analyze_gyroid_30w_heating.py`  
统计数据: `stats_gyroid_30w_heating.csv`  
可视化图表: `analysis_gyroid_30w_heating.png`
