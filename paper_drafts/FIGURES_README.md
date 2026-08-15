# 论文图表系统说明

## 图表清单

### Fig. 1 - TPMS结构示意图
- **文件**: `tpms_structures.drawio`
- **导出方式**: 使用draw.io打开，导出为PNG (300 DPI) 或 PDF
- **内容**: Gyroid、IWP、Primitive三种TPMS拓扑结构的三维示意图
- **用途**: Introduction部分，介绍三种TPMS结构

### Fig. 2 - 实验装置示意图
- **文件**: `experimental_setup.drawio`
- **导出方式**: 使用draw.io打开，导出为PNG (300 DPI) 或 PDF
- **内容**: 实验装置 schematic，包括：
  - TPMS晶格试样 (50×50×20 mm³)
  - 底部Kapton加热器
  - 9个热电偶的三层布置
  - 隔热箱
  - 数据采集系统
- **用途**: Experimental Setup部分

### Fig. 3 - 三种TPMS结构综合对比
- **文件**: `tpms_comprehensive_comparison.png/pdf`
- **已生成**: 是
- **内容**: 3×3网格图，展示三种结构在10W/20W/30W下的：
  - 熔融时长
  - A-B梯度@42°C
  - A-B梯度膨胀率
  - T1达42°C时间
  - T9达42°C时间
  - A-B梯度@55°C
- **用途**: Results and Discussion 3.1节

### Fig. 4 - 温度曲线对比
- **文件**: `temperature_curves.png/pdf`
- **已生成**: 是
- **内容**: 3×3子图，展示三种结构在10W/20W/30W下的温度-时间曲线
  - T1 (加热器)
  - T_B (中间层平均)
  - T_C (顶层)
  - 42°C水平参考线（PCM熔点）
- **用途**: Results and Discussion 3.2节

### Fig. 5 - 功率敏感性分析
- **文件**: `power_sensitivity.png/pdf`
- **已生成**: 是
- **内容**: 双面板柱状图
  - Panel A: 熔融时长缩减倍数 (10W→20W→30W)
  - Panel B: A-B梯度增大倍数 (10W→20W→30W)
- **关键数据**:
  - Gyroid: 19.1× / 2.8×
  - IWP: 30.8× / 2.4×
  - Primitive: 29.2× / 2.2×
- **用途**: Results and Discussion 3.4节

### Fig. 6 - 性能排名反转
- **文件**: `performance_ranking.png/pdf`
- **已生成**: 是
- **内容**: 双面板图
  - Panel A: 熔融时长对比，标注排名反转
  - Panel B: A-B梯度@42°C，标注改善百分比
- **关键发现**: 10W时IWP > Gyroid，20W/30W时Gyroid > IWP
- **用途**: Results and Discussion 3.3节

## 导出draw.io文件为PNG/PDF

### 方法1: 使用draw.io桌面应用
1. 下载并安装 draw.io: https://github.com/jgraph/drawio-desktop/releases
2. 打开 `.drawio` 文件
3. File → Export as → PNG (选择 300 DPI) 或 PDF
4. 保存到 `output/paper/figures/` 目录

### 方法2: 使用在线draw.io
1. 访问 https://app.diagrams.net/
2. File → Open from → Device (上传 `.drawio` 文件)
3. File → Export as → PNG (选择 300 DPI) 或 PDF
4. 下载并保存到 `output/paper/figures/` 目录

### 方法3: 使用VS Code扩展
1. 安装 "Draw.io Integration" 扩展
2. 双击 `.drawio` 文件打开编辑
3. 右键 → Export as PNG/PDF

## 论文版本

- **v3**: 纯文本论文（无图表引用）
- **v4**: 完整论文（包含图表引用和图注）
  - 英文版: `paper_drafts/paper_v4_en.md`
  - 中文版: `paper_drafts/paper_v4_zh.md` (待更新)

## 脚本文件

所有绘图脚本保存在 `scripts/` 目录：
- `plot_temperature_curves.py` - 生成Fig. 4
- `plot_power_sensitivity.py` - 生成Fig. 5
- `plot_performance_ranking.py` - 生成Fig. 6
- `compare_all_structures.py` - 生成Fig. 3

## 数据文件

- `output/paper/data/tpms_comprehensive_comparison.csv` - 所有实验数据汇总
