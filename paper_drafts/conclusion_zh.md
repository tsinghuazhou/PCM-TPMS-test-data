# 5. 结论

本研究首次对 Gyroid 和 Primitive 两种 TPMS 晶格结构与 phase change materials 复合后的热性能进行了系统性实验对比研究。采用增材制造 AlSiMg 金属晶格骨架（50 × 50 × 20 mm³），填充石蜡基 PCM（T_m = 42 °C），在 10 W、20 W 和 30 W 恒定加热功率下开展实验。通过在三个垂直层布置九个 thermocouple，实现了对相变过程中沿厚度方向 temperature gradient 的定量评估。主要研究结论如下。

第一，Gyroid topology 在抑制空间 temperature gradient 方面展现出显著优势。在 10 W 加热条件下，Gyroid 结构的底面-中层 gradient（A–B）在整个 phase change window 内比 Primitive 结构低 40–50%（T₁ = 42 °C 时分别为 4.2 °C 和 7.7 °C）。更为关键的是，Primitive 晶格在熔化过程中 gradient 恶化幅度达 55%（A–B 从 7.7 °C 增至 11.9 °C），而 Gyroid 结构表现出优异的 gradient 稳定性，A–B 在整个熔化过程中波动不超过 ±1 °C。这一行为归因于 Gyroid 的三重连通、曲率连续的 channel network，即使 PCM 转变为低 thermal conductivity 的液相后，仍能维持高效的热量分布。

第二，input power 对 thermal performance 的影响显著且呈非线性特征。在 Gyroid 构型中，加热功率从 10 W 增加至 30 W 使 A–B gradient 增大了 2.8 倍（T₁ = 42 °C 时从 4.4 °C 升至 12.4 °C）。与此同时，melting duration 缩短了约 20 倍（从 11.8 min 降至 0.6 min），表明过高的加热功率会严重削弱 PCM 均匀吸热的能力。该发现揭示了 charging speed 与 thermal uniformity 之间的根本性 trade-off，在 system design 中必须予以考虑。

第三，通过相同条件下的重复实验严格验证了 experimental reproducibility。Gyroid 10 W 构型经两次独立样品制备与测试，A–B gradient 差异小于 1 °C，melting duration 偏差不超过 0.3 min。这一一致性证实了 measurement methodology 的可靠性以及所观察到的 topology 效应的稳健性。

本研究的 practical implications 具有直接指导意义。对于要求空间 uniform thermal management 的应用场景——如 electronics cooling 和 battery thermal regulation——强烈建议采用 Gyroid topology 而非 Primitive 构型。系统设计者应根据可接受的 gradient 水平选择合适的 heating power，以平衡 charging rate，本研究数据为此优化提供了定量依据。

未来工作将从以下几个方面推进。基于重构 TPMS geometry 的 numerical simulation 有待开展，以阐明 local heat transfer mechanisms 并验证实验观测结果。应开展 TPMS geometry 的参数化优化——包括 wall thickness、unit cell size 和 hybrid configurations——以针对特定应用定制性能。需要进行 long-term thermal cycling tests，以评估 PCM–lattice 相互作用在反复 charge–discharge cycles 中的耐久性。最后，将 TPMS–PCM 结构与 active cooling systems 相集成，是实现 rapid heat dissipation 与 sustained thermal regulation 的有前景的研究方向。
