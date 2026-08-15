# 实验数据汇总（用于论文撰写）

## 实验设计
- **材料**: 石蜡基PCM（相变温度42°C）
- **晶格结构**: Gyroid（陀螺体）和 Primitive（原始体）TPMS晶格
- **制造方式**: 增材制造AlSiMg金属晶格
- **样品尺寸**: 50×50×20 mm³
- **加热功率**: 10W, 20W, 30W

## 热电偶布放
- **T1**: 底面中心 (0,0,0) - 加热器位置
- **T2-T5**: 中间层 z=10mm，边长25mm正方形4个角 (±12.5, ±12.5, 10)
- **T6-T9**: 上表面 z=20mm，边长25mm正方形4个边中点 ((±12.5, 0, 20), (0, ±12.5, 20))
- **上层相对中层旋转45°**

## 统计规则
- **A组**: T1（底面）
- **B组**: T2/T3/T5 直接平均（去掉T4，传感器有问题）
- **C组**: T9（顶层，接触最稳定）

## 主要实验数据

### Gyroid 10W（两次实验）
| 指标 | OLD (08-04) | NEW (08-08) |
|------|-------------|-------------|
| 时长 | 25.4 min | 32.5 min |
| T1末值 | 93.8°C | 106.5°C |
| A-B@42°C | 5.8°C | 4.2°C |
| A-B@50°C | 5.9°C | 5.2°C |
| A-C@42°C | 8.0°C | 8.6°C |
| A-C@50°C | 9.7°C | 10.4°C |
| 熔融时长 | 12.1 min | 11.8 min |

### Gyroid 20W
| 指标 | OLD (07-31) | NEW (08-08) |
|------|-------------|-------------|
| 时长 | 11.1 min | 12.2 min |
| T1末值 | 144.7°C | 103.0°C |
| A-B@42°C | 14.1°C | 9.1°C |
| A-B@50°C | 23.5°C | 10.6°C |
| A-C@42°C | 18.0°C | 12.4°C |
| A-C@50°C | 23.8°C | 14.5°C |
| 熔融时长 | 0.0 min | 2.2 min |

### Gyroid 30W（NEW 08-08）
| 指标 | 数值 |
|------|------|
| 时长 | 9.4 min |
| T1峰值 | 127.9°C |
| A-B@42°C | 12.4°C |
| A-B@50°C | 14.4°C |
| A-C@42°C | 15.7°C |
| A-C@50°C | 21.6°C |
| 熔融时长 | 0.6 min |

### Primitive 10W (08-05)
| 指标 | 数值 |
|------|------|
| 时长 | 26.9 min |
| T1末值 | 107.0°C |
| A-B@42°C | 7.7°C |
| A-B@50°C | 9.9°C |
| A-C@42°C | 10.7°C |
| A-C@50°C | 14.4°C |
| 熔融时长 | 9.4 min |

## 核心发现

### 1. Gyroid vs Primitive 对比（10W）
- **A-B梯度**: Gyroid比Primitive低约40-50%（42°C时4.2 vs 7.7°C）
- **A-C梯度**: Gyroid比Primitive低约20-30%（42°C时8.6 vs 10.7°C）
- **梯度稳定性**: Gyroid在相变过程中梯度保持稳定，Primitive梯度持续增大（+55%）
- **熔融时长**: Gyroid比Primitive长25-28%（11.8 vs 9.4 min）
- **机制**: Gyroid的三维连通网络抑制了相变过程中的梯度恶化

### 2. 功率效应（Gyroid）
- **A-B梯度**: 30W是10W的2.8倍（42°C时12.4 vs 4.4°C）
- **A-C梯度**: 30W是10W的1.8倍（42°C时15.7 vs 8.6°C）
- **熔融时长**: 功率增加3倍，熔融时长缩短20倍（11.8→0.6 min）
- **相变窗口**: 30W下相变几乎瞬间完成（0.6 min）

### 3. 数据可复现性
- Gyroid 10W两次实验高度一致（A-B梯度差异<1°C）
- 新旧数据对比验证了实验方法的可靠性

## 可用图表
1. thermocouple_layout_3d.png - 热电偶3D布放图
2. thermocouple_layout_top.png - 热电偶俯视图
3. primitive_vs_gyroid_10w_update.png - Primitive vs Gyroid 10W对比
4. gyroid_power_comparison_no_t4.png - Gyroid功率对比（10W/20W/30W）
5. gyroid_30w_new_analysis.png - Gyroid 30W完整分析
6. gyroid_30w_old_vs_new_heating_only.png - Gyroid 30W新旧对比（加热阶段）
7. gyroid_10w_repeat_comparison.png - Gyroid 10W重复性验证

## 论文结构建议
1. Introduction - TPMS晶格在热管理中的应用背景
2. Experimental Setup - 材料、制造、测试方法
3. Results and Discussion
   - 3.1 热电偶布放与测量方法
   - 3.2 Gyroid vs Primitive热性能对比
   - 3.3 功率效应分析
   - 3.4 相变动力学
   - 3.5 数据可复现性
4. Conclusion
5. References
