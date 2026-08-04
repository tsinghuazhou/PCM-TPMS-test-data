# 冷却过程温度数据分析报告

**数据文件**: `temperature_record_20260802_204933.csv`  
**分析日期**: 2026-08-02  
**分析脚本**: `analyze_cooling_data.py`  
**实验条件**: 20W加热功率下的gyroid晶格测温实验（冷却阶段）

---

## 1. 数据概览

| 指标 | 数值 | 代码来源 |
|------|------|----------|
| 总记录数 | 547 | `len(df)` |
| 传感器数量 | 9 | `len(temp_cols)` |
| 实验开始时间 | 2026-08-02 20:49:33 | `df['时间'].min()` |
| 实验结束时间 | 2026-08-02 21:01:06 | `df['时间'].max()` |
| 实验时长 | 693.0 秒 (11.6 分钟) | `df['elapsed'].iloc[-1]` |

**数据结构**: 10列 × 547行  
- 第1列: 时间戳 (datetime64)
- 第2-10列: T1-T9 温度传感器读数 (float64, 单位: °C)

**实验类型**: 冷却过程（温度从高到低）

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

**代码来源**: `analyze_cooling_data.py` 中的 `remove_worst_sensor_and_average()` 和 `apply_ema()` 函数

### 2.3 离群传感器剔除结果

| 组别 | 去掉的传感器 | 使用的传感器 |
|------|--------------|--------------|
| T2-T5 | T3 | T2, T4, T5 |
| T6-T9 | T6 | T7, T8, T9 |

**观察**: T3在B组中被整体剔除，T6在C组中被整体剔除，表明这些传感器在整个实验过程中系统性偏离组均值。

---

## 3. 关键发现

### 3.1 各组温度统计 (去离群后均值)

| 组别 | 平均温度 (°C) | 标准差 (°C) | 最低温度 (°C) | 最高温度 (°C) | 初始温度 (°C) | 最终温度 (°C) |
|------|---------------|-------------|---------------|---------------|---------------|---------------|
| T1 | 80.41 | 5.75 | 70.81 | 90.00 | 90.00 | 70.81 |
| T2-T5 | 80.83 | 5.64 | 71.27 | 90.39 | 90.39 | 71.27 |
| T6-T9 | 72.31 | 4.62 | 64.52 | 80.10 | 80.10 | 64.52 |

**代码来源**: `stats_cooling_data.csv` (由 `stats_df.to_csv()` 生成)

### 3.2 降温行为分析

**A组 (T1 单独)**:
- 初始温度: 90.00°C
- 最终温度: 70.81°C
- 降温: -19.19°C (`70.81 - 90.00`)

**B组 (T2-T5 去离群后均值)**:
- 初始温度: 90.39°C
- 最终温度: 71.27°C
- 降温: -19.12°C (`71.27 - 90.39`)

**C组 (T6-T9 去离群后均值)**:
- 初始温度: 80.10°C
- 最终温度: 64.52°C
- 降温: -15.58°C (`64.52 - 80.10`)

**结论**: T1和T2-T5的降温幅度相近（约19°C），T6-T9降温较少（约15.6°C）。三组存在明显的温度分层。

---

## 4. 可视化

**图表文件**: `analysis_cooling_data.png`

图表在单坐标系中显示三条温度变化曲线：
- **红色曲线**: T1 (A组) - 单独传感器
- **蓝色曲线**: T2-T5 均值 (B组) - 去掉T3后取均值，EMA平滑
- **绿色曲线**: T6-T9 均值 (C组) - 去掉T6后取均值，EMA平滑

每条曲线末端标注了最终温度值，便于直观比较三组的温度差异。

**代码来源**: `analyze_cooling_data.py` 中的 `plt.savefig('analysis_cooling_data.png', dpi=300)`

---

## 5. 结论

1. **冷却过程**: 这是一个从高温到低温的冷却过程，持续约11.6分钟。

2. **温度分层**: 存在明显的温度分层：T2-T5 > T1 > T6-T9。初始时T2-T5温度最高（90.39°C），T6-T9温度最低（80.10°C）。

3. **降温幅度**: T1和T2-T5的降温幅度相近（约19°C），T6-T9降温较少（约15.6°C）。

4. **传感器差异**: T3和T6在整个实验过程中系统性偏离组均值，可能位置特殊或传感器特性不同。

5. **离群传感器**: T3在B组中被整体剔除，T6在C组中被整体剔除，表明这些传感器读数与其他传感器存在系统性差异。

---

## 6. 数据溯源

所有数值均可通过以下代码复现:

```python
import pandas as pd
import numpy as np

EMA_ALPHA = 0.4

df = pd.read_csv('temperature_record_20260802_204933.csv', parse_dates=[0])
df.columns = ['时间', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']

print(f"T1 最终温度: {df['T1'].iloc[-1]:.2f}°C")  # 70.81°C

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
print(f"T2-T5: 去掉 {worst_b}, 使用 {remaining_b}, 最终均值: {smooth_b[-1]:.2f}°C")  # 71.27°C

raw_c, worst_c, remaining_c = remove_worst_sensor_and_average(df, ['T6', 'T7', 'T8', 'T9'])
smooth_c = apply_ema(raw_c, EMA_ALPHA)
print(f"T6-T9: 去掉 {worst_c}, 使用 {remaining_c}, 最终均值: {smooth_c[-1]:.2f}°C")  # 64.52°C
```

完整分析代码: `analyze_cooling_data.py`  
统计数据: `stats_cooling_data.csv`  
可视化图表: `analysis_cooling_data.png`
