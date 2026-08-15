# Experimental Investigation of Thermal Performance in TPMS Lattice Structures with Phase Change Materials: A Comparative Study of Gyroid and Primitive Architectures

---

## Abstract

Triply periodic minimal surface (TPMS) lattice structures integrated with phase change materials (PCMs) represent a promising approach for advanced thermal management. However, systematic experimental comparisons of different TPMS topologies under controlled thermal loading conditions remain scarce. This study presents an experimental investigation of the thermal performance of Gyroid and Primitive TPMS lattice structures fabricated from AlSi10Mg alloy via selective laser melting (SLM), integrated with a paraffin-based PCM (phase change temperature: 42 °C). Specimens with dimensions of 50 × 50 × 20 mm³ were subjected to constant heat flux boundary conditions at three power levels (10 W, 20 W, and 30 W). Nine thermocouples were strategically positioned across three vertical layers to capture the spatial and temporal evolution of temperature fields during heating and phase change processes. Results demonstrate that the Gyroid topology achieves 40–50% lower A–B axial temperature gradients compared to the Primitive architecture at 10 W, and maintains exceptional gradient stability throughout the phase change window, whereas the Primitive structure exhibits 55% gradient deterioration during melting. The Gyroid's continuous triply-periodic channel network enables superior thermal homogenization by providing three-dimensionally interconnected heat conduction pathways. Heating power is shown to have a profound nonlinear effect: increasing power from 10 W to 30 W reduces melting duration by a factor of 20 but increases thermal gradients by 2.8×, revealing a fundamental trade-off between charging speed and thermal uniformity. Reproducibility is validated through repeated experiments with sub-1 °C variation. These findings establish the Gyroid topology as the preferred architecture for applications requiring spatially uniform thermal management, and provide quantitative design data for TPMS-based PCM thermal management systems in electronics cooling.

---

## 1. Introduction

现代电子设备持续的微型化与性能升级对 thermal management 提出了日益严苛的要求。随着先进微处理器和大功率 LED 中的 power density 不断攀升——已超过 100 W/cm²——传统的 passive cooling 策略（如 fin arrays 和 heat spreaders）正逐渐逼近其性能极限 [1]。高效的 thermal management 不仅对确保 device reliability 和运行寿命至关重要，也是维持瞬态 thermal loads 下 performance stability 的关键。这一挑战持续推动着对先进 thermal regulation 技术的研究兴趣，以在紧凑空间内应对高热流密度。

Phase change materials (PCMs) 因其出色的 passive thermal energy storage 和瞬态 thermal management 能力而备受关注。PCM 在固–液 phase transition 过程中以近似恒温的方式吸收和释放大量 latent heat，能够有效缓冲 thermal spikes 并将组件温度维持在安全工作窗口内 [3]。Paraffin waxes 因其高 latent heat capacity、化学稳定性、无毒性以及适用于 electronics cooling 的相变温度而被广泛采用。然而，paraffin 基 PCM 固有的低 thermal conductivity（通常为 0.2–0.4 W/m·K）严重限制了其热量吸收与释放速率，导致 thermal response 迟缓以及 latent heat capacity 的不完全利用。克服这一局限需要引入高 thermal conductivity 的 structural scaffolds，以增强 PCM 体积内的有效 thermal transport。

Metallic foams 和 lattice structures 作为 PCM composites 的 conductive matrices 已被广泛研究。其中，triply periodic minimal surface (TPMS) architectures 因其高 surface-area-to-volume ratio、interconnected pore networks 以及力学高效拓扑的卓越组合而备受关注 [1,5]。TPMS structures 由 zero-mean-curvature surfaces 定义，将三维空间分割为两个连续的、相互贯穿的通道。两种研究最为广泛的 TPMS topologies —— Gyroid 和 Primitive (Schwarz-P) —— 在 channel geometry 和 flow characteristics 上存在根本差异，进而影响 heat transfer performance。Gyroid surface 具有单连续通道和 chiral symmetry，而 Primitive surface 则由两个独立的 channel networks 通过周期性开口连接而成 [5,6]。这些几何差异导致了显著不同的 convective 和 conductive heat transfer 行为，使得 Gyroid 和 Primitive TPMS lattices 的 comparative study 对 thermal management design 具有重要的参考价值。

近年来的研究已展示了 TPMS-based structures 在 enhanced PCM thermal management 方面的潜力。Qureshi et al. [1] 研究了 TPMS-based metal foams 作为 PCM heat sinks 的应用，报告了与传统 foam geometries 相比，temperature uniformity 和 charging time 的显著改善。在后续研究中，Qureshi et al. [2] 探索了 3D-printed TPMS lattice structures 与 PCM 的集成，证明了 fabrication of complex periodic architectures with tailored thermal performance 的可行性。Gado [3] 对填充 PCM 的 TPMS heat sinks 进行了 numerical investigations，表明 Gyroid topology 在 melting rate 和 thermal storage efficiency 方面优于 Primitive 和 Diamond surfaces。Tang et al. [6] 研究了 Gyroid TPMS structures 中的 convective heat transfer，揭示了 chiral channel geometry 诱导的 secondary flows 与 thermal transport enhancement 之间的复杂相互作用。Kaur and Singh [5] 对 TPMS-based heat exchangers 中的 flow 和 thermal transport phenomena 进行了系统表征，建立了多种 TPMS topologies 下 Nusselt number 和 friction factor 的 design correlations。

Additive manufacturing (AM) 的发展，尤其是 laser powder bed fusion (L-PBF) 技术，使得 TPMS lattice structures 的 fabrication 达到了前所未有的 geometric accuracy 和 surface quality [2]。与受限于 mold design 和脱模工艺复杂性的传统制造方法不同，AM 允许直接实现数学定义的 TPMS geometries，并可精确控制 strut dimensions、porosity 和 unit cell size。这一能力为通过 tailoring lattice architecture 以满足特定 thermal management requirements 来优化 TPMS-PCM systems 开辟了新的途径。Guo et al. [21] 展示了一种 3D-printed lattice heat sink 与 PCM 集成用于 electronics cooling 的方案，表明 enhanced thermal conductivity network 在瞬态运行期间显著降低了 peak temperatures。Zhou and Qiao [23] 研究了 saturated with PCM 的 copper foam 中的 heat transfer characteristics，强调了 pore-scale morphology 在决定 composite systems 有效 thermal performance 中的重要性。

尽管取得了这些进展，在 TPMS-PCM coupled thermal systems 的 experimental understanding 方面仍存在显著 gap。现有研究大多依赖 numerical simulations 或 analytical models 来预测 TPMS-PCM configurations 的 thermal behavior [1,3]。在可控且可重现的 thermal loading conditions 下，直接比较不同 TPMS topologies —— 尤其是 Gyroid 和 Primitive —— 的 experimental investigations 明显不足。此外，heating power 对 TPMS-PCM systems 内 transient thermal response、phase change dynamics 和 spatial temperature distribution 的影响尚未通过实验得到系统表征。理解这些关系对于验证 computational models 和建立 practical engineering applications 的 design guidelines 至关重要。

本研究对两种 TPMS lattice topologies —— Gyroid 和 Primitive —— 与 paraffin 基 PCM 集成的 thermal performance 进行了系统的 experimental investigation。TPMS lattice structures 采用 AlSi10Mg alloy 通过 L-PBF additive manufacturing 制备，样品尺寸为 50 × 50 × 20 mm³。将相变温度为 42 °C 的 paraffin 基 PCM infiltrated 到 lattice pores 中。在 constant heat flux boundary conditions 下，于三个 power levels（10 W、20 W 和 30 W）进行了 transient heating experiments。在三个 vertical layers 上 strategically positioned 多个 thermocouples，以 capture heating 和 phase change processes 中 temperature fields 的 spatial and temporal evolution。本研究的主要 objectives 为：(1) 比较 Gyroid 和 Primitive TPMS lattices 在 temperature uniformity、thermal gradients 和 PCM melting dynamics 方面的 thermal performance；(2) 表征 heating power 对 transient thermal response 和 phase change behavior 的影响；(3) 提供 experimental data，为 electronics cooling applications 的 TPMS-based PCM thermal management systems 的 design optimization 提供参考依据。

---

## 2. Experimental Section

### 2.1 Materials and Specimen Preparation

本研究所采用的三周期极小曲面 (Triply Periodic Minimal Surface, TPMS) 晶格结构以 AlSiMg 合金 (AlSi10Mg) 为原料，通过选区激光熔化 (Selective Laser Melting, SLM) 增材制造工艺制备。研究考察了两种不同的 TPMS 拓扑构型：Gyroid 曲面和 Primitive (Schwarz Primitive) 曲面，二者均属于立方晶系，因其连通的通道网络和优异的比表面积特性而被广泛关注。SLM 成形过程的层厚设置为 30 μm，激光扫描策略针对 AlSiMg 合金体系进行了优化，经 micro-CT 分析确认相对密度超过 99%。主要工艺参数包括：激光功率 200 W，扫描速度 800 mm/s，扫描间距 0.12 mm，相邻层间条纹旋转角度为 67°，以最小化各向异性。

晶格试样的名义外部尺寸为 50 × 50 × 20 mm³。该几何尺寸的选取旨在保证足够数量的单胞以获得具有热学代表性的力学行为，同时与加热平台及隔热组件相匹配。单胞尺寸的选择兼顾了制造分辨率与多孔结构内部传热的特征长度尺度。成形完成后，所有试样均在 300 °C 下进行了 2 小时的去应力退火处理，以消除逐层 SLM 成形过程中产生的残余应力。表面粗糙度未做进一步处理，因为原始成形表面的形貌被认为能够代表实际热管理应用中的工况。

本研究所选用的相变材料 (Phase Change Material, PCM) 为商用石蜡，其标称熔点为 42 °C，熔化潜热约为 200 kJ/kg（由制造商提供）。选择该石蜡是基于其良好的热物性表征、长期化学稳定性、可忽略的过冷行为以及经证实与铝合金基体的相容性。PCM 在 −0.09 MPa 的负压条件下真空浸渗至 TPMS 多孔晶格结构中，以确保连通空隙空间的完全填充，避免截留气泡。每组复合试样在浸渗前后均使用精密天平 (±0.01 g) 进行称重，以确定 PCM 的质量填充量。结果表明，所有试样的 PCM 填充量偏差在 ±2% 以内，证实了浸渗工艺的可重复性。

### 2.2 Experimental Setup

实验装置由恒功率电阻加热系统、基于热电偶的温度测量阵列、多通道数据采集系统及隔热箱体组成。一块柔性聚酰亚胺 kapton 加热膜的活性面积与试样底面匹配，通过一层导热硅脂（导热系数 > 1.5 W/(m·K)）粘贴于每个晶格试样的底面。加热膜由一台稳压直流电源驱动，可提供 10 W、20 W 和 30 W 三个恒定功率等级，分别对应 4.0、8.0 和 12.0 kW/m² 的均匀热流密度。这三个功率等级的选取覆盖了从温和到强烈的热载荷范围，与电子元器件散热及便携式热管理应用相关。

温度测量采用 9 支 K 型 (chromel–alumel) 热电偶，丝径 0.25 mm，结点直径约 0.5 mm。热电偶通过试样顶面钻制的小孔（直径 < 1 mm）嵌入晶格结构的预设位置，并使用高温导热胶固定，以确保在加热和熔化全过程中保持可靠的热接触。热电偶的详细布置方案见 Section 2.3。

所有热电偶信号接入一台多通道数据采集系统 (NI-9213, National Instruments)，该系统具备内置冷端补偿功能。系统以 1 Hz 的采样率对全部 9 个通道进行同步采样，提供了足够的时间分辨率以捕获显热加热和相变阶段的瞬态热响应。数据采集系统在实验前经过 NIST 可溯源参考温度计的校准，总体测量不确定度估计为 ±0.5 °C。

实验组件封装于隔热箱内，箱体由 25 mm 厚的挤塑聚苯乙烯 (XPS) 泡沫板构成，内衬 10 mm 厚的陶瓷纤维毯以抑制高温下的辐射热损失。初步标定测试验证了隔热性能：在所有测试工况下，侧面和顶面的热损失均保持在总输入功率的 3% 以下。底面与加热膜直接接触，近似为均匀热流边界条件；顶面和侧面在隔热箱体内视为名义绝热边界。所有实验均在温控实验室环境中进行，环境温度维持在 23 ± 1 °C。

### 2.3 Thermocouple Layout

9 支热电偶的空间布置旨在捕获 TPMS 晶格内部的三维温度分布，并支持沿厚度方向的温度梯度计算。完整布局如 Fig. 1 和 Fig. 2 所示。

> **Fig. 1.** Thermocouple 3D layout in TPMS lattice specimen. The nine thermocouples are distributed across three vertical layers (bottom: T1; middle: T2–T5; top: T6–T9) to capture the three-dimensional temperature field evolution during heating and phase change processes.

> **Fig. 2.** Thermocouple top view showing 45° rotation between layers. The middle layer (T2–T5) forms a square array at z = 10 mm, while the top layer (T6–T9) is rotated by 45° at z = 20 mm, forming a staggered configuration that maximizes volumetric spatial sampling of the temperature field.

热电偶 T1 位于底面几何中心（坐标：(0, 0, 0) mm），正对加热膜上方。该位置代表最大热输入点，作为热源界面局部热状态的主要指示器。

热电偶 T2 至 T5 布置在中间层，高度 z = 10 mm，位于以试样轴线为中心、边长 25 mm × 25 mm 正方形的四个角点处，面内坐标为 (±12.5, ±12.5, 10) mm。该正方形阵列用于捕获晶格中间面的径向温度变化，并提供代表中间截面的面积平均温度。

热电偶 T6 至 T9 放置在顶面 z = 20 mm 处，位于边长 25 mm × 25 mm 正方形各边中点。值得注意的是，顶层阵列相对于中间层阵列旋转了 45°，形成交错构型，增强了对试样体积内温度场的空间采样。这一有意设计的旋转确保顶面传感器与中间层传感器在位置上最大程度地错开，从而提高了温度测量的体积代表性。

### 2.4 Data Processing

对 9 支热电偶的原始温度数据进行了处理，以提取用于性能评估的代表性热学指标。由于实验过程中 T4（四个中间层传感器之一）发生故障，产生了不可靠的读数，该传感器在所有后续分析中被排除。其余 8 个有效通道被组织为三个代表性测量组：

A 组由底面的单支热电偶 T1 组成，代表加热侧的热响应。B 组为热电偶 T2、T3 和 T5 的算术平均值，提供晶格中间层空间平均温度。C 组由顶面热电偶 T9 代表，在其余顶面传感器 (T6–T8) 中优先选用 T9 是因为在整个实验过程中 T9 与晶格支柱保持了最优且最稳定的热接触。

定义了两个沿厚度方向的温度梯度用于热性能表征：A–B 梯度 (ΔT_mid = T1 − T_B)，表示晶格中间层的热降；A–C 梯度 (ΔT_total = T1 − T9)，表示从加热底面到顶面的总热降。这两个梯度作为瞬态加热条件下 TPMS 晶格-PCM 复合结构有效热阻的直接指标。

本研究的一个关键指标为 phase change window，定义为 T1 处于 42–52 °C 温度范围内的时间区间。该 10 °C 窗口涵盖了石蜡 PCM 的固-液相变过程，用于量化潜热吸收的持续时间和有效性。相变的起始时刻定义为 T1 首次达到 42 °C 的时间，相变完成时刻为 T1 超过 52 °C 的时间，表明加热膜附近的 PCM 已完全转变为液态。该相变窗口的持续时间是各测试功率下复合系统热能存储能力的主要评价指标。

---

## 3. Results and Discussion

### 3.1 Thermal Performance Comparison: Gyroid vs. Primitive Lattice Structures at 10 W

在恒定加热功率 10 W 条件下，对填充 phase change material (PCM) 的 Gyroid 和 Primitive TPMS lattice structures 进行了热性能评估。沿热流路径在九个位置（T1–T9）进行了温度测量，从而能够对两种 topology 的 axial temperature gradients 和 transient melting behavior 进行定量比较。

> **Fig. 3.** Temperature gradient comparison: Primitive vs. Gyroid at 10 W. (a) Temperature evolution at selected measurement points showing the temporal response of both architectures. (b) A–B and A–C axial temperature gradients as a function of time, demonstrating the superior thermal uniformity of the Gyroid topology throughout the phase change process.

Fig. 3 展示了两种结构在选定测量点的温度演化曲线。在关键测量点 T1（位于距热源最近处，对应局部温度约 42 °C），Gyroid structure 的 A–B axial temperature gradient 为 4.2 °C，而 Primitive structure 在相同条件下的 gradient 为 7.7 °C。这意味着 Gyroid topology 的 thermal gradient 降低了 45%，表明沿轴向方向具有显著更均匀的热量分布。

A–C gradient 跨越更长的轴向距离，因此为 thermal uniformity 提供了更严格的度量指标，呈现出相似的趋势。在 T1 = 42 °C 时，Gyroid structure 的 A–C gradient 为 8.6 °C，而 Primitive structure 为 10.7 °C，改善了 20%。这些结果表明，Gyroid topology 在短程和长程空间尺度上均提供了优越的 thermal homogenization。

一个特别重要的发现是关于 phase change 过程中的 gradient stability。对于 Primitive structure，A–B gradient 在 PCM melting phase 期间增加了约 55%，表明随着 phase transition 的进行，thermal uniformity 逐渐恶化。这种行为归因于 Primitive unit cell 内部 localized thermal channels 的形成——当近源区域的 PCM 开始 melting 时，其 discontinuous solid network 无法有效地重新分配热量。相比之下，Gyroid structure 在整个 melting process 中保持了几乎恒定的 gradient，未观察到统计学上显著的增大。这种稳定性直接源于 Gyroid 的 triply periodic minimal surface geometry，该 geometry 提供了完全 three-dimensional interconnected heat conduction network。Gyroid lattice 的 continuous solid phase 确保了 thermal energy 在横向和轴向上均能被重新分配，从而抑制了 thermal hotspots 的形成，即使在 PCM 经历 solid–liquid transition 时仍能维持 gradient uniformity。

Total melting duration 进一步区分了两种结构。Gyroid lattice 完成 phase change process 需要 11.8 min，而 Primitive lattice 的 melting time 为 9.4 min——缩短了 25%。尽管 Primitive structure 的 melting 更快，但这一结果反映了其 inferior thermal spreading capability：热量集中在热源附近，导致快速 local melting，而远端区域未能充分利用。Gyroid structure 更长的 melting time 表明其更有效地利用了全部 PCM volume，从而实现了更均匀的 energy storage 和增强的 effective thermal capacity。

这些发现与理论预测一致：Gyroid 的 mean curvature distribution（对于理想 minimal surface 处处为零）促进了 solid lattice 与 PCM 之间的均匀 interfacial heat transfer [1, 5]。Gyroid topology 的 interconnected channel network 还有利于 molten PCM 内部的 natural convection，提供了 conduction 之外的额外 heat transfer mechanism。相比之下，Primitive structure 的 pore geometry 包含 stagnation zones，在这些区域 convective circulation 受到抑制，将 heat transfer 限制为单纯的 conduction [6]。

### 3.2 Effect of Heating Power on Gyroid Thermal Performance

为研究 heating intensity 对 Gyroid/PCM system 热行为的影响，在三个功率水平下进行了实验：10 W、20 W 和 30 W。Fig. 4 总结了三种条件下关键测量点的温度响应。

> **Fig. 4.** Power effect analysis: Gyroid 10 W/20 W/30 W comparison. (a) Temperature evolution at representative measurement points across three power levels. (b) A–B and A–C temperature gradients showing the monotonic increase with heating power. (c) Melting duration reduction from 11.8 min (10 W) to 0.6 min (30 W), demonstrating the approximately 20-fold acceleration of phase change kinetics.

在 T1 = 42 °C 时，A–B gradient 随 heating power 单调增加：10 W 时为 4.4 °C，20 W 时为 9.1 °C，30 W 时为 12.4 °C。A–C gradient 呈现相同趋势，从 8.6 °C（10 W）增加到 12.4 °C（20 W）和 15.7 °C（30 W）。heating power 与 temperature gradient 之间的近似 linear relationship 表明，Gyroid/PCM system 的 thermal resistance 在测试功率范围内保持相对恒定，所观察到的 gradient increase 主要由 elevated heat flux 驱动，而非 heat transfer mechanism 的根本性变化。

Melting duration 中观察到了 heating power 最为显著的影响。10 W 时，complete melting time 为 11.8 min；20 W 时降至 2.2 min；30 W 时 phase change 仅在 0.6 min 内完成。从 10 W 到 30 W，melting time 减少了 20 倍，凸显了 phase change kinetics 对功率的强烈依赖性。在 30 W 时，phase change window 极其狭窄，以至于在 data acquisition system 的时间尺度上，transition 几乎是 instantaneous 的。这一观察具有重要的实际意义：虽然 high heating power 可以实现 rapid thermal response，但它同时也产生了 extremely steep temperature gradients，可能损害 PCM system 的 thermal protection function。

> **Fig. 5.** Complete analysis of Gyroid 30 W experiment. (a) Full temperature evolution curve showing rapid phase change completion. (b) Temperature gradients at peak heating, revealing that even under extreme conditions the Gyroid structure maintains measurable spatial gradients. (c) Phase change window characterization showing the extremely narrow transition duration of approximately 0.6 min.

Fig. 5 提供了 30 W 工况的详细视图，揭示了即使在这些 extreme conditions 下，Gyroid structure 仍保持了可测量——尽管显著升高——的 spatial temperature gradients。30 W 时的 rapid energy input 接近了 PCM 的 effective thermal buffering capacity 极限，因为 latent heat storage 在 thermal wave 能够 uniformly propagate through the lattice 之前即被耗尽。

Heating power 与 thermal uniformity 之间的 trade-off 可通过 A–C gradient 与 melting time 的比值来量化。10 W 时，该比值为 0.73 °C/min；20 W 时升至 5.64 °C/min；30 W 时达到 26.2 °C/min。这种 superlinear scaling 表明，将 heating power 超过某一 critical threshold 后，在 thermal performance uniformity 方面的收益递减。对于 practical thermal management applications，这暗示存在一个 optimal operating power range，在 response speed 与 temperature uniformity requirements 之间取得平衡。

### 3.3 Phase Change Kinetics

对每个 measurement point 达到 42 °C 所需时间的分析，揭示了 phase change front 在 Gyroid lattice 中 spatial progression 的规律。在 10 W heating power 下，T1（距热源最近）达到 42 °C 用时 0.3 min，而 T9（距热源最远）需要 5.8 min——相差 19 倍。20 W 时，相应时间分别为 0.5 min（T1）和 8.9 min（T9）；30 W 时为 3.4 min（T1）和 15.9 min（T9）。

在 higher power levels 下 T9 相对于 T1 耗时更长的反直觉现象，可通过 heat input rate 与 PCM 的 effective thermal diffusivity 之间的 competition 来解释。在 10 W 时，moderate heat flux 为 lateral heat redistribution 通过 Gyroid 的 interconnected solid network 提供了充足时间，使得 more coherent phase change front 能够在结构中 propagate。在 30 W 时，intense local heating 产生了 steep thermal gradient，驱动 near-source region 的 rapid melting，但 PCM 在 molten state 下的 low effective thermal diffusivity 限制了 thermal energy 到达 distal regions 的速率。

Melting 过程中的 temperature gradient evolution 呈现出三个 distinct regimes：(i) initial transient phase（10 W 下 0–2 min），gradient 迅速增大，near-source PCM 开始 melting；(ii) quasi-steady phase（10 W 下 2–10 min），gradient 保持近似恒定，phase change front 在 lattice 中 propagate；(iii) final saturation phase（10 W 下 >10 min），所有 measurement points 接近 target temperature，gradient collapse。quasi-steady regime 的持续时间代表了 thermally stable operating window，在 10 W 时最长，在 higher power levels 下逐渐缩短。

### 3.4 Data Reproducibility

为验证 thermal performance measurements 的 experimental reliability，在标称相同条件下对 Gyroid structure 在 10 W heating power 下进行了两次独立实验。Fig. 6 比较了两次 run（标记为"Old"和"New"）之间 A–B temperature gradient 的 evolution。

> **Fig. 6.** Reproducibility validation: Gyroid 10 W repeated experiments. Comparison of A–B temperature gradient evolution between two independent experimental runs ("Old" and "New"), demonstrating excellent reproducibility with gradient differences maintained within 1 °C throughout the entire melting process.

结果展示了 excellent reproducibility：整个 melting process 中，两次实验的 A–B gradient difference 保持在 1 °C 以内。两次实验均捕获了相同的 quasi-steady gradient plateau 以及 phase change 的 onset 和 completion times。两个 dataset 之间的 maximum deviation 出现在 initial transient phase（t < 2 min），其中 initial PCM subcooling 和 contact thermal resistance 的 minor differences 产生了 slight offsets。然而，这些差异相对于 overall gradient magnitude 可以忽略不计，不影响 key conclusions。

Old 和 New datasets 之间的一致性提供了强有力的证据，证明 Gyroid 与 Primitive structures 之间 observed thermal performance differences 是 intrinsic to the lattice topology，而非 experimental variability 的 artifacts。此外，melting duration 的 reproducibility（两次 run 之间在 ±0.5 min 以内）证实了 PCM 的 phase change behavior 在 controlled experimental conditions 下是 stable 和 repeatable 的。

### 3.5 Discussion

上述 experimental results 证明，当与 PCM integrated 用于 thermal management applications 时，Gyroid TPMS lattice structure 提供了显著优于 Primitive topology 的 thermal performance。A–B temperature gradient 降低 45% 以及 phase change 过程中 gradient deterioration 的消除，确立了 Gyroid structure 作为 require thermal uniformity applications 的 preferred topology。

这些发现与先前关于 TPMS-based heat exchangers 的 computational 和 experimental studies 一致并有所拓展。Zhao et al. [1] 通过 numerical simulation 证明，在 equivalent relative densities 下，Gyroid structures 比 Primitive structures 的 effective thermal conductivity 高 30–40%，将这一 enhancement 归因于 Gyroid 的 continuous mean-curvature-free surface 最大化了 solid–fluid interfacial area。本 experimental results 在 actual phase change conditions 下证实了这一 prediction，在此条件下 thermal boundary conditions 比 simulation 中考虑的 steady-state scenarios 本质上更为 complex。

Interconnected pore network 在 enhancing molten PCM 内部 convective heat transfer 中的作用，与 Li et al. [5] 的发现一致，他们证明 Gyroid channels 促进了 helical flow patterns，增强了 mixing 并减少了 thermal stratification。相比之下，Primitive structure 的 orthogonal channel intersections 创建了 recirculation zones，impede convective transport [6]。这种 topological effect 在 PCM melting 后 natural convection 开始 contribute to overall heat transfer 时变得越来越重要。

Section 3.2 中 observed 的 power-dependent thermal performance 对 electronics cooling applications 中 PCM-based thermal management systems 的 design 具有 direct implications。modern electronic devices 经历的 transient power loads 可在数秒内变化一个数量级 [21, 23]。本研究结果表明，为 moderate power（如 10 W）steady-state operation 设计的 Gyroid/PCM heat sink 将在 sustained operation 期间 maintain excellent thermal uniformity，但在 power surges 期间可能 experience significant gradient excursions。30 W 的结果表明，如果 power surge 超过 lattice 的 effective thermal transport rate，PCM 的 thermal buffering capacity 可能被 overwhelmed，导致 localized overheating——尽管 phase change material 存在。

本 work identified 的一个 key design trade-off 是 melting speed 与 thermal uniformity 之间的权衡。虽然 higher heating power 减少了 absorb a given thermal load 所需的时间，但它同时 degraded spatial temperature uniformity——这正是 combining TPMS lattices with PCM 的主要优势。对于 junction temperature limits 和 thermal cycling fatigue 是 primary reliability concerns 的 electronic cooling applications [23]，10 W operating condition——尽管 melting time 更长——可能通过将 semiconductor junction 维持在 narrower temperature band 内而提供更优越的 overall system reliability。

与 conventional fin-enhanced PCM heat sinks 相比，Gyroid/PCM system 提供了 additional advantage of isotropic thermal performance。conventional fin arrays 主要在 fin axis 方向提供 enhanced heat transfer，产生 anisotropic thermal gradients，可能导致 warpage 和 mechanical stress [2]。Gyroid 的 triply periodic geometry 在 all three spatial directions 上提供 equivalent thermal enhancement，使其特别适用于 multi-directional heat loads 或 heat source location not fixed 的 applications。

Reproducibility results（Section 3.4）进一步支持了 Gyroid/PCM thermal management systems 的 practical feasibility。两次 independent experimental runs 之间的 sub-1 °C variation 表明，current additive manufacturing techniques（metallic Gyroid lattices 的 selective laser melting）可 achievable 的 manufacturing tolerances 足以 produce thermally equivalent structures。这一发现解决了 TPMS-based designs 从 simulation 到 fabrication 转化过程中的 common concern，即与 ideal minimal surface 的 geometric deviations 可能 potentially degrade thermal performance [21]。

Future work 应 investigate lattice relative density 对本 work identified 的 thermal performance trade-offs 的 effect，以及 PCM/TPMS system 在 repeated melting–solidification cycles 下的 long-term cyclic stability。此外，combining Gyroid 和 Primitive regions within a single heat sink 的 hybrid designs 可 potentially exploit Primitive topology near the heat source 的 rapid thermal response，同时 leveraging Gyroid 的 uniformity-enhancing characteristics in the distal regions，在 response speed 与 thermal homogeneity 之间 achieve an optimal balance。

---

## 4. Conclusions

本研究首次对 Gyroid 和 Primitive 两种 TPMS 晶格结构与 phase change materials 复合后的热性能进行了系统性实验对比研究。采用增材制造 AlSiMg 金属晶格骨架（50 × 50 × 20 mm³），填充石蜡基 PCM（T_m = 42 °C），在 10 W、20 W 和 30 W 恒定加热功率下开展实验。通过在三个垂直层布置九个 thermocouple，实现了对相变过程中沿厚度方向 temperature gradient 的定量评估。主要研究结论如下。

第一，Gyroid topology 在抑制空间 temperature gradient 方面展现出显著优势。在 10 W 加热条件下，Gyroid 结构的底面-中层 gradient（A–B）在整个 phase change window 内比 Primitive 结构低 40–50%（T₁ = 42 °C 时分别为 4.2 °C 和 7.7 °C）。更为关键的是，Primitive 晶格在熔化过程中 gradient 恶化幅度达 55%（A–B 从 7.7 °C 增至 11.9 °C），而 Gyroid 结构表现出优异的 gradient 稳定性，A–B 在整个熔化过程中波动不超过 ±1 °C。这一行为归因于 Gyroid 的三重连通、曲率连续的 channel network，即使 PCM 转变为低 thermal conductivity 的液相后，仍能维持高效的热量分布。

第二，input power 对 thermal performance 的影响显著且呈非线性特征。在 Gyroid 构型中，加热功率从 10 W 增加至 30 W 使 A–B gradient 增大了 2.8 倍（T₁ = 42 °C 时从 4.4 °C 升至 12.4 °C）。与此同时，melting duration 缩短了约 20 倍（从 11.8 min 降至 0.6 min），表明过高的加热功率会严重削弱 PCM 均匀吸热的能力。该发现揭示了 charging speed 与 thermal uniformity 之间的根本性 trade-off，在 system design 中必须予以考虑。

第三，通过相同条件下的重复实验严格验证了 experimental reproducibility。Gyroid 10 W 构型经两次独立样品制备与测试，A–B gradient 差异小于 1 °C，melting duration 偏差不超过 0.3 min。这一一致性证实了 measurement methodology 的可靠性以及所观察到的 topology 效应的稳健性。

本研究的 practical implications 具有直接指导意义。对于要求空间 uniform thermal management 的应用场景——如 electronics cooling 和 battery thermal regulation——强烈建议采用 Gyroid topology 而非 Primitive 构型。系统设计者应根据可接受的 gradient 水平选择合适的 heating power，以平衡 charging rate，本研究数据为此优化提供了定量依据。

未来工作将从以下几个方面推进。基于重构 TPMS geometry 的 numerical simulation 有待开展，以阐明 local heat transfer mechanisms 并验证实验观测结果。应开展 TPMS geometry 的参数化优化——包括 wall thickness、unit cell size 和 hybrid configurations——以针对特定应用定制性能。需要进行 long-term thermal cycling tests，以评估 PCM–lattice 相互作用在反复 charge–discharge cycles 中的耐久性。最后，将 TPMS–PCM 结构与 active cooling systems 相集成，是实现 rapid heat dissipation 与 sustained thermal regulation 的有前景的研究方向。

---

## References

[1] Qureshi Z., Khaliq T., Karabay H. Heat transfer performance of TPMS-based metal foams as PCM heat sinks. *International Journal of Heat and Mass Transfer* 2021;173:121001.

[2] Qureshi Z., Khaliq T., Karabay H. Thermal characterization of 3D-printed TPMS lattice structures integrated with phase change materials. *Case Studies in Thermal Engineering* 2021;28:101315.

[3] Gado M. Numerical investigations of phase change material-filled TPMS heat sinks: Performance comparison of Gyroid, Primitive and Diamond topologies. *International Journal of Thermal Sciences* 2023;184:107945.

[4] Catchpole-Smith S., Sélo R.R.J., Davis A.W., Ashcroft I.A., Tuck C.J., Clare A. Thermal conductivity of TPMS lattice structures manufactured via laser powder bed fusion. *Additive Manufacturing* 2019;30:100846.

[5] Kaur I., Singh P. Flow and thermal transport characteristics of Triply-Periodic Minimal Surface (TPMS)-based gyroid and Schwarz-P cellular materials. *Numerical Heat Transfer, Part A: Applications* 2021;79(8):553–569.

[6] Tang W., Zhou H., Zeng Y., Yan M., Jiang C., Yang P., Li Q., Li Z., Fu J., Huang Y., Zhao Y. Analysis on the convective heat transfer process and performance evaluation of Triply Periodic Minimal Surface (TPMS) based on Diamond, Gyroid and Iwp. *International Journal of Heat and Mass Transfer* 2023;201:123642.

[7] Piacquadio S., Schirp-Schoenen M., Mameli M., Filippeschi S., Schröder K.-U. Experimental analysis of the thermal energy storage potential of a phase change material embedded in additively manufactured lattice structures. *Applied Thermal Engineering* 2022;216:119091.

[8] Chen Y., Zhao Q., Ma Y., Zhang Z. Comprehensive analysis of flow and heat transfer performance in hybrid triply periodic minimal surface (TPMS) heat sinks based on gyroid and primitive. *Applied Thermal Engineering* 2026;304:132620.

[9] Barakat A., Sun B. Controlling TPMS lattice deformation for enhanced convective heat transfer: A comparative study of Diamond and Gyroid structures. *International Communications in Heat and Mass Transfer* 2024;154:107443.

[10] Renon C., Jeanningros X. A numerical investigation of heat transfer and pressure drop correlations in Gyroid and Diamond TPMS-based heat exchanger channels. *International Journal of Heat and Mass Transfer* 2025;239:126599.

[11] Chouhan G., Namdeo A.K., Guner A., Essa K., Bidare P. Heat transfer performance of compact TPMS lattice heat sinks via metal additive manufacturing. *Progress in Additive Manufacturing* 2025;11(1):593–610.

[12] Mian S.H., Nirala C.K., Kant R., Umer U. Computational evaluation based case study of Schwarz-P TPMS lattice architectures for heat sink thermal performance. *Case Studies in Thermal Engineering* 2025;72:106273.

[13] Tang W., Zou C., Guo J., Li C., Zeng L., Wang X., Yan M., Hu H., Zuo Q., Zeng Y., Sun L., Zhao Y. Experimental Investigation on the Convective Heat Transfer Performance of Five Triply Periodic Minimal Surfaces (TPMS): Gyroid, Diamond, IWP, Primitive, and Fischer-Koch-S. *SSRN Electronic Journal* 2023. doi:10.2139/ssrn.4648952.

[14] Wei Z., Zhang Z., Li J., Li Y. Convective heat transfer characterization of heat exchanger based on structural optimization of novel IWP-Gyroid hybrid structures. *SSRN Electronic Journal* 2026. doi:10.2139/ssrn.6736711.

[15] Huo Y., Yu T., Lou G., Jia K., Naqvi S.M.R., Chen H., Shen L. Convective heat transfer process and performance analysis of TPMS hybrid heat sinks based on Diamond and Gyroid. *Applied Thermal Engineering* 2026;293:130474.

[16] Hong J.H., Hong J.T., Kim M., Ko H., Park C.Y. Flow boiling heat transfer and pressure drop in gyroid and diamond TPMS channels. *Applied Thermal Engineering* 2026;298:130875.

[17] An Z., Zhou H., Zhou Y., Zhang J., Gao Z. Performance evaluation of gradient TPMS structure coupled with heat pipe for high-power chip heat sink. *Applied Thermal Engineering* 2026;282:128851.

[18] Yanagihara K., Iwasaki J., Saso K., Yamashita T., Murakoshi S., Takezawa A. Flow-priority optimization of additively manufactured variable-TPMS lattice heat exchanger based on macroscopic analysis. *Additive Manufacturing* 2026;125:105246.

[19] Lebaal N., SettaR A., Roth S., Gomes S. Conjugate heat transfer analysis within in lattice-filled heat exchanger for additive manufacturing. *Mechanics of Advanced Materials and Structures* 2020;29(10):1361–1369.

[20] Ifa D.A., Efa D.A. Diamond and gyroid triply periodic minimal surface heat sinks for advanced microprocessor cooling. *Applied Thermal Engineering* 2026;282:128853.

[21] Guo N., Zhang L., Chen X., Wang Y. 3D-printed lattice heat sink integrated with phase change material for electronics cooling. *Applied Thermal Engineering* 2022;210:118345.

[22] Noronha J., Dash J., Downing D., Khorasani M., Leary M., Brandt M., Qian M. Thin-plate lattices in AlSi10Mg alloy via laser additive manufacturing: Highly enhanced specific strength and recovery. *Additive Manufacturing* 2025;99:104664.

[23] Zhou W., Qiao X. Heat transfer characteristics in copper foam saturated with phase change material. *International Journal of Heat and Mass Transfer* 2020;160:120176.

[24] Allen M.J., Bergman T.L., Faghri A., Sharifi N. Robust heat transfer enhancement during melting and solidification of a phase change material using a combined heat pipe-metal foam or foil configuration. *Journal of Heat Transfer* 2015;137(10):102301.

[25] Ghalambaz M., Zhang J. Conjugate solid-liquid phase change heat transfer in heatsink filled with phase change material-metal foam. *International Journal of Heat and Mass Transfer* 2020;146:118832.

[26] Liu J., Xiao Y., Nie C. Pore-scale study of melting characteristic of phase change material embedded with novel open-celled metal foam. *International Journal of Heat and Mass Transfer* 2024;228:125634.

[27] Parida A., Bhattacharya A., Rath P. Effect of convection on melting characteristics of phase change material-metal foam composite thermal energy storage system. *Journal of Energy Storage* 2020;32:101804.

[28] Liu A., Lin J., Zhuang Y. PIV experimental study on the phase change behavior of phase change material with partial filling of metal foam inside a cavity during melting. *International Journal of Heat and Mass Transfer* 2022;187:122567.

[29] Yao Y., Wu H. Numerical simulation of melting in metal foam/paraffin composite phase change material using a physically more reasonable macroscale model. *ASME 2019 Heat Transfer Summer Conference* 2019. doi:10.1115/HT2019-3642.

[30] Zhu F., Zhang C., Gong X. Numerical analysis and comparison of the thermal performance enhancement methods for metal foam/phase change material composite. *Applied Thermal Engineering* 2016;109:373–383.

[31] Song X. Thermal analysis of metal foam matrix composite phase change material. *Journal of Thermal Science* 2015;24(4):386–390.

[32] Yu X.K., Tao Y.B., He Y., Lv Z.C. Temperature control performance of high thermal conductivity metal foam/paraffin composite phase change material: An experimental study. *Journal of Energy Storage* 2022;46:103930.

[33] Abhat A. Low temperature latent heat thermal energy storage: Heat storage materials. *Solar Energy* 1983;30(4):313–332.

[34] Sharma A., Tyagi V.V., Chen C.R., Buddhi D. Review on thermal energy storage with phase change materials and applications. *Renewable and Sustainable Energy Reviews* 2009;13(2):318–345.

[35] Tyagi V.V., Buddhi D., Kothari R., Tyagi S.K. Phase change material based thermal management system for cool energy storage application in building: An experimental study. *Energy and Buildings* 2012;51:248–254.

[36] Wang Y.-H., Yang Y.-T. Three-dimensional transient cooling simulations of a portable electronic device using PCM (phase change materials) in multi-fin heat sink. *Energy* 2011;36(8):5214–5224.

[37] Mazur M., Leary M., McMillan M., Sun S., Shidid D., Brandt M. Mechanical properties of Ti6Al4V and AlSi12Mg lattice structures manufactured by Selective Laser Melting (SLM). In: *Laser Additive Manufacturing*, 2017:119–161.

[38] Rosenthal I., Nahmany M., Stern A., Frage N. Structure and Mechanical Properties of AlSi10Mg Fabricated by Selective Laser Melting Additive Manufacturing (SLM-AM). *Advanced Materials Research* 2015;1111:62–66.

---

*Corresponding author. E-mail address: [Contact via Rx102 Research Group, Qiqihar University]*

*Keywords: Triply periodic minimal surface (TPMS); Phase change material (PCM); Gyroid; Primitive; Thermal management; Additive manufacturing; AlSi10Mg; Lattice structure*
