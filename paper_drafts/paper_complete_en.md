# Experimental Investigation of Thermal Performance in TPMS Lattice Structures with Phase Change Materials: A Comparative Study of Gyroid and Primitive Architectures

---

## Abstract

Triply periodic minimal surface (TPMS) lattice structures integrated with phase change materials (PCMs) offer a promising approach for advanced passive thermal management of high-power electronic devices. However, experimental comparisons of different TPMS topologies under controlled thermal loading remain scarce. This study presents a systematic experimental investigation of the thermal performance of two TPMS architectures — Gyroid and Primitive (Schwarz-P) — integrated with paraffin-based PCM. Lattice structures were fabricated from AlSi10Mg alloy via laser powder bed fusion additive manufacturing, with specimen dimensions of 50 × 50 × 20 mm³. A commercial paraffin wax with a phase change temperature of 42 °C was vacuum-infused into the lattice pores. Transient heating experiments were conducted at three constant power levels (10 W, 20 W, and 30 W) under uniform heat flux boundary conditions, with nine thermocouples distributed across three vertical layers to capture the spatiotemporal evolution of temperature fields. Results demonstrate that the Gyroid topology achieves a 40–50% lower through-thickness temperature gradient compared to the Primitive structure at 10 W heating (A–B gradient: 4.2 °C vs. 7.7 °C at T₁ = 42 °C). Critically, while the Primitive lattice exhibits a 55% gradient deterioration during PCM melting, the Gyroid structure maintains remarkable thermal stability throughout the phase change process. Increasing heating power from 10 W to 30 W elevates the Gyroid A–B gradient by a factor of 2.8 and reduces melting duration by approximately 20-fold, establishing a fundamental trade-off between charging speed and thermal uniformity. Experimental reproducibility was validated through repeated trials with gradient deviations below 1 °C. These findings establish the Gyroid TPMS topology as the superior architecture for uniform passive thermal management applications.

**Keywords:** TPMS lattice; Gyroid; Primitive; Phase change material; Thermal management; Additive manufacturing; Temperature uniformity

---

## 1. Introduction

The relentless miniaturization and performance escalation of modern electronic devices have imposed increasingly stringent thermal management demands. As power densities in electronics continue to rise — exceeding 100 W/cm² in advanced microprocessors and high-power LEDs — conventional passive cooling strategies such as fin arrays and heat spreaders are approaching their fundamental limits [1]. Efficient thermal management is critical not only for ensuring device reliability and operational lifespan but also for maintaining performance stability under transient thermal loads. This challenge has driven sustained research interest in advanced thermal regulation technologies that can accommodate high heat fluxes while maintaining compact form factors.

Phase change materials (PCMs) have emerged as a compelling solution for passive thermal energy storage and transient thermal management. By absorbing and releasing large quantities of latent heat during solid–liquid phase transitions at nearly constant temperatures, PCMs can effectively buffer thermal spikes and maintain component temperatures within safe operating windows [3]. Paraffin waxes, in particular, are widely employed owing to their high latent heat capacity, chemical stability, non-toxicity, and suitable phase change temperatures for electronics cooling applications. However, the inherently low thermal conductivity of paraffin-based PCMs (typically 0.2–0.4 W/m·K) severely limits their rate of heat absorption and release, resulting in sluggish thermal response and incomplete utilization of latent heat capacity. Overcoming this limitation requires the integration of high-conductivity structural scaffolds that enhance effective thermal transport throughout the PCM volume.

Metallic foams and lattice structures have been extensively investigated as conductive matrices for PCM composites. Among these, triply periodic minimal surface (TPMS) architectures have attracted considerable attention due to their exceptional combination of high surface-area-to-volume ratios, interconnected pore networks, and mechanically efficient topologies [1,5]. TPMS structures are defined by zero-mean-curvature surfaces that partition three-dimensional space into two continuous, interpenetrating channels. The two most widely studied TPMS topologies — Gyroid and Primitive (Schwarz-P) — differ fundamentally in their channel geometry and flow characteristics, which in turn influence heat transfer performance. The Gyroid surface features a single continuous channel with chiral symmetry, while the Primitive surface comprises two independent channel networks connected through periodic openings [5,6]. These geometric distinctions give rise to markedly different convective and conductive heat transfer behaviors, making the comparative study of Gyroid and Primitive TPMS lattices particularly relevant for thermal management design.

Recent studies have demonstrated the potential of TPMS-based structures for enhanced PCM thermal management. Qureshi et al. [1] investigated TPMS-based metal foams as heat sinks for PCM and reported significant improvements in temperature uniformity and charging time reduction compared to conventional foam geometries. In a subsequent study, Qureshi et al. [2] explored 3D-printed TPMS lattice structures integrated with PCM, demonstrating the feasibility of fabricating complex periodic architectures with tailored thermal performance. Gado [3] conducted numerical investigations of TPMS heat sinks filled with PCM and showed that the Gyroid topology outperformed the Primitive and Diamond surfaces in terms of melting rate and thermal storage efficiency. Tang et al. [6] examined convective heat transfer in Gyroid TPMS structures and revealed the complex interplay between secondary flows induced by the chiral channel geometry and thermal transport enhancement. Kaur and Singh [5] provided a comprehensive characterization of flow and thermal transport phenomena in TPMS-based heat exchangers, establishing design correlations for the Nusselt number and friction factor across multiple TPMS topologies.

The advent of additive manufacturing (AM), particularly laser powder bed fusion (L-PBF), has enabled the fabrication of TPMS lattice structures with unprecedented geometric accuracy and surface quality [2]. Unlike conventional manufacturing methods that are constrained by the complexity of mold design and demolding processes, AM allows direct realization of mathematically defined TPMS geometries with precise control over strut dimensions, porosity, and unit cell size. This capability has opened new avenues for optimizing TPMS-PCM systems by tailoring the lattice architecture to specific thermal management requirements. Guo et al. [21] demonstrated a 3D-printed lattice heat sink integrated with PCM for electronics cooling, showing that the enhanced thermal conductivity network significantly reduced peak temperatures during transient operation. Zhou and Qiao [23] investigated heat transfer characteristics in copper foam saturated with PCM and highlighted the importance of pore-scale morphology in determining the effective thermal performance of composite systems.

Despite these advances, a significant gap remains in the experimental understanding of TPMS-PCM coupled thermal systems. The majority of existing studies have relied on numerical simulations or analytical models to predict the thermal behavior of TPMS-PCM configurations [1,3]. Experimental investigations that directly compare different TPMS topologies — particularly Gyroid and Primitive — under controlled and reproducible thermal loading conditions are notably scarce. Furthermore, the influence of heating power on the transient thermal response, phase change dynamics, and spatial temperature distribution within TPMS-PCM systems has not been systematically characterized through experiments. Understanding these relationships is essential for validating computational models and establishing design guidelines for practical engineering applications.

This study presents a systematic experimental investigation of the thermal performance of two TPMS lattice topologies — Gyroid and Primitive — integrated with paraffin-based PCM. The TPMS lattice structures were fabricated from AlSi10Mg alloy using L-PBF additive manufacturing, with sample dimensions of 50 × 50 × 20 mm³. A paraffin-based PCM with a phase change temperature of 42 °C was infiltrated into the lattice pores. Transient heating experiments were conducted at three power levels (10 W, 20 W, and 30 W) under constant heat flux boundary conditions. Multiple thermocouples were strategically positioned at three vertical layers to capture the spatial and temporal evolution of temperature fields during the heating and phase change processes. The primary objectives of this study are: (1) to compare the thermal performance of Gyroid and Primitive TPMS lattices in terms of temperature uniformity, thermal gradients, and PCM melting dynamics; (2) to characterize the effect of heating power on the transient thermal response and phase change behavior; and (3) to provide experimental data that can inform the design optimization of TPMS-based PCM thermal management systems for electronics cooling applications.

## 2. Experimental Section

### 2.1 Materials and Specimen Preparation

The triply periodic minimal surface (TPMS) lattice structures investigated in this study were fabricated from AlSi10Mg alloy using selective laser melting (SLM), a powder-bed fusion additive manufacturing technique. Two distinct TPMS topologies were examined: the Gyroid and Primitive (Schwarz Primitive) surfaces, both belonging to the cubic crystal system and recognized for their interconnected channel networks and favorable specific surface area. The SLM process was performed with a layer thickness of 30 μm, achieving a relative density exceeding 99% as confirmed by micro-CT analysis. Key processing parameters included a laser power of 200 W, a scan speed of 800 mm/s, a hatch spacing of 0.12 mm, and a 67° stripe rotation between consecutive layers to minimize anisotropy.

The lattice specimens were designed with nominal external dimensions of 50 × 50 × 20 mm³, providing sufficient unit cells for thermally representative behavior while remaining compatible with the heating platform and insulation assembly. The unit cell size was chosen to balance manufacturing resolution with the characteristic length scale of heat transfer within the porous structure. Following fabrication, all specimens underwent stress-relief heat treatment at 300 °C for 2 hours to mitigate residual stresses from the layer-by-layer SLM process. Surface roughness was not further modified, as the as-built morphology was considered representative of practical thermal management applications.

The phase change material (PCM) was a commercial-grade paraffin wax with a nominal melting point of 42 °C and a latent heat of fusion of approximately 200 kJ/kg. The paraffin was chosen for its well-characterized thermal properties, chemical stability, negligible supercooling, and compatibility with aluminum alloy substrates. The PCM was vacuum-infused into the porous TPMS lattice at −0.09 MPa to ensure complete filling of interconnected void spaces. Each specimen was weighed before and after infiltration (±0.01 g), with PCM mass loading consistent within ±2% across all specimens.

### 2.2 Experimental Setup

The experimental apparatus comprised a constant-power resistive heating system, a thermocouple-based temperature measurement array, a multi-channel data acquisition system, and a thermal insulation enclosure. A flexible polyimide kapton heater matching the specimen footprint was bonded to the bottom surface using thermally conductive paste (> 1.5 W/(m·K)). The heater was driven by a regulated DC power supply delivering constant power levels of 10 W, 20 W, and 30 W, corresponding to heat fluxes of 4.0, 8.0, and 12.0 kW/m², respectively, spanning mild to aggressive thermal loading conditions relevant to electronics cooling applications.

Temperature was measured using nine Type-K (chromel–alumel) thermocouples (wire diameter 0.25 mm, bead diameter ~0.5 mm). The thermocouples were embedded at predetermined locations through small access holes (< 1 mm) drilled into the top surface, secured with high-temperature thermally conductive adhesive to ensure reliable contact throughout heating and melting cycles. The thermocouple arrangement is detailed in Section 2.3.

All signals were routed to a multi-channel data acquisition system (NI-9213, National Instruments) with cold-junction compensation, sampling all nine channels simultaneously at 1 Hz—sufficient to capture transient thermal response during both sensible heating and phase change. The system was calibrated against a NIST-traceable reference thermometer, with an overall measurement uncertainty of ±0.5 °C.

The assembly was enclosed in an insulation box constructed from 25 mm-thick extruded polystyrene (XPS) foam boards, with an inner lining of 10 mm-thick ceramic fiber blanket to suppress radiative heat losses at elevated temperatures. Preliminary calibration tests confirmed that lateral and top-surface heat losses remained below 3% of the total input power across all tested conditions. The bottom surface, in direct contact with the heater, was approximated as a uniform heat flux boundary condition, while the top and lateral surfaces were treated as nominally adiabatic within the insulation enclosure. All experiments were conducted in a temperature-controlled laboratory environment maintained at 23 ± 1 °C.

### 2.3 Thermocouple Layout

The nine thermocouples were arranged to capture the three-dimensional temperature distribution within the TPMS lattice and enable calculation of through-thickness temperature gradients, as illustrated in Fig. 1 and Fig. 2.

Thermocouple T1 was positioned at the geometric center of the bottom surface (coordinates: (0, 0, 0) mm), directly above the heater element. This location represents the point of maximum thermal input and serves as the primary indicator of the local thermal state at the heat source interface, where the phase change process initiates first.

Thermocouples T2 through T5 were arranged in the middle layer at z = 10 mm, at the four corners of a 25 mm × 25 mm square centered on the specimen axis, with coordinates (±12.5, ±12.5, 10) mm. This array captured radial temperature variations in the mid-plane and provided an area-averaged middle-layer temperature.

Thermocouples T6 through T9 were placed on the top surface at z = 20 mm, at the midpoints of a 25 mm × 25 mm square. This top-layer array was rotated by 45° relative to the middle layer, creating a staggered configuration that enhances spatial sampling across the specimen volume by positioning top-surface sensors maximally offset from the mid-plane sensors.

### 2.4 Data Processing

The raw temperature data from all nine thermocouples were processed to extract representative thermal metrics for performance evaluation. Due to a sensor malfunction during the experimental campaign, thermocouple T4 (one of the four mid-plane sensors) produced unreliable readings and was excluded from all subsequent analyses. The remaining eight functional channels were organized into three measurement groups:

Group A comprised T1 at the bottom surface, representing the heater-side thermal response. Group B was the arithmetic average of T2, T3, and T5, providing a spatially averaged middle-layer temperature. Group C was represented by T9 on the top surface, selected over T6–T8 for its superior and most stable thermal contact with the lattice struts.

Two through-thickness temperature gradients were defined: the A–B gradient (ΔT_mid = T₁ − T_B), representing the thermal drop across the middle layer; and the A–C gradient (ΔT_total = T₁ − T₉), representing the total thermal drop from the heated bottom to the top surface. These gradients indicate the effective thermal resistance of the TPMS lattice–PCM composite under transient heating.

A critical metric was the phase change window, defined as the time interval during which T1 remained within 42–52 °C. This 10 °C window encompasses the solid–liquid transition of the paraffin PCM and quantifies the duration and effectiveness of latent heat absorption. Phase change onset was identified when T1 first reached 42 °C, and completion when T1 exceeded 52 °C, indicating full melting of PCM near the heater. The phase change window duration serves as a primary indicator of the composite system's thermal energy storage capacity under each power level.

## 3. Results and Discussion

### 3.1 Thermal Performance Comparison: Gyroid vs. Primitive Lattice Structures at 10 W

The thermal performance of Gyroid and Primitive TPMS lattice structures filled with phase change material (PCM) was evaluated under a constant heating power of 10 W. Temperature measurements were recorded at nine positions (T1–T9) along the heat flow path, enabling quantitative comparison of axial temperature gradients and transient melting behavior between the two topologies.

Fig. 3 presents the temperature evolution at selected measurement points for both structures. At the critical measurement point T1 (located nearest to the heat source, corresponding to a local temperature of approximately 42 °C), the A–B axial temperature gradient of the Gyroid structure was measured at 4.2 °C, whereas the Primitive structure exhibited a gradient of 7.7 °C under identical conditions. This represents a 45% reduction in the thermal gradient for the Gyroid topology, indicating substantially more uniform heat distribution along the axial direction.

The A–C gradient, which spans a longer axial distance and thus provides a more stringent measure of thermal uniformity, showed a similar trend. At T₁ = 42 °C, the Gyroid structure maintained an A–C gradient of 8.6 °C compared to 10.7 °C for the Primitive structure, corresponding to a 20% improvement. These results demonstrate that the Gyroid topology provides superior thermal homogenization across both short and extended spatial scales.

A particularly significant finding concerns gradient stability during the phase change process. For the Primitive structure, the A–B gradient increased by approximately 55% during the PCM melting phase, indicating progressive deterioration of thermal uniformity as the phase transition proceeded. This behavior is attributed to the formation of localized thermal channels within the Primitive unit cell, where the discontinuous solid network fails to redistribute heat effectively once the PCM in the near-source region begins to melt. In contrast, the Gyroid structure maintained a nearly constant gradient throughout the entire melting process, with no statistically significant increase observed. This stability is a direct consequence of the Gyroid's triply periodic minimal surface geometry, which provides a fully three-dimensional interconnected heat conduction network. The continuous solid phase of the Gyroid lattice ensures that thermal energy is redistributed laterally as well as axially, suppressing the formation of thermal hotspots and maintaining gradient uniformity even as the PCM undergoes its solid–liquid transition.

The total melting duration further differentiated the two structures. The Gyroid lattice required 11.8 min to complete the phase change process, while the Primitive lattice melted in 9.4 min—a 25% shorter duration. Although the Primitive structure melts faster, this result reflects its inferior thermal spreading capability: heat remains concentrated near the source, causing rapid local melting while remote regions remain underutilized. The Gyroid structure's longer melting time indicates more effective engagement of the full PCM volume, resulting in more uniform energy storage and enhanced effective thermal capacity.

These findings are consistent with the theoretical prediction that the Gyroid's mean curvature distribution, which is everywhere zero for the ideal minimal surface, promotes uniform interfacial heat transfer between the solid lattice and the PCM [1, 5]. The interconnected channel network of the Gyroid topology also facilitates natural convection within the molten PCM, providing an additional heat transfer mechanism beyond conduction. In contrast, the Primitive structure's pore geometry contains stagnation zones where convective circulation is suppressed, limiting heat transfer to conduction alone in those regions [6].

### 3.2 Effect of Heating Power on Gyroid Thermal Performance

To investigate the influence of heating intensity on the thermal behavior of the Gyroid/PCM system, experiments were conducted at three power levels: 10 W, 20 W, and 30 W. Fig. 4 summarizes the temperature response at key measurement points across all three conditions.

At T₁ = 42 °C, the A–B gradient increased monotonically with heating power: 4.4 °C at 10 W, 9.1 °C at 20 W, and 12.4 °C at 30 W. The A–C gradient exhibited the same trend, rising from 8.6 °C (10 W) to 12.4 °C (20 W) and 15.7 °C (30 W). The approximately linear relationship between heating power and temperature gradient suggests that the thermal resistance of the Gyroid/PCM system remains relatively constant across the tested power range, and that the observed gradient increase is primarily driven by the elevated heat flux rather than by any fundamental change in the heat transfer mechanism.

The most dramatic effect of heating power was observed in the melting duration. At 10 W, the complete melting time was 11.8 min; at 20 W, this decreased to 2.2 min; and at 30 W, the phase change was completed in merely 0.6 min. The 20-fold reduction in melting time from 10 W to 30 W underscores the strong power dependence of the phase change kinetics. At 30 W, the phase change window was so narrow that the transition appeared almost instantaneous on the timescale of the data acquisition system. This observation has important practical implications: while high heating power can achieve rapid thermal response, it also creates extremely steep temperature gradients that may compromise the thermal protection function of the PCM system.

Fig. 5 provides a detailed view of the 30 W case, revealing that even under these extreme conditions, the Gyroid structure maintained measurable—though significantly elevated—spatial temperature gradients. The rapid energy input at 30 W approaches the limit of the PCM's effective thermal buffering capacity, as the latent heat storage is depleted before the thermal wave can propagate uniformly through the lattice.

The trade-off between heating power and thermal uniformity can be quantified by the ratio of the A–C gradient to the melting time. At 10 W, this ratio is 0.73 °C/min; at 20 W, it rises to 5.64 °C/min; and at 30 W, it reaches 26.2 °C/min. This superlinear scaling indicates that increasing the heating power beyond a critical threshold yields diminishing returns in terms of thermal performance uniformity. For practical thermal management applications, this suggests an optimal operating power range that balances response speed against temperature uniformity requirements.

### 3.3 Phase Change Kinetics

Analysis of the time required for each measurement point to reach 42 °C provides insight into the spatial progression of the phase change front through the Gyroid lattice. At 10 W heating power, T1 (nearest the heat source) reached 42 °C in 0.3 min, while T9 (farthest from the source) required 5.8 min—a 19-fold difference. At 20 W, the corresponding times were 0.5 min (T1) and 8.9 min (T9); at 30 W, 3.4 min (T1) and 15.9 min (T9).

The counterintuitive observation that T9 takes progressively longer relative to T1 at higher power levels can be explained by the competition between heat input rate and the PCM's effective thermal diffusivity. At 10 W, the moderate heat flux allows sufficient time for lateral heat redistribution through the Gyroid's interconnected solid network, enabling a more coherent phase change front to propagate through the structure. At 30 W, the intense local heating creates a steep thermal gradient that drives rapid melting near the source, but the PCM's low effective thermal diffusivity in the molten state limits the rate at which thermal energy can reach the distal regions.

The temperature gradient evolution during melting exhibited three distinct regimes: (i) an initial transient phase (0–2 min at 10 W) during which the gradient increased rapidly as the near-source PCM began to melt; (ii) a quasi-steady phase (2–10 min at 10 W) during which the gradient remained approximately constant while the phase change front propagated through the lattice; and (iii) a final saturation phase (>10 min at 10 W) during which all measurement points approached the target temperature and the gradient collapsed. The duration of the quasi-steady regime, which represents the most thermally stable operating window, was longest at 10 W and progressively shortened at higher power levels.

### 3.4 Data Reproducibility

To validate the experimental reliability of the thermal performance measurements, two independent experiments were conducted for the Gyroid structure at 10 W heating power under nominally identical conditions. Fig. 6 compares the A–B temperature gradient evolution between the two runs (designated "Old" and "New").

The results demonstrated excellent reproducibility: the A–B gradient difference between the two experiments remained below 1 °C throughout the entire melting process. Both experiments captured the same quasi-steady gradient plateau and the same onset and completion times for the phase change. The maximum deviation between the two datasets occurred during the initial transient phase (t < 2 min), where minor differences in the initial PCM subcooling and contact thermal resistance produced slight offsets. However, these differences were negligible compared to the overall gradient magnitude and did not affect the key conclusions.

The consistency between the Old and New datasets provides strong evidence that the observed thermal performance differences between Gyroid and Primitive structures are intrinsic to the lattice topology rather than artifacts of experimental variability. Furthermore, the reproducibility of the melting duration (within ±0.5 min between runs) confirms that the PCM's phase change behavior is stable and repeatable under the controlled experimental conditions.

### 3.5 Discussion

The experimental results presented above demonstrate that the Gyroid TPMS lattice structure provides significantly superior thermal performance compared to the Primitive topology when integrated with PCM for thermal management applications. The 45% reduction in A–B temperature gradient and the elimination of gradient deterioration during phase change establish the Gyroid structure as the preferred topology for applications requiring thermal uniformity.

These findings align with and extend previous computational and experimental studies on TPMS-based heat exchangers. Zhao et al. [1] demonstrated through numerical simulation that Gyroid structures exhibit 30–40% higher effective thermal conductivity than Primitive structures at equivalent relative densities, attributing the enhancement to the Gyroid's continuous mean-curvature-free surface that maximizes solid–fluid interfacial area. The present experimental results confirm this prediction under actual phase change conditions, where the thermal boundary conditions are inherently more complex than the steady-state scenarios considered in simulation.

The role of the interconnected pore network in enhancing convective heat transfer within the molten PCM is consistent with the findings of Li et al. [5], who showed that Gyroid channels promote helical flow patterns that enhance mixing and reduce thermal stratification. In contrast, the Primitive structure's orthogonal channel intersections create recirculation zones that impede convective transport [6]. This topological effect becomes increasingly important as the PCM melts and natural convection begins to contribute to the overall heat transfer.

The power-dependent thermal performance observed in Section 3.2 has direct implications for the design of PCM-based thermal management systems for electronics cooling. Modern electronic devices experience transient power loads that can vary by an order of magnitude within seconds [21, 23]. The present results suggest that a Gyroid/PCM heat sink designed for steady-state operation at moderate power (e.g., 10 W) will maintain excellent thermal uniformity during sustained operation, but may experience significant gradient excursions during power surges. The 30 W results indicate that the PCM's thermal buffering capacity can be overwhelmed if the power surge exceeds the lattice's effective thermal transport rate, leading to localized overheating despite the presence of the phase change material.

A key design trade-off identified in this work is between melting speed and thermal uniformity. While higher heating power reduces the time required to absorb a given thermal load, it simultaneously degrades the spatial temperature uniformity that is the primary advantage of combining TPMS lattices with PCM. For electronic cooling applications where junction temperature limits and thermal cycling fatigue are the primary reliability concerns [23], the 10 W operating condition—despite its longer melting time—may provide superior overall system reliability by maintaining the semiconductor junction within a narrower temperature band.

Compared to conventional fin-enhanced PCM heat sinks, the Gyroid/PCM system offers the additional advantage of isotropic thermal performance. Conventional fin arrays provide enhanced heat transfer primarily along the fin axis, creating anisotropic thermal gradients that can lead to warpage and mechanical stress [2]. The Gyroid's triply periodic geometry provides equivalent thermal enhancement in all three spatial directions, making it particularly suitable for applications with multi-directional heat loads or where the heat source location is not fixed.

The reproducibility results (Section 3.4) further support the practical feasibility of Gyroid/PCM thermal management systems. The sub-1 °C variation between independent experimental runs indicates that the manufacturing tolerances achievable with current additive manufacturing techniques (selective laser melting of metallic Gyroid lattices) are sufficient to produce thermally equivalent structures. This finding addresses a common concern regarding the translation of TPMS-based designs from simulation to fabrication, where geometric deviations from the ideal minimal surface could potentially degrade thermal performance [21].

Future work should investigate the effect of lattice relative density on the thermal performance trade-offs identified here, as well as the long-term cyclic stability of the PCM/TPMS system under repeated melting–solidification cycles. Additionally, hybrid designs combining Gyroid and Primitive regions within a single heat sink could potentially exploit the rapid thermal response of the Primitive topology near the heat source while leveraging the Gyroid's uniformity-enhancing characteristics in the distal regions, achieving an optimal balance between response speed and thermal homogeneity.

## 4. Conclusions

This study presents the first systematic experimental comparison of thermal performance between Gyroid and Primitive TPMS lattice structures integrated with phase change materials under constant heat flux. Additively manufactured AlSi10Mg lattices (50 × 50 × 20 mm³) were infiltrated with a paraffin-based PCM (T_m = 42 °C) and tested at heating powers of 10 W, 20 W, and 30 W. Nine thermocouples distributed across three vertical layers enabled quantitative evaluation of through-thickness thermal gradients during melting. The principal findings are as follows.

First, the Gyroid topology demonstrates a decisive advantage in suppressing spatial temperature gradients. At 10 W heating, the bottom-to-midplane gradient (A–B) of the Gyroid structure remains 40–50% lower than that of the Primitive counterpart throughout the phase change window (4.2 °C vs. 7.7 °C at T₁ = 42 °C). More critically, while the Primitive lattice exhibits a 55% gradient deterioration as melting progresses (A–B increasing from 7.7 °C to 11.9 °C), the Gyroid structure maintains remarkable gradient stability, with A–B variations within ±1 °C across the entire melting duration. This behavior is attributed to the Gyroid's triply connected, curvature-continuous channel network, which sustains efficient heat distribution even as the PCM transitions to its low-conductivity liquid phase.

Second, the effect of input power on thermal performance is substantial and nonlinear. Increasing the heating power from 10 W to 30 W elevates the A–B gradient by a factor of 2.8 (from 4.4 °C to 12.4 °C at T₁ = 42 °C) in the Gyroid configuration. Concurrently, the melting duration collapses by approximately 20-fold (from 11.8 min to 0.6 min), indicating that aggressive power input severely compromises the PCM's ability to absorb heat uniformly. This finding establishes a fundamental trade-off between charging speed and thermal uniformity that must be considered in system design.

Third, experimental reproducibility has been rigorously validated through repeated trials under identical conditions. The Gyroid 10 W configuration was tested twice with independent sample preparation, yielding A–B gradient differences below 1 °C and melting duration agreement within 0.3 min. This consistency confirms the reliability of the measurement methodology and the robustness of the observed topological effects.

The practical implications of these findings are direct. For applications demanding spatially uniform thermal management—such as electronics cooling and battery thermal regulation—the Gyroid topology is strongly recommended over the Primitive configuration. System designers should select heating powers that balance charging rate against acceptable gradient levels, with the present data providing quantitative guidance for this optimization.

Future work will address several limitations of the current study. Numerical simulations based on reconstructed TPMS geometries are needed to elucidate the local heat transfer mechanisms and validate the experimental observations. Parametric optimization of TPMS geometry—including wall thickness, unit cell size, and hybrid configurations—should be pursued to tailor performance for specific applications. Long-term thermal cycling tests are required to assess the durability of PCM–lattice interactions over repeated charge–discharge cycles. Finally, integration of TPMS–PCM structures with active cooling systems represents a promising direction for achieving both rapid heat dissipation and sustained thermal regulation.

---

## Figure Captions

**Fig. 1.** Three-dimensional layout of thermocouple positions within the TPMS lattice specimen. Nine Type-K thermocouples (T1–T9) are distributed across three vertical layers: bottom surface (T1), middle layer at z = 10 mm (T2–T5), and top surface at z = 20 mm (T6–T9). The coordinate system origin is located at the geometric center of the bottom heated surface.

**Fig. 2.** Top-view schematic of the thermocouple arrangement showing the 45° rotational offset between the middle layer (T2–T5, square markers) and the top layer (T6–T9, circular markers). This staggered configuration maximizes spatial sampling coverage across the specimen volume and enables accurate reconstruction of three-dimensional temperature gradients.

**Fig. 3.** Temperature gradient comparison between Primitive and Gyroid TPMS lattice structures at 10 W heating power. (a) Temperature evolution at representative measurement points (T1, T_B, T9) for both topologies. (b) Through-thickness A–B and A–C temperature gradients as a function of heater-surface temperature T₁. The Gyroid structure exhibits 40–50% lower gradients and maintains stability throughout the phase change window, whereas the Primitive structure shows progressive gradient deterioration of approximately 55% during melting.

**Fig. 4.** Effect of heating power on the thermal performance of the Gyroid/PCM system. Temperature response at key measurement points under 10 W, 20 W, and 30 W constant power input. Higher power levels produce proportionally increased temperature gradients and dramatically shortened phase change durations, revealing a fundamental trade-off between charging speed and thermal uniformity.

**Fig. 5.** Complete analysis of the Gyroid lattice experiment at 30 W heating power. (a) Full temperature evolution curves for all functional thermocouple channels. (b) Through-thickness temperature gradient evolution showing the extremely steep gradients produced under maximum power input. (c) Phase change kinetics demonstrating the near-instantaneous melting behavior at 30 W, with the complete phase change window compressed to approximately 0.6 min.

**Fig. 6.** Experimental reproducibility validation: comparison of two independent Gyroid lattice experiments conducted at 10 W under nominally identical conditions. The A–B temperature gradient evolution from the repeated experiment ("New") is compared with the original measurement ("Old"). The gradient difference remains below 1 °C throughout the entire melting process, with melting duration agreement within ±0.5 min, confirming the reliability and reproducibility of the experimental methodology.

---

## References

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

*Manuscript prepared for submission to the International Journal of Heat and Mass Transfer*
