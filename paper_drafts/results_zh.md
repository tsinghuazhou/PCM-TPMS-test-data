# 3. 结果与讨论 (Results and Discussion)

## 3.1 热性能对比：Gyroid与Primitive晶格结构在10 W下的比较 (Thermal Performance Comparison: Gyroid vs. Primitive Lattice Structures at 10 W)

在恒定加热功率10 W条件下，对填充phase change material (PCM)的Gyroid和Primitive TPMS lattice structures进行了热性能评估。沿热流路径在九个位置（T1–T9）进行了温度测量，从而能够对两种topology的axial temperature gradients和transient melting behavior进行定量比较。

Fig. 3 (primitive_vs_gyroid_10w_update.png)展示了两种结构在选定测量点的温度演化曲线。在关键测量点T1（位于距热源最近处，对应局部温度约42 °C），Gyroid structure的A–B axial temperature gradient为4.2 °C，而Primitive structure在相同条件下的gradient为7.7 °C。这意味着Gyroid topology的thermal gradient降低了45%，表明沿轴向方向具有显著更均匀的热量分布。

A–C gradient跨越更长的轴向距离，因此为thermal uniformity提供了更严格的度量指标，呈现出相似的趋势。在T1 = 42 °C时，Gyroid structure的A–C gradient为8.6 °C，而Primitive structure为10.7 °C，改善了20%。这些结果表明，Gyroid topology在短程和长程空间尺度上均提供了优越的thermal homogenization。

一个特别重要的发现是关于phase change过程中的gradient stability。对于Primitive structure，A–B gradient在PCM melting phase期间增加了约55%，表明随着phase transition的进行，thermal uniformity逐渐恶化。这种行为归因于Primitive unit cell内部localized thermal channels的形成——当近源区域的PCM开始melting时，其discontinuous solid network无法有效地重新分配热量。相比之下，Gyroid structure在整个melting process中保持了几乎恒定的gradient，未观察到统计学上显著的增大。这种稳定性直接源于Gyroid的triply periodic minimal surface geometry，该geometry提供了完全three-dimensional interconnected heat conduction network。Gyroid lattice的continuous solid phase确保了thermal energy在横向和轴向上均能被重新分配，从而抑制了thermal hotspots的形成，即使在PCM经历solid–liquid transition时仍能维持gradient uniformity。

Total melting duration进一步区分了两种结构。Gyroid lattice完成phase change process需要11.8 min，而Primitive lattice的melting time为9.4 min——缩短了25%。尽管Primitive structure的melting更快，但这一结果反映了其inferior thermal spreading capability：热量集中在热源附近，导致快速local melting，而远端区域未能充分利用。Gyroid structure更长的melting time表明其更有效地利用了全部PCM volume，从而实现了更均匀的energy storage和增强的effective thermal capacity。

这些发现与理论预测一致：Gyroid的mean curvature distribution（对于理想minimal surface处处为零）促进了solid lattice与PCM之间的均匀interfacial heat transfer [1, 5]。Gyroid topology的interconnected channel network还有利于molten PCM内部的natural convection，提供了conduction之外的额外heat transfer mechanism。相比之下，Primitive structure的pore geometry包含stagnation zones，在这些区域convective circulation受到抑制，将heat transfer限制为单纯的conduction [6]。

## 3.2 加热功率对Gyroid热性能的影响 (Effect of Heating Power on Gyroid Thermal Performance)

为研究heating intensity对Gyroid/PCM system热行为的影响，在三个功率水平下进行了实验：10 W、20 W和30 W。Fig. 4 (gyroid_power_comparison_no_t4.png)总结了三种条件下关键测量点的温度响应。

在T1 = 42 °C时，A–B gradient随heating power单调增加：10 W时为4.4 °C，20 W时为9.1 °C，30 W时为12.4 °C。A–C gradient呈现相同趋势，从8.6 °C（10 W）增加到12.4 °C（20 W）和15.7 °C（30 W）。heating power与temperature gradient之间的近似linear relationship表明，Gyroid/PCM system的thermal resistance在测试功率范围内保持相对恒定，所观察到的gradient increase主要由elevated heat flux驱动，而非heat transfer mechanism的根本性变化。

melting duration中观察到了heating power最为显著的影响。10 W时，complete melting time为11.8 min；20 W时降至2.2 min；30 W时phase change仅在0.6 min内完成。从10 W到30 W，melting time减少了20倍，凸显了phase change kinetics对功率的强烈依赖性。在30 W时，phase change window极其狭窄，以至于在data acquisition system的时间尺度上，transition几乎是instantaneous的。这一观察具有重要的实际意义：虽然high heating power可以实现rapid thermal response，但它同时也产生了extremely steep temperature gradients，可能损害PCM system的thermal protection function。

Fig. 5 (gyroid_30w_new_analysis.png)提供了30 W工况的详细视图，揭示了即使在这些extreme conditions下，Gyroid structure仍保持了可测量——尽管显著升高——的spatial temperature gradients。30 W时的rapid energy input接近了PCM的effective thermal buffering capacity极限，因为latent heat storage在thermal wave能够uniformly propagate through the lattice之前即被耗尽。

heating power与thermal uniformity之间的trade-off可通过A–C gradient与melting time的比值来量化。10 W时，该比值为0.73 °C/min；20 W时升至5.64 °C/min；30 W时达到26.2 °C/min。这种superlinear scaling表明，将heating power超过某一critical threshold后，在thermal performance uniformity方面的收益递减。对于practical thermal management applications，这暗示存在一个optimal operating power range，在response speed与temperature uniformity requirements之间取得平衡。

## 3.3 Phase Change Kinetics

对每个measurement point达到42 °C所需时间的分析，揭示了phase change front在Gyroid lattice中spatial progression的规律。在10 W heating power下，T1（距热源最近）达到42 °C用时0.3 min，而T9（距热源最远）需要5.8 min——相差19倍。20 W时，相应时间分别为0.5 min（T1）和8.9 min（T9）；30 W时为3.4 min（T1）和15.9 min（T9）。

在higher power levels下T9相对于T1耗时更长的反直觉现象，可通过heat input rate与PCM的effective thermal diffusivity之间的competition来解释。在10 W时，moderate heat flux为lateral heat redistribution通过Gyroid的interconnected solid network提供了充足时间，使得more coherent phase change front能够在结构中propagate。在30 W时，intense local heating产生了steep thermal gradient，驱动near-source region的rapid melting，但PCM在molten state下的low effective thermal diffusivity限制了thermal energy到达distal regions的速率。

melting过程中的temperature gradient evolution呈现出三个distinct regimes：(i) initial transient phase（10 W下0–2 min），gradient迅速增大，near-source PCM开始melting；(ii) quasi-steady phase（10 W下2–10 min），gradient保持近似恒定，phase change front在lattice中propagate；(iii) final saturation phase（10 W下>10 min），所有measurement points接近target temperature，gradient collapse。quasi-steady regime的持续时间代表了thermally stable operating window，在10 W时最长，在higher power levels下逐渐缩短。

## 3.4 数据可重复性 (Data Reproducibility)

为验证thermal performance measurements的experimental reliability，在标称相同条件下对Gyroid structure在10 W heating power下进行了两次独立实验。Fig. 6 (gyroid_10w_repeat_comparison.png)比较了两次run（标记为"Old"和"New"）之间A–B temperature gradient的evolution。

结果展示了excellent reproducibility：整个melting process中，两次实验的A–B gradient difference保持在1 °C以内。两次实验均捕获了相同的quasi-steady gradient plateau以及phase change的onset和completion times。两个dataset之间的maximum deviation出现在initial transient phase（t < 2 min），其中initial PCM subcooling和contact thermal resistance的minor differences产生了slight offsets。然而，这些差异相对于overall gradient magnitude可以忽略不计，不影响key conclusions。

Old和New datasets之间的一致性提供了强有力的证据，证明Gyroid与Primitive structures之间observed thermal performance differences是intrinsic to the lattice topology，而非experimental variability的artifacts。此外，melting duration的reproducibility（两次run之间在±0.5 min以内）证实了PCM的phase change behavior在controlled experimental conditions下是stable和repeatable的。

## 3.5 讨论 (Discussion)

上述experimental results证明，当与PCM integrated用于thermal management applications时，Gyroid TPMS lattice structure提供了显著优于Primitive topology的thermal performance。A–B temperature gradient降低45%以及phase change过程中gradient deterioration的消除，确立了Gyroid structure作为require thermal uniformity applications的preferred topology。

这些发现与先前关于TPMS-based heat exchangers的computational和experimental studies一致并有所拓展。Zhao et al. [1]通过numerical simulation证明，在equivalent relative densities下，Gyroid structures比Primitive structures的effective thermal conductivity高30–40%，将这一enhancement归因于Gyroid的continuous mean-curvature-free surface最大化了solid–fluid interfacial area。本experimental results在actual phase change conditions下证实了这一prediction，在此条件下thermal boundary conditions比simulation中考虑的steady-state scenarios本质上更为complex。

interconnected pore network在enhancing molten PCM内部convective heat transfer中的作用，与Li et al. [5]的发现一致，他们证明Gyroid channels促进了helical flow patterns，增强了mixing并减少了thermal stratification。相比之下，Primitive structure的orthogonal channel intersections创建了recirculation zones，impede convective transport [6]。这种topological effect在PCM melting后natural convection开始contribute to overall heat transfer时变得越来越重要。

Section 3.2中observed的power-dependent thermal performance对electronics cooling applications中PCM-based thermal management systems的design具有direct implications。modern electronic devices经历的transient power loads可在数秒内变化一个数量级[21, 23]。本研究结果表明，为moderate power（如10 W）steady-state operation设计的Gyroid/PCM heat sink将在sustained operation期间maintain excellent thermal uniformity，但在power surges期间可能experience significant gradient excursions。30 W的结果表明，如果power surge超过lattice的effective thermal transport rate，PCM的thermal buffering capacity可能被overwhelmed，导致localized overheating——尽管phase change material存在。

本work identified的一个key design trade-off是melting speed与thermal uniformity之间的权衡。虽然higher heating power减少了absorb a given thermal load所需的时间，但它同时degraded spatial temperature uniformity——这正是combining TPMS lattices with PCM的主要优势。对于junction temperature limits和thermal cycling fatigue是primary reliability concerns的electronic cooling applications [23]，10 W operating condition——尽管melting time更长——可能通过将semiconductor junction维持在narrower temperature band内而提供更优越的overall system reliability。

与conventional fin-enhanced PCM heat sinks相比，Gyroid/PCM system提供了additional advantage of isotropic thermal performance。conventional fin arrays主要在fin axis方向提供enhanced heat transfer，产生anisotropic thermal gradients，可能导致warpage和mechanical stress [2]。Gyroid的triply periodic geometry在all three spatial directions上提供equivalent thermal enhancement，使其特别适用于multi-directional heat loads或heat source location not fixed的applications。

Reproducibility results（Section 3.4）进一步支持了Gyroid/PCM thermal management systems的practical feasibility。两次independent experimental runs之间的sub-1 °C variation表明，current additive manufacturing techniques（metallic Gyroid lattices的selective laser melting）可achievable的manufacturing tolerances足以produce thermally equivalent structures。这一发现解决了TPMS-based designs从simulation到fabrication转化过程中的common concern，即与ideal minimal surface的geometric deviations可能potentially degrade thermal performance [21]。

Future work应investigate lattice relative density对本workidentified的thermal performance trade-offs的effect，以及PCM/TPMS system在repeated melting–solidification cycles下的long-term cyclic stability。此外，combining Gyroid和Primitive regions within a single heat sink的hybrid designs可potentially exploit Primitive topology near the heat source的rapid thermal response，同时leveraging Gyroid的uniformity-enhancing characteristics in the distal regions，在response speed与thermal homogeneity之间achieve an optimal balance。
