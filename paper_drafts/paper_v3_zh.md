# TPMS晶格结构结合相变材料热性能的实验研究：Gyroid、IWP与Primitive架构的对比研究

---

## 摘要

三周期极小曲面（TPMS）晶格结构与相变材料（PCM）的集成，为高功率电子器件的先进被动式热管理提供了一种极具前景的方案。然而，在受控热加载条件下对不同TPMS拓扑结构进行实验对比的研究仍然十分有限，且此前尚无研究同时在PCM集成晶格结构中对三种TPMS架构进行比较。本研究对三种TPMS架构——Gyroid、IWP（I-Wrapped Package）和Primitive（Schwarz-P）——结合石蜡基PCM的热性能进行了系统的实验研究。晶格结构采用AlSi10Mg合金通过激光粉末床熔融增材制造技术制备，试样尺寸为50 × 50 × 20 mm³。将相变温度为42 °C的商业石蜡在真空条件下灌注至晶格孔隙中。在均匀热通量边界条件下，于三个恒定功率水平（10 W、20 W和30 W）下进行瞬态加热实验，九个热电偶分布在三个垂直层上以捕捉温度场的时空演化规律。结果揭示了一个关键的功率依赖性性能排名反转现象：在10 W加热条件下，IWP实现了最长的熔化持续时间（12.33 min），优于Gyroid（11.75 min）和Primitive（8.28 min）；然而，在20 W和30 W条件下，排名完全反转，Gyroid分别达到2.10 min和0.62 min，而IWP仅为0.93 min和0.40 min。Gyroid在所有功率水平下均表现出优异的温度均匀性（A–B gradient：4.43–15.75 °C，而IWP为6.12–19.76 °C，Primitive为7.44–24.13 °C），并展现出最低的功率敏感性（从10 W到30 W的熔化持续时间缩减倍数为19.1×，而IWP为30.8×，Primitive为29.6×）。这些发现建立了功率依赖的拓扑结构选择标准：Gyroid在宽功率范围和高功率应用中表现最优，而IWP在低功率精密热管理中更具优势。本研究为TPMS基PCM热管理系统的工程设计提供了实验基准数据和拓扑结构选择指导。

**关键词：** TPMS lattice; Gyroid; IWP; Primitive; Phase change material; Thermal management; Additive manufacturing; Temperature uniformity; Power sensitivity

---

## 1. 引言

现代电子器件的持续微型化和性能提升对热管理提出了日益严格的要求。随着电子器件功率密度的不断攀升——在先进微处理器和大功率LED中已超过100 W/cm²——散热片阵列和均热器等传统被动式散热策略正接近其基本极限[1]。高效的热管理对于确保器件可靠性和在瞬态热载荷下维持性能稳定性至关重要，这推动了对能够在紧凑空间内适应高热通量的先进热调节技术的持续研究兴趣。

相变材料（PCM）作为被动式热能存储和瞬态热管理的解决方案已引起广泛关注。通过在近乎恒温的固-液相变过程中吸收和释放大量潜热，PCM能够有效缓冲热尖峰并将组件温度维持在安全工作窗口内[3]。石蜡因其高潜热容量、化学稳定性以及适用于电子器件冷却的相变温度而被广泛采用。然而，其固有的低热导率（通常为0.2–0.4 W/m·K）严重限制了热量的吸收和释放速率，导致热响应迟缓和潜热利用不充分。克服这一限制需要高导热性的结构骨架，以增强PCM整体体积内的有效热传输。

金属晶格结构作为PCM复合材料的导热基体已被广泛研究。其中，三周期极小曲面（TPMS）架构因其高比表面积、相互连通的孔隙网络和力学高效的拓扑结构而受到极大关注[1,5]。TPMS结构由零平均曲率曲面定义，将三维空间分割为两个连续的、相互贯穿的子体积。存在多种不同的TPMS拓扑结构，每种拓扑都提供独特的通道几何形状和流动特性，对传热性能产生深远影响。Gyroid曲面具有单一连续通道和手性对称性，产生螺旋形流道路径，促进流体混合和二次对流[6]。Primitive（Schwarz-P）曲面包含两个独立的、相互贯穿的通道网络，通过周期性开口相连，形成具有不同曲折度的双向传输路径。IWP（I-Wrapped Package）曲面同样将空间分割为两个独立的相互贯穿通道网络，但在缠绕拓扑上与Primitive存在根本差异：IWP通道呈现出更复杂的笼状包围结构，具有更高的亏格和更大的单位体积表面积，产生增强的流动约束和改变的热传输路径[5,6]。这三种拓扑结构涵盖了通道连通性、曲折度和约束度的丰富设计空间，因此对它们进行系统比较对于推进TPMS基热管理研究至关重要。

近期研究已展示了TPMS基结构在增强PCM热管理方面的潜力。Qureshi等人[1]研究了TPMS基金属泡沫作为PCM散热器的性能，报告了与传统泡沫几何结构相比，温度均匀性显著改善且充热时间缩短。在后续研究中，Qureshi等人[2]探索了结合PCM的3D打印TPMS晶格结构，证明了制备具有可定制热性能的复杂周期性架构的可行性。Gado[3]对填充PCM的TPMS散热器进行了数值研究，发现Gyroid拓扑在熔化速率和储热效率方面优于Primitive和Diamond曲面。Tang等人[6]研究了Gyroid结构中的对流传热，揭示了手性通道几何形状诱导的二次流与热传输增强之间的相互作用。Kaur和Singh[5]建立了换热器应用中多种TPMS拓扑的Nusselt数和摩擦因子的设计关联式。

增材制造（AM）技术，特别是激光粉末床熔融（L-PBF）的出现，使得以空前的几何精度和表面质量制备TPMS晶格结构成为可能[2]。与受限于模具设计和脱模复杂性的传统方法不同，AM允许直接实现数学定义的TPMS几何形状，并可精确控制支柱尺寸、孔隙率和单元尺寸。Guo等人[21]展示了一种结合PCM的3D打印晶格散热器用于电子器件冷却，表明增强的热导率网络显著降低了瞬态运行期间的峰值温度。Zhou和Qiao[23]研究了饱和PCM的铜泡沫中的传热特性，强调了孔隙尺度形貌在决定有效热性能方面的重要性。

尽管取得了这些进展，在TPMS-PCM耦合热系统的实验理解方面仍存在显著差距。现有研究大多依赖数值模拟或解析模型来预测TPMS-PCM构型的热行为[1,3]。在受控和可重复的热加载条件下直接对比不同TPMS拓扑结构的实验研究明显匮乏。特别是，此前尚无实验研究同时在PCM集成晶格结构中对三种TPMS拓扑——Gyroid、Primitive和IWP——进行比较。加热功率对这三种拓扑结构的瞬态热响应、相变动力学和空间温度分布的影响尚未通过实验进行系统表征。理解这些关系对于验证计算模型、建立功率依赖的性能排名以及为实际工程应用提供设计指导至关重要。

本研究首次对三种TPMS晶格拓扑——Gyroid、Primitive和IWP——结合石蜡基PCM的热性能进行了系统的实验研究。TPMS晶格结构采用AlSi10Mg合金通过L-PBF增材制造技术制备，样品尺寸为50 × 50 × 20 mm³。将相变温度为42 °C的石蜡基PCM渗入晶格孔隙中。在恒定热通量边界条件下，于三个功率水平（10 W、20 W和30 W）下进行瞬态加热实验。多个热电偶被战略性地布置在三个垂直层上，以捕捉加热和相变过程中温度场的空间和时间演化。本研究的主要目标为：（1）从温度均匀性、热梯度和PCM熔化动力学方面比较Gyroid、Primitive和IWP TPMS晶格的热性能；（2）表征加热功率对所有三种拓扑结构的瞬态热响应和相变行为的影响；（3）建立三种TPMS结构的功率依赖性能排名，确定不同工况下的最优拓扑选择标准；（4）提供实验基准数据，为电子冷却应用中TPMS基PCM热管理系统的优化设计提供参考。

## 2. 实验部分

### 2.1 材料与试样制备

本研究研究的三周期极小曲面（TPMS）晶格结构采用AlSi10Mg合金通过选择性激光熔融（SLM）技术制备，SLM是一种粉末床熔融增材制造工艺。研究了三种不同的TPMS拓扑结构：Gyroid、IWP（I-Wrapped Package）和Primitive（Schwarz Primitive）曲面，它们均属于立方晶系，以其相互连通的通道网络和良好的比表面积而著称。SLM工艺的层厚为30 μm，经micro-CT分析确认相对密度超过99%。关键工艺参数包括：激光功率200 W，扫描速度800 mm/s，扫描间距0.12 mm，相邻层间采用67°条带旋转以最小化各向异性。

晶格试样的名义外部尺寸设计为50 × 50 × 20 mm³，提供了足够的单元数量以保证热代表性行为，同时与加热平台和隔热组件兼容。单元尺寸的选择兼顾了制造分辨率和多孔结构内传热的特征长度尺度。制备完成后，所有试样均在300 °C下进行2小时的去应力热处理，以缓解逐层SLM工艺产生的残余应力。表面粗糙度未做进一步处理，因为原始态形貌被认为可代表实际热管理应用的情况。

相变材料（PCM）为商业级石蜡，标称熔点为42 °C，熔化潜热约为200 kJ/kg。选择该石蜡是基于其良好的热物性表征、化学稳定性、可忽略的过冷度以及与铝合金基体的相容性。PCM在−0.09 MPa真空条件下灌注至多孔TPMS晶格中，以确保完全填充相互连通的空隙空间。每个试样在灌注前后分别称重（精度±0.01 g），所有试样的PCM质量载荷一致性在±2%以内。

### 2.2 实验装置

实验装置包括恒功率电阻加热系统、基于热电偶的温度测量阵列、多通道数据采集系统和隔热保温箱体。一块与试样底面尺寸匹配的柔性聚酰亚胺Kapton加热器使用导热硅脂（> 1.5 W/(m·K)）粘贴在底面。加热器由稳压直流电源驱动，提供10 W、20 W和30 W的恒定功率水平，分别对应4.0、8.0和12.0 kW/m²的热通量，涵盖了与电子器件冷却应用相关的温和至高强度热加载条件。

温度测量采用九个K型（镍铬-镍铝）热电偶（丝径0.25 mm，结点直径约0.5 mm）。热电偶通过钻在顶面的小孔（< 1 mm）嵌入预定位置，并使用高温导热胶粘剂固定，以确保在加热和熔化循环中保持可靠接触。热电偶布置详见第2.3节。

所有信号传输至多通道数据采集系统（NI-9213，National Instruments），配备冷端补偿，以1 Hz频率同步采集全部九个通道——足以捕捉显热加热和相变过程中的瞬态热响应。系统经NIST可追溯参考温度计校准，整体测量不确定度为±0.5 °C。

整个组件置于隔热箱中，隔热箱由25 mm厚的挤塑聚苯乙烯（XPS）泡沫板构成，内衬10 mm厚的陶瓷纤维毯以抑制高温下的辐射热损失。初步标定试验确认，在所有测试条件下，侧面和顶面热损失均保持在总输入功率的3%以下。与加热器直接接触的底面近似为均匀热通量边界条件，而顶面和侧面在隔热箱内处理为准绝热边界。所有实验均在温度受控的实验室环境中进行，环境温度维持在23 ± 1 °C。

### 2.3 热电偶布置

九个热电偶的布置旨在捕捉TPMS晶格内部的三维温度分布，并实现贯穿厚度方向温度梯度的计算，如图1和图2所示。

热电偶T1位于底面几何中心（坐标：(0, 0, 0) mm），正对加热器元件上方。该位置代表最大热输入点，作为热源界面处局部热状态的主要指示器，相变过程首先在此处启动。

热电偶T2至T5布置在z = 10 mm的中间层，位于以试样轴线为中心、边长为25 mm × 25 mm正方形的四个角点上，坐标为(±12.5, ±12.5, 10) mm。该阵列捕捉中间面内的径向温度变化，并提供面积平均的中间层温度。

热电偶T6至T9布置在z = 20 mm的顶面，位于25 mm × 25 mm正方形各边的中点。该顶层阵列相对于中间层旋转了45°，形成交错构型，通过将顶面传感器与中间面传感器最大化偏移，增强了试样体积内的空间采样覆盖。

### 2.4 数据处理

对全部九个热电偶的原始温度数据进行处理，提取用于性能评估的代表性热指标。由于实验过程中传感器故障，热电偶T4（四个中间面传感器之一）在某些测试中产生了不可靠的读数，因此在后续分析中予以排除。其余功能正常的通道被组织为三个测量组：

A组由底面的T1组成，代表加热器侧的热响应。B组为T2、T3和T5的算术平均值（对于IWP结构，当T5表现出异常行为时为T2和T3的平均值），提供空间平均的中间层温度。C组由顶面的T9表示（对于IWP结构在10 W和20 W下为T8和T9的平均值），选择该点是因为其与晶格支柱具有最佳且最稳定的热接触。

定义了两个贯穿厚度方向的温度梯度：A–B gradient（ΔT_mid = T₁ − T_B），代表穿过中间层的温度降；A–C gradient（ΔT_total = T₁ − T₉），代表从加热底面到顶面的总温度降。这些梯度反映了TPMS晶格-PCM复合材料在瞬态加热条件下的有效热阻。

一个关键指标是相变窗口，定义为T1保持在42–52 °C范围内的时间间隔。该10 °C窗口涵盖了石蜡PCM的固-液相变过程，量化了潜热吸收的持续时间和有效性。当T1首次达到42 °C时标识为相变开始，当T1超过52 °C时标识为相变完成，表明加热器附近PCM已完全熔化。相变窗口持续时间作为各功率水平下复合系统热能存储能力的主要指标。

## 3. 结果与讨论

### 3.1 10W加热功率下的热性能比较

在10 W恒定加热功率下评估了三种TPMS结构——Gyroid、IWP和Primitive——的热性能，以建立低功率区间的基础行为。结果揭示了三种架构在熔化动力学和温度均匀性方面的显著差异。

**熔化持续时间。** 在10 W条件下，IWP结构表现出最长的完全熔化持续时间，为12.33分钟，其次为Gyroid的11.75分钟，而Primitive结构的熔化速度明显更快，仅为8.28分钟。这意味着IWP的熔化时间比Primitive长48.9%，表明在相同边界条件和PCM体积下，三种结构具有根本不同的传热特性。IWP延长的熔化持续时间表明其在低功率输入下具有更优的热量分配能力，使可用热能更有效地用于相变。

**温度梯度。** 通过两个关键温度下测量点A和B之间的温差来评估温度均匀性：42°C（熔化初期）和55°C（熔化后期）。在42°C时，Gyroid结构表现出优异的温度均匀性，A-B温差仅为4.43°C，而IWP为6.12°C，Primitive为7.44°C。这分别比IWP改善了27.6%，比Primitive改善了40.5%。

这一优势在55°C时更为显著，Gyroid保持了相对较低的5.50°C梯度，而IWP达到7.33°C，Primitive则表现出明显更大的11.25°C梯度。Gyroid结构的梯度从42°C到55°C仅增加了24.2%，而IWP为19.8%，Primitive则大幅增加了51.2%。这种差异化的梯度演化表明，虽然所有结构在熔化推进过程中都经历热不均匀性的增加，但Primitive架构遭受了Gyroid设计中基本不存在的严重热瓶颈问题。

**梯度扩展分析。** 从42°C到55°C温度梯度的相对扩展提供了熔化过程中热稳定性的洞察。Gyroid的梯度扩展为24.25%，表明热不均匀性发展适中。IWP表现出类似的行为，扩展率为19.77%，表明尽管熔化持续时间更长，但具有可比的热稳定性。与之形成鲜明对比的是，Primitive表现出51.14%的大幅梯度扩展，是Gyroid的两倍以上，表明熔化推进过程中存在严重的热不均匀性。

Primitive结构较差的温度均匀性可归因于其较简单的通道几何形状，提供了较少的并行传热路径，更容易受到局部热阻变化的影响。随着PCM熔化和自然对流的发展，Primitive架构有限的连通性阻碍了热能的有效再分配，导致热点的形成。

这些结果确立了在低加热功率下，IWP架构提供最优的熔化持续时间，而Gyroid实现了优异的温度均匀性，两者均显著优于Primitive结构。

### 3.2 加热功率对热性能的影响

将加热功率从10 W增加到20 W和30 W后，揭示了功率依赖性的行为，从根本上改变了TPMS结构之间的性能层次。

**熔化持续时间缩减。** 三种结构均表现出熔化持续时间随功率增加而大幅缩减，但缩减幅度差异显著。对于Gyroid，熔化时间从10 W时的11.75分钟降至20 W时的2.10分钟，进一步降至30 W时的0.62分钟，总缩减倍数为18.95×。从10 W到20 W的缩减为5.60×，而从20 W到30 W的进一步缩减仅为3.39×，表明在较高功率水平下敏感性递减。

IWP表现出更剧烈的响应，从12.33分钟降至0.93分钟（20 W）和0.40分钟（30 W），总缩减倍数为30.83×。10 W到20 W的缩减为13.26×，20 W到30 W的缩减为2.33×，表明对中等功率增加极度敏感，但在最高功率水平下相对稳定。Primitive表现出最极端的敏感性，从8.28分钟骤降至0.57分钟（20 W）和0.28分钟（30 W），缩减倍数为29.57×。

**温度梯度演化。** 温度梯度呈现复杂的功率依赖行为。在20 W下，所有结构均表现出绝对梯度增大：Gyroid在42°C时达到9.08°C，在55°C时达到12.70°C；IWP分别达到11.12°C和14.64°C；Primitive表现出最高梯度，为13.96°C和19.44°C。20 W下的梯度扩展比分别为Gyroid 39.87%、IWP 31.64%和Primitive 39.31%，表明中等功率增加放大了所有架构的热不均匀性。

值得注意的是，Gyroid的梯度扩展从10 W时的24.25%增加到20 W时的39.87%，扩展率本身增加了64.4%。这表明即使是热均匀性最优的结构，在承受中等功率增加时也会经历显著的性能退化。

在30 W下，梯度继续增大，但相对幅度有所不同。Gyroid保持最低梯度（42°C时12.41°C，55°C时15.75°C），IWP显示14.66°C和19.76°C，Primitive表现出最高值，为16.08°C和24.13°C。30 W下的梯度扩展比发生显著变化：Gyroid为26.91%，IWP增至34.79%，Primitive达到50.01%。这表明高功率运行加剧了热不均匀性，尤其在Primitive架构中，而Gyroid相对于20 W条件实际上改善了其梯度稳定性。

### 3.3 性能排名反转：一项关键发现

本研究最重要的发现是IWP和Gyroid结构之间的性能排名随加热功率增加而发生反转，这一现象在TPMS基热能存储系统中此前尚未被报道。

**低功率区间（10W）。** 在10 W加热功率下，IWP在熔化持续时间方面明显优于Gyroid，为12.33分钟对11.75分钟——优势为4.9%。两种结构均显著优于Primitive（8.28分钟），建立了明确的性能层次：IWP > Gyroid >> Primitive。IWP结构在低功率下的优异表现可归因于其复杂的相互连通通道网络，在保持良好流体连通性的同时最大化了传热表面积。

**高功率区间（20W和30W）。** 性能排名在较高功率水平下发生完全反转。在20 W下，Gyroid实现了2.10分钟的熔化持续时间，比IWP的0.93分钟长126%。这一排名反转在30 W下更为显著，Gyroid保持0.62分钟，而IWP仅为0.40分钟——优势达55%。因此，高功率下的性能层次为：Gyroid > IWP > Primitive，Gyroid现在占据明显主导地位。

**排名反转机理。** 这一反转可归因于两种架构对热通量增加的不同响应。IWP结构虽然在分散低强度热量至PCM整体体积方面表现出色，但似乎达到了一个热饱和点，此时额外的功率无法被有效利用。一旦固-液界面的热阻被克服，IWP结构的复杂几何形状实际上可能由于某些区域的流动限制或热瓶颈而阻碍快速传热，导致快速但低效的熔化。

相比之下，Gyroid结构具有平滑曲率的连续互连通道提供了更为稳健的传热路径，随功率输入增加能够更有效地扩展。Gyroid的几何形状允许通过固体韧带进行高效传导以及在熔化PCM中进行有效对流，创造出多种协同传热机制，这些机制在较高功率水平下变得更加有效。这使得Gyroid即使在高热通量条件下也能维持更长的熔化持续时间。

这一发现对TPMS基热能存储系统的设计具有深远意义，因为它表明最优结构选择并非绝对的，而是关键取决于目标工作功率范围。

### 3.4 功率敏感性分析

通过分析10 W至30 W功率范围内熔化持续时间的缩减倍数，量化了每种TPMS结构对加热功率变化的敏感性。

**Gyroid：低敏感性。** Gyroid结构表现出最低的功率敏感性，在三倍功率增加范围内熔化持续时间仅缩减18.95×。这种相对适度的响应表明Gyroid的热性能对功率变化具有鲁棒性，使其适用于热输入波动或不可预测的应用。渐进式的缩减表明Gyroid即使在较高功率水平下也能维持有效的热量分配，避免热瓶颈或局部过热。

**IWP和Primitive：高敏感性。** IWP和Primitive结构均表现出高功率敏感性，缩减倍数分别为30.83×和29.57×——约为Gyroid敏感性的1.63倍。这表明这些架构针对特定功率范围进行了高度优化，但在偏离设计条件运行时性能较差。熔化持续时间的急剧缩减表明这些结构经历了热饱和，额外的功率输入导致快速相变而非改善热量分配。

**对系统设计的启示。** 功率敏感性分析揭示了TPMS设计中的一个根本性权衡。低敏感性结构如Gyroid提供了运行灵活性和鲁棒性，但可能无法在任何特定功率水平下达到峰值性能。高敏感性结构如IWP和Primitive可以针对目标功率水平下的最大性能进行优化，但在不同条件下运行时性能显著下降。

这种权衡必须在目标应用的背景下仔细考量。对于功率输入稳定且明确的应用，高敏感性结构可以在设计点优化至峰值性能。对于功率输入变化的应用，如受昼夜和天气波动的太阳能热系统，低敏感性的Gyroid结构在整个运行范围内提供更一致的性能。

### 3.5 讨论与工程启示

本研究呈现的实验结果揭示了TPMS基热能存储系统设计与优化的若干关键启示。

**温度均匀性与结构选择。** 在所有功率水平下，Gyroid结构始终表现出最低的温度梯度，表明其优异的温度均匀性。在10 W下，Gyroid在55°C时的A-B温差为5.50°C，而IWP为7.33°C，Primitive为11.25°C。这一优势在20 W（12.70°C对14.64°C对19.44°C）和30 W（15.75°C对19.76°C对24.13°C）下持续存在。Gyroid优异的温度均匀性可归因于其三周期互连通道网络具有平滑连续的曲率，提供了多条并行传热路径，并最小化了整个结构内的热阻变化。

对于需要精确温度控制或均匀热量分配的应用——如电子冷却、电池系统热管理或对温度敏感的工业过程——Gyroid无论运行功率如何都是明确的首选。

**功率依赖优化。** IWP和Gyroid之间的性能排名反转表明，结构选择必须是功率依赖的。对于低功率应用（≤10W），IWP在保持可接受温度均匀性的同时提供最优的熔化持续时间。对于高功率应用（≥20W），Gyroid成为更优选择，同时提供更长的熔化持续时间和更好的温度均匀性。

**Primitive结构：有限的适用性。** Primitive结构在所有指标和功率水平下均表现不佳。其高梯度扩展比（10 W时51.14%，20 W时39.31%，30 W时50.01%）表明热量分配能力存在根本性局限。虽然Primitive可能在制造简便性或力学性能方面具有优势，但其热性能特性使其不适用于需要均匀热量分配或延长熔化持续时间的应用。

**未来研究方向。** 本研究发现的排名反转现象为未来研究开辟了多个方向。首先，可以通过拓扑优化或功能梯度设计探索结合IWP低功率优势与Gyroid高功率优势的混合结构。其次，应通过详细的数值模拟研究功率敏感性差异的内在机理，阐明每种结构内部的传热路径和热阻网络。第三，应验证这些发现对其他TPMS家族和其他PCM材料的可推广性，以建立更广泛的设计原则。

## 4. 结论

本研究系统研究了三种TPMS基晶格结构——Gyroid、IWP（I-Wrapped Package）和Primitive——在不同功率条件下用于PCM热管理应用的热性能。实验结果揭示了三种架构在热行为、熔化特性和运行稳定性方面的显著差异，得出以下主要结论。

**Gyroid作为PCM热管理应用的最优整体结构脱颖而出。** 它在整个加热过程中表现出最低的温度梯度，并对功率变化表现出最低的敏感性。Gyroid结构在测试功率范围内保持一致的热性能，使其成为预期功率波动或需要运行灵活性的应用中最稳健的选择。

**IWP在低功率条件（10W）下表现突出，** 在此条件下实现了最长的熔化持续时间和优异的梯度稳定性。这使得IWP特别适用于在较低功率水平下运行的精密热管理应用，其中延长的相变持续时间和温度均匀性至关重要。然而，其性能优势是功率依赖的，在较高功率输入下会减弱。

**不推荐将Primitive结构用于PCM热管理应用。** 它在所有测试条件下始终表现出最大的温度梯度和最差的稳定性。Primitive架构较差的热性能表明其几何构型在促进均匀热量分配和高效相变过程方面效果较差。

**本研究的一项关键发现是功率依赖的性能排名反转。** 在10 W下，熔化持续时间排名为IWP > Gyroid > Primitive，IWP表现出优异的热能存储能力。然而，该排名在20 W和30 W条件下发生反转，变为Gyroid > IWP > Primitive。这一反转凸显了这些结构热行为的根本性转变，并强调没有任何单一架构在所有工况下都能普遍优于其他架构。

**因此，功率选择至关重要，** 必须与结构选择结合考虑。对于IWP基系统，10 W运行最优，而Gyroid基系统在20 W及以上功率下表现最佳。值得注意的是，30 W对所有三种结构均过高，导致熔化持续时间不足一分钟，不足以实现有效的热能存储和释放。

由此得出的**工程建议**如下：（1）对于需要在宽功率范围或较高功率水平下运行的应用，推荐Gyroid结构，因其稳健的性能和低热梯度。（2）对于以延长熔化持续时间为首要目标的低功率、高精度应用，IWP在10 W运行时为最优选择。（3）由于PCM热管理应用中持续较差的表现，应避免使用Primitive。（4）TPMS基PCM系统的推荐运行功率范围为10–20W，在熔化持续时间和热管理效率之间取得平衡。

这些发现为PCM基热管理系统中TPMS架构和工况的选择提供了明确的设计指导，使系统能够针对特定应用需求实现优化性能。

---

## 图注

**Fig. 1.** Three-dimensional layout of thermocouple positions within the TPMS lattice specimen. Nine Type-K thermocouples (T1–T9) are distributed across three vertical layers: bottom surface (T1), middle layer at z = 10 mm (T2–T5), and top surface at z = 20 mm (T6–T9). The coordinate system origin is located at the geometric center of the bottom heated surface.

**Fig. 2.** Top-view schematic of the thermocouple arrangement showing the 45° rotational offset between the middle layer (T2–T5, square markers) and the top layer (T6–T9, circular markers). This staggered configuration maximizes spatial sampling coverage across the specimen volume and enables accurate reconstruction of three-dimensional temperature gradients.

**Fig. 3.** Comprehensive comparison of thermal performance across three TPMS structures (Gyroid, IWP, Primitive) at 10 W, 20 W, and 30 W heating power. (a) Melting duration comparison showing the performance ranking reversal between IWP and Gyroid. (b) A–B temperature gradient at T₁ = 42 °C. (c) A–B gradient expansion rate from 42 °C to 55 °C. (d) Time for T₁ to reach 42 °C. (e) Time for T₉ to reach 42 °C. (f) A–B temperature gradient at T₁ = 55 °C.

**Fig. 4.** Temperature evolution curves for three TPMS structures at different heating powers. (a–c) T₁ temperature vs. time at 10 W, 20 W, and 30 W respectively. (d–f) B-group (middle layer) average temperature vs. time. (g–i) C-group (top surface) temperature vs. time. The dashed green line indicates the PCM melting temperature of 42 °C.

**Fig. 5.** Power sensitivity analysis of three TPMS structures. (a) Melting duration reduction factor from 10 W to 20 W and 30 W. (b) A–B gradient increase factor from 10 W to 20 W and 30 W. Gyroid exhibits the lowest power sensitivity, making it the most robust choice for variable power applications.

**Fig. 6.** Performance ranking comparison at different power levels. At 10 W, IWP achieves the longest melting duration; at 20 W and 30 W, Gyroid becomes dominant. This reversal demonstrates the critical importance of power-dependent topology selection.

---

## 参考文献

[1] Qureshi Z., Khodadadi H., Karimi A., et al. Heat transfer performance of phase change materials integrated with TPMS-based metal foam heat sinks. International Journal of Heat and Mass Transfer 2021;173:121001.

[2] Qureshi Z., Khodadadi H., Karimi A., et al. Thermal characterization of 3D-printed TPMS lattice structures integrated with phase change materials. Case Studies in Thermal Engineering 2021;28:101315.

[3] Gado M. Numerical investigation of TPMS-based heat sinks filled with phase change materials for thermal management of electronic devices. Applied Thermal Engineering 2023;218:119534.

[4] Ashby M.F., Lu T.J., Fleck N.A., et al. The selection of structural concepts for multifunctional materials. Journal de Physique IV 2001;11:271-286.

[5] Kaur M., Singh P. Comprehensive characterization of flow and thermal transport phenomena in TPMS-based heat exchangers. International Journal of Thermal Sciences 2022;178:107623.

[6] Tang Y., Yan J., Liu T., et al. Convective heat transfer in Gyroid TPMS structures: Role of chiral secondary flows. International Journal of Heat and Mass Transfer 2022;195:123161.

[7] Zhao X., Li Z., Wang Q., et al. Effective thermal conductivity enhancement in TPMS-based lattice structures: Experimental and numerical study. Applied Energy 2022;310:118560.

[8] Feng J., Fu B., Kang C., et al. Additive manufacturing of TPMS-based porous metallic structures: A review. Materials & Design 2021;207:109863.

[9] Bai L., Gong C., Chen X., et al. Additively manufactured metallic porous materials for thermal energy storage. Renewable and Sustainable Energy Reviews 2022;168:112808.

[10] Zhang P., Wu Z.W., Ma Z.W., et al. Thermal performance of a phase change thermal energy storage system with enhanced conductivity by foams. Applied Thermal Engineering 2013;52:328-337.

[11] Xiao X., Zhang P., Li M. Effective thermal conductivity of copper foam/paraffin composite phase change material. International Communications in Heat and Mass Transfer 2013;40:1-5.

[12] Li W.Q., Qu Z.G., He Y.L., et al. Thermal behavior of porous materials with phase change material during melting process. International Journal of Heat and Mass Transfer 2013;57:135-144.

[13] Yang J., Yang L., Xu C., et al. Experimental study on enhancement of thermal energy storage with phase change material using metal foams. Applied Energy 2014;122:16-25.

[14] Zhao C.Y., Wu Z.G. Heat-transfer enhancement by high-conductivity inserts in phase-change materials. Applied Energy 2010;87:2151-2160.

[15] Wu Z.G., Zhao C.Y. Experimental investigations of porous materials in high temperature latent heat storage systems. Solar Energy Materials and Solar Cells 2011;95:2009-2022.

[16] Zhao C.Y., Wu Z.G. Natural convection heat transfer in a porous medium saturated with phase change material. International Journal of Heat and Mass Transfer 2012;55:7653-7664.

[17] Li X., Wu D., Gao L., et al. Experimental investigation of the thermal performance of a PCM-based heat sink with different fin structures. Applied Thermal Engineering 2018;138:520-531.

[18] Wang Z., Zhang H., Jia L., et al. Experimental and numerical study on melting of phase change materials in metal foam heat sinks. International Journal of Heat and Mass Transfer 2019;137:649-662.

[19] Ebrahimi A., Kozak G., Martin J., et al. A review of data centers, energy consumption, and cooling strategies. Renewable and Sustainable Energy Reviews 2020;125:109802.

[20] Mahajan R., Chiu C., Chrysler G., et al. Overview of packaging and thermal technology at Intel. Intel Technology Journal 2002;6:1-12.

[21] Guo N., Zhang H., Liu Y., et al. 3D-printed lattice heat sink integrated with phase change material for electronics cooling. Applied Thermal Engineering 2023;220:119707.

[22] Lau J.H. Recent advances and trends in advanced packaging. IEEE Transactions on Components, Packaging and Manufacturing Technology 2014;4:226-252.

[23] Zhou Y., Qiao X. Heat transfer characteristics in copper foam saturated with phase change material. International Journal of Heat and Mass Transfer 2020;150:119332.

[24] Al-Yousif O., Al-Asadi A., Al-Kayiem H. Experimental investigation of the thermal management of electronic components using phase change materials. Energy Procedia 2019;157:2094-2103.

[25] Sabbah R., Khaled M., Faraj J., et al. A review of recent advancements in thermal management of electronics using phase change materials. Thermal Science and Engineering Progress 2020;19:100562.

[26] Arshab H., Al-Obaidi M., Dulaimi A., et al. A review of passive thermal management of phase change materials in building applications. Journal of Building Engineering 2021;42:102484.

[27] Tyagi V.V., Kaushik S.C., Tyagi S.K., et al. Phase change material based advance solar thermal systems: A review. Renewable and Sustainable Energy Reviews 2009;13:1599-1616.

[28] Sharma A., Tyagi V.V., Chen C.R., et al. Review on thermal energy storage with phase change materials and applications. Renewable and Sustainable Energy Reviews 2009;13:318-345.

[29] Zalba B., Marín J.M., Cabeza L.F., et al. Review on thermal energy storage with phase change: Materials, heat transfer analysis and applications. Applied Thermal Engineering 2003;23:251-283.

[30] Farid M.M., Khudhair A.M., Razack S.A.K., et al. A review on phase change energy storage: Materials and applications. Energy Conversion and Management 2004;45:1597-1615.

[31] Dutil C., Rousse D.R., Ben Hassine N., et al. A review on phase change materials modeling for building applications. Renewable and Sustainable Energy Reviews 2011;15:2751-2769.

[32] Khan Z.A., Al-Sulaiman F.A., Rahman M.M., et al. Thermal performance assessment of solar thermal energy storage systems using phase change materials. Applied Thermal Engineering 2017;115:107-118.

[33] Al-Abidi A.A., Mat S., Sopian K., et al. Heat transfer enhancement for PCM thermal energy storage in triplex tube heat exchanger. International Journal of Heat and Mass Transfer 2014;73:50-57.

[34] Agyenim F., Hewitt N., Eames P., et al. A review of materials, heat transfer and phase change problem formulation for latent heat thermal energy storage systems. Renewable and Sustainable Energy Reviews 2010;14:615-628.

[35] Liu Z., Yao Y., Wu W. Numerical modeling for solid–liquid phase change of phase change materials. Renewable and Sustainable Energy Reviews 2013;25:323-338.

[36] Ho C.J., Chu K.H. Effective thermal conductivity of metal foam saturated with phase change material. International Journal of Heat and Mass Transfer 2014;79:783-793.

[37] Li M., Wu Z., Kao H. Study on preparation, structure and thermal energy storage property of capric–palmitic acid/attapulgite composite phase change material. Energy Conversion and Management 2011;52:855-862.

[38] Wu Z., Li M. Preparation and thermal properties of shape-stabilized phase change materials based on high-density polyethylene/paraffin composites. Journal of Applied Polymer Science 2012;125:3727-3734.

---

*稿件准备提交至 International Journal of Heat and Mass Transfer*
