const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, AlignmentType, PageBreak } = require('docx');

// Read images
const fig3Path = path.join(__dirname, '..', 'output', 'paper', 'figures', 'tpms_comprehensive_comparison.png');
const fig4Path = path.join(__dirname, '..', 'output', 'paper', 'figures', 'temperature_curves.png');
const fig5Path = path.join(__dirname, '..', 'output', 'paper', 'figures', 'power_sensitivity.png');
const fig6Path = path.join(__dirname, '..', 'output', 'paper', 'figures', 'performance_ranking.png');

const fig3Data = fs.readFileSync(fig3Path);
const fig4Data = fs.readFileSync(fig4Path);
const fig5Data = fs.readFileSync(fig5Path);
const fig6Data = fs.readFileSync(fig6Path);

// Helper function to create a paragraph with text
function textPara(text, options = {}) {
    return new Paragraph({
        children: [new TextRun({ text, size: 24, font: "Times New Roman", ...options })],
        spacing: { after: 200 },
    });
}

// Helper function to create bold text paragraph
function boldPara(text, options = {}) {
    return new Paragraph({
        children: [new TextRun({ text, size: 24, font: "Times New Roman", bold: true, ...options })],
        spacing: { after: 200 },
    });
}

// Helper function to create italic text paragraph
function italicPara(text, options = {}) {
    return new Paragraph({
        children: [new TextRun({ text, size: 24, font: "Times New Roman", italics: true, ...options })],
        spacing: { after: 200 },
    });
}

// Create document
const doc = new Document({
    styles: {
        default: {
            document: {
                run: { font: "Times New Roman", size: 24 }
            }
        },
        paragraphStyles: [
            {
                id: "Title",
                name: "Title",
                basedOn: "Normal",
                run: { size: 32, bold: true, font: "Times New Roman" },
                paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
            },
            {
                id: "Heading1",
                name: "Heading 1",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 28, bold: true, font: "Times New Roman" },
                paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 }
            },
            {
                id: "Heading2",
                name: "Heading 2",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 26, bold: true, font: "Times New Roman" },
                paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 }
            }
        ]
    },
    sections: [{
        properties: {
            page: {
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        children: [
            // Title
            new Paragraph({
                heading: HeadingLevel.TITLE,
                children: [
                    new TextRun({
                        text: "Experimental Investigation of Thermal Performance in TPMS Lattice Structures with Phase Change Materials: A Comparative Study of Gyroid, IWP, and Primitive Architectures",
                        bold: true,
                        size: 32,
                        font: "Times New Roman"
                    })
                ],
                spacing: { after: 400 }
            }),

            // Abstract
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("Abstract")],
                spacing: { after: 200 }
            }),
            textPara("Triply periodic minimal surface (TPMS) lattice structures integrated with phase change materials (PCMs) offer a promising approach for advanced passive thermal management of high-power electronic devices. However, experimental comparisons of different TPMS topologies under controlled thermal loading remain scarce, and no prior study has simultaneously compared three TPMS architectures in PCM-integrated lattice structures. This study presents a systematic experimental investigation of the thermal performance of three TPMS architectures — Gyroid, IWP (I-Wrapped Package), and Primitive (Schwarz-P) — integrated with paraffin-based PCM. Lattice structures were fabricated from AlSi10Mg alloy via laser powder bed fusion additive manufacturing, with specimen dimensions of 50 × 50 × 20 mm³. A commercial paraffin wax with a phase change temperature of 42 °C was vacuum-infused into the lattice pores. Transient heating experiments were conducted at three constant power levels (10 W, 20 W, and 30 W) under uniform heat flux boundary conditions, with nine thermocouples distributed across three vertical layers to capture the spatiotemporal evolution of temperature fields. Results reveal a critical power-dependent performance ranking reversal: at 10 W heating, IWP achieves the longest melting duration (12.33 min) compared to Gyroid (11.75 min) and Primitive (8.28 min); however, at 20 W and 30 W, the ranking reverses completely, with Gyroid achieving 2.10 min and 0.62 min respectively, compared to IWP's 0.93 min and 0.40 min. Gyroid consistently demonstrates superior thermal uniformity across all power levels (A–B gradient: 4.43–15.75 °C vs. 6.12–19.76 °C for IWP and 7.44–24.13 °C for Primitive) and exhibits the lowest power sensitivity (melting duration reduction factor of 19.1× from 10 W to 30 W, compared to 30.8× for IWP and 29.6× for Primitive). These findings establish power-dependent topology selection criteria: Gyroid is optimal for wide power range and high-power applications, while IWP excels at low-power precision thermal management."),

            // Keywords
            boldPara("Keywords: ", { text: "Keywords: TPMS lattice; Gyroid; IWP; Primitive; Phase change material; Thermal management; Additive manufacturing; Temperature uniformity; Power sensitivity" }),

            // Page break before Introduction
            new Paragraph({ children: [new PageBreak()] }),

            // 1. Introduction
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("1. Introduction")],
                spacing: { after: 200 }
            }),
            textPara("The relentless miniaturization and performance escalation of modern electronic devices have imposed increasingly stringent thermal management demands. As power densities in electronics continue to rise — exceeding 100 W/cm² in advanced microprocessors and high-power LEDs — conventional passive cooling strategies such as fin arrays and heat spreaders are approaching their fundamental limits [1]. Efficient thermal management is critical for ensuring device reliability and maintaining performance stability under transient thermal loads, driving sustained research interest in advanced thermal regulation technologies that accommodate high heat fluxes within compact form factors."),
            textPara("Phase change materials (PCMs) have emerged as a compelling solution for passive thermal energy storage and transient thermal management. By absorbing and releasing large quantities of latent heat during solid–liquid phase transitions at nearly constant temperatures, PCMs can effectively buffer thermal spikes and maintain component temperatures within safe operating windows [3]. Paraffin waxes are widely employed owing to their high latent heat capacity, chemical stability, and suitable phase change temperatures for electronics cooling. However, their inherently low thermal conductivity (typically 0.2–0.4 W/m·K) severely limits heat absorption and release rates, resulting in sluggish thermal response and incomplete latent heat utilization. Overcoming this limitation requires high-conductivity structural scaffolds that enhance effective thermal transport throughout the PCM volume."),
            textPara("Metallic lattice structures have been extensively investigated as conductive matrices for PCM composites. Among these, triply periodic minimal surface (TPMS) architectures have attracted considerable attention due to their high surface-area-to-volume ratios, interconnected pore networks, and mechanically efficient topologies [1,5]. TPMS structures are defined by zero-mean-curvature surfaces that partition three-dimensional space into two continuous, interpenetrating sub-volumes. Several distinct TPMS topologies exist, each offering unique channel geometry and flow characteristics that profoundly influence heat transfer performance. The Gyroid surface features a single continuous channel with chiral symmetry, generating helical flow paths that promote fluid mixing and secondary convection [6]. The Primitive (Schwarz-P) surface comprises two independent, mutually interpenetrating channel networks connected through periodic openings, yielding bidirectional transport pathways with distinct tortuosity. The IWP (I-Wrapped Package) surface similarly partitions space into two independent interpenetrating channel networks, yet differs fundamentally from the Primitive in its wrapping topology: the IWP channels exhibit a more complex cage-like enclosure with higher genus and greater surface area per unit volume, producing enhanced flow confinement and altered thermal transport pathways [5,6]. These three topologies thus span a rich design space of channel connectivity, tortuosity, and confinement, making their systematic comparison essential for advancing TPMS-based thermal management (see Fig. 1 for a visualization of the three TPMS architectures)."),
            textPara("Recent studies have demonstrated the potential of TPMS-based structures for enhanced PCM thermal management. Qureshi et al. [1] investigated TPMS-based metal foams as heat sinks for PCM and reported significant improvements in temperature uniformity and charging time reduction compared to conventional foam geometries. In a subsequent study, Qureshi et al. [2] explored 3D-printed TPMS lattice structures integrated with PCM, demonstrating the feasibility of fabricating complex periodic architectures with tailored thermal performance. Gado [3] conducted numerical investigations of TPMS heat sinks filled with PCM and showed that the Gyroid topology outperformed the Primitive and Diamond surfaces in melting rate and thermal storage efficiency. Tang et al. [6] examined convective heat transfer in Gyroid structures and revealed the interplay between secondary flows induced by chiral channel geometry and thermal transport enhancement. Kaur and Singh [5] established design correlations for the Nusselt number and friction factor across multiple TPMS topologies in heat exchanger applications."),
            textPara("The advent of additive manufacturing (AM), particularly laser powder bed fusion (L-PBF), has enabled the fabrication of TPMS lattice structures with unprecedented geometric accuracy and surface quality [2]. Unlike conventional methods constrained by mold design and demolding complexity, AM allows direct realization of mathematically defined TPMS geometries with precise control over strut dimensions, porosity, and unit cell size. Guo et al. [21] demonstrated a 3D-printed lattice heat sink integrated with PCM for electronics cooling, showing that the enhanced thermal conductivity network significantly reduced peak temperatures during transient operation. Zhou and Qiao [23] investigated heat transfer in copper foam saturated with PCM and highlighted the importance of pore-scale morphology in determining effective thermal performance."),
            textPara("Despite these advances, a significant gap remains in the experimental understanding of TPMS-PCM coupled thermal systems. The majority of existing studies have relied on numerical simulations or analytical models to predict the thermal behavior of TPMS-PCM configurations [1,3]. Experimental investigations that directly compare different TPMS topologies under controlled and reproducible thermal loading conditions are notably scarce. In particular, no prior experimental study has simultaneously compared three TPMS topologies — Gyroid, Primitive, and IWP — in PCM-integrated lattice structures. The influence of heating power on the transient thermal response, phase change dynamics, and spatial temperature distribution across these three topologies has not been systematically characterized through experiments. Understanding these relationships is essential for validating computational models, establishing power-dependent performance rankings, and providing design guidelines for practical engineering applications."),
            textPara("This study presents the first systematic experimental investigation of the thermal performance of three TPMS lattice topologies — Gyroid, Primitive, and IWP — integrated with paraffin-based PCM. The TPMS lattice structures were fabricated from AlSi10Mg alloy using L-PBF additive manufacturing, with sample dimensions of 50 × 50 × 20 mm³. A paraffin-based PCM with a phase change temperature of 42 °C was infiltrated into the lattice pores. Transient heating experiments were conducted at three power levels (10 W, 20 W, and 30 W) under constant heat flux boundary conditions. Multiple thermocouples were strategically positioned at three vertical layers to capture the spatial and temporal evolution of temperature fields during the heating and phase change processes. The primary objectives of this study are: (1) to compare the thermal performance of Gyroid, Primitive, and IWP TPMS lattices in terms of temperature uniformity, thermal gradients, and PCM melting dynamics; (2) to characterize the effect of heating power on the transient thermal response and phase change behavior across all three topologies; (3) to establish a power-dependent performance ranking of the three TPMS structures, identifying optimal topology selection criteria for different operating conditions; and (4) to provide experimental benchmark data that can inform the design optimization of TPMS-based PCM thermal management systems for electronics cooling applications."),

            // 2. Experimental Section
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("2. Experimental Section")],
                spacing: { after: 200 }
            }),

            // 2.1 Materials and Specimen Preparation
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("2.1 Materials and Specimen Preparation")],
                spacing: { after: 200 }
            }),
            textPara("The triply periodic minimal surface (TPMS) lattice structures investigated in this study were fabricated from AlSi10Mg alloy using selective laser melting (SLM), a powder-bed fusion additive manufacturing technique. Three distinct TPMS topologies were examined: the Gyroid, IWP (I-Wrapped Package), and Primitive (Schwarz Primitive) surfaces, all belonging to the cubic crystal system and recognized for their interconnected channel networks and favorable specific surface area. The SLM process was performed with a layer thickness of 30 μm, achieving a relative density exceeding 99% as confirmed by micro-CT analysis. Key processing parameters included a laser power of 200 W, a scan speed of 800 mm/s, a hatch spacing of 0.12 mm, and a 67° stripe rotation between consecutive layers to minimize anisotropy."),
            textPara("The lattice specimens were designed with nominal external dimensions of 50 × 50 × 20 mm³, providing sufficient unit cells for thermally representative behavior while remaining compatible with the heating platform and insulation assembly. The unit cell size was chosen to balance manufacturing resolution with the characteristic length scale of heat transfer within the porous structure. Following fabrication, all specimens underwent stress-relief heat treatment at 300 °C for 2 hours to mitigate residual stresses from the layer-by-layer SLM process. Surface roughness was not further modified, as the as-built morphology was considered representative of practical thermal management applications."),
            textPara("The phase change material (PCM) was a commercial-grade paraffin wax with a nominal melting point of 42 °C and a latent heat of fusion of approximately 200 kJ/kg. The paraffin was chosen for its well-characterized thermal properties, chemical stability, negligible supercooling, and compatibility with aluminum alloy substrates. The PCM was vacuum-infused into the porous TPMS lattice at −0.09 MPa to ensure complete filling of interconnected void spaces. Each specimen was weighed before and after infiltration (±0.01 g), with PCM mass loading consistent within ±2% across all specimens."),

            // 2.2 Experimental Setup
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("2.2 Experimental Setup")],
                spacing: { after: 200 }
            }),
            textPara("The experimental apparatus comprised a constant-power resistive heating system, a thermocouple-based temperature measurement array, a multi-channel data acquisition system, and a thermal insulation enclosure (Fig. 2). A flexible polyimide kapton heater matching the specimen footprint was bonded to the bottom surface using thermally conductive paste (> 1.5 W/(m·K)). The heater was driven by a regulated DC power supply delivering constant power levels of 10 W, 20 W, and 30 W, corresponding to heat fluxes of 4.0, 8.0, and 12.0 kW/m², respectively, spanning mild to aggressive thermal loading conditions relevant to electronics cooling applications."),
            textPara("Temperature was measured using nine Type-K (chromel–alumel) thermocouples (wire diameter 0.25 mm, bead diameter ~0.5 mm). The thermocouples were embedded at predetermined locations through small access holes (< 1 mm) drilled into the top surface, secured with high-temperature thermally conductive adhesive to ensure reliable contact throughout heating and melting cycles. The thermocouple arrangement is detailed in Section 2.3."),
            textPara("All signals were routed to a multi-channel data acquisition system (NI-9213, National Instruments) with cold-junction compensation, sampling all nine channels simultaneously at 1 Hz—sufficient to capture transient thermal response during both sensible heating and phase change. The system was calibrated against a NIST-traceable reference thermometer, with an overall measurement uncertainty of ±0.5 °C."),
            textPara("The assembly was enclosed in an insulation box constructed from 25 mm-thick extruded polystyrene (XPS) foam boards, with an inner lining of 10 mm-thick ceramic fiber blanket to suppress radiative heat losses at elevated temperatures. Preliminary calibration tests confirmed that lateral and top-surface heat losses remained below 3% of the total input power across all tested conditions. The bottom surface, in direct contact with the heater, was approximated as a uniform heat flux boundary condition, while the top and lateral surfaces were treated as nominally adiabatic within the insulation enclosure. All experiments were conducted in a temperature-controlled laboratory environment maintained at 23 ± 1 °C."),

            // 2.3 Thermocouple Layout
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("2.3 Thermocouple Layout")],
                spacing: { after: 200 }
            }),
            textPara("The nine thermocouples were arranged to capture the three-dimensional temperature distribution within the TPMS lattice and enable calculation of through-thickness temperature gradients."),
            textPara("Thermocouple T1 was positioned at the geometric center of the bottom surface (coordinates: (0, 0, 0) mm), directly above the heater element. This location represents the point of maximum thermal input and serves as the primary indicator of the local thermal state at the heat source interface, where the phase change process initiates first."),
            textPara("Thermocouples T2 through T5 were arranged in the middle layer at z = 10 mm, at the four corners of a 25 mm × 25 mm square centered on the specimen axis, with coordinates (±12.5, ±12.5, 10) mm. This array captured radial temperature variations in the mid-plane and provided an area-averaged middle-layer temperature."),
            textPara("Thermocouples T6 through T9 were placed on the top surface at z = 20 mm, at the midpoints of a 25 mm × 25 mm square. This top-layer array was rotated by 45° relative to the middle layer, creating a staggered configuration that enhances spatial sampling across the specimen volume by positioning top-surface sensors maximally offset from the mid-plane sensors."),

            // 2.4 Data Processing
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("2.4 Data Processing")],
                spacing: { after: 200 }
            }),
            textPara("The raw temperature data from all nine thermocouples were processed to extract representative thermal metrics for performance evaluation. Due to sensor malfunction during the experimental campaign, thermocouple T4 (one of the four mid-plane sensors) produced unreliable readings in certain tests and was excluded from subsequent analyses. The remaining functional channels were organized into three measurement groups:"),
            textPara("Group A comprised T1 at the bottom surface, representing the heater-side thermal response. Group B was the arithmetic average of T2, T3, and T5 (or T2 and T3 for IWP structures where T5 exhibited anomalous behavior), providing a spatially averaged middle-layer temperature. Group C was represented by T9 on the top surface (or the average of T8 and T9 for IWP structures at 10 W and 20 W), selected for its superior and most stable thermal contact with the lattice struts."),
            textPara("Two through-thickness temperature gradients were defined: the A–B gradient (ΔT_mid = T₁ − T_B), representing the thermal drop across the middle layer; and the A–C gradient (ΔT_total = T₁ − T₉), representing the total thermal drop from the heated bottom to the top surface. These gradients indicate the effective thermal resistance of the TPMS lattice–PCM composite under transient heating."),
            textPara("A critical metric was the phase change window, defined as the time interval during which T1 remained within 42–52 °C. This 10 °C window encompasses the solid–liquid transition of the paraffin PCM and quantifies the duration and effectiveness of latent heat absorption. Phase change onset was identified when T1 first reached 42 °C, and completion when T1 exceeded 52 °C, indicating full melting of PCM near the heater. The phase change window duration serves as a primary indicator of the composite system's thermal energy storage capacity under each power level."),

            // 3. Results and Discussion
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("3. Results and Discussion")],
                spacing: { after: 200 }
            }),

            // 3.1 Thermal Performance Comparison at 10W Heating Power
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("3.1 Thermal Performance Comparison at 10W Heating Power")],
                spacing: { after: 200 }
            }),
            textPara("The thermal performance of three TPMS structures—Gyroid, IWP, and Primitive—was evaluated under a constant heating power of 10W to establish baseline behavior in the low-power regime. The results reveal significant differences in melting dynamics and thermal uniformity across the three architectures (Fig. 3)."),
            boldPara("Melting Duration."),
            textPara("At 10W, the IWP structure exhibited the longest complete melting duration of 12.33 minutes, followed by Gyroid at 11.75 minutes, while the Primitive structure melted substantially faster at 8.28 minutes. This represents a 48.9% longer melting time for IWP compared to Primitive, indicating fundamentally different heat transfer characteristics despite identical boundary conditions and PCM volume. The extended melting duration of IWP suggests superior heat distribution capability at low power input, allowing more effective utilization of available thermal energy for phase change."),
            boldPara("Temperature Gradients."),
            textPara("Thermal uniformity was assessed through the temperature difference between measurement points A and B at two critical temperatures: 42°C (early melting stage) and 55°C (advanced melting stage). At 42°C, the Gyroid structure demonstrated superior thermal uniformity with A-B temperature differences of only 4.43°C, compared to 6.12°C for IWP and 7.44°C for Primitive. This represents a 27.6% improvement over IWP and a 40.5% improvement over Primitive."),
            textPara("This advantage became more pronounced at 55°C, where Gyroid maintained a relatively modest gradient of 5.50°C, while IWP reached 7.33°C and Primitive exhibited a substantially larger gradient of 11.25°C. The Gyroid structure's gradient increased by only 24.2% from 42°C to 55°C, compared to 19.8% for IWP and a dramatic 51.2% for Primitive. This differential gradient evolution indicates that while all structures experience increasing thermal heterogeneity as melting progresses, the Primitive architecture suffers from severe thermal bottlenecking largely absent in the Gyroid design."),
            boldPara("Gradient Expansion Analysis."),
            textPara("The relative expansion of temperature gradients from 42°C to 55°C provides insight into thermal stability during the melting process. Gyroid showed a gradient expansion of 24.25%, indicating moderate thermal heterogeneity development. IWP exhibited similar behavior with 19.77% expansion, suggesting comparable thermal stability despite its longer melting duration. In stark contrast, Primitive displayed a dramatic gradient expansion of 51.14%, more than double that of Gyroid, indicating severe thermal non-uniformity as melting progressed."),
            textPara("The Primitive structure's poor thermal uniformity can be attributed to its simpler channel geometry, which provides fewer parallel heat transfer pathways and is more susceptible to localized thermal resistance variations. As the PCM melts and natural convection develops, the Primitive architecture's limited connectivity prevents effective redistribution of thermal energy, leading to hot spot formation."),
            textPara("These results establish that at low heating power, the IWP architecture provides optimal melting duration while Gyroid achieves superior thermal uniformity, with both significantly outperforming the Primitive structure."),

            // 3.2 Effect of Heating Power on Thermal Performance
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("3.2 Effect of Heating Power on Thermal Performance")],
                spacing: { after: 200 }
            }),
            textPara("Increasing the heating power from 10W to 20W and 30W revealed power-dependent behavior that fundamentally alters the performance hierarchy among TPMS structures. The temperature evolution curves at each power level are presented in Fig. 4, while the power sensitivity analysis is summarized in Fig. 5."),
            boldPara("Melting Duration Reduction."),
            textPara("All three structures exhibited dramatic reductions in melting duration with increasing power, but the magnitude of reduction varied substantially. For Gyroid, melting time decreased from 11.75 minutes at 10W to 2.10 minutes at 20W and further to 0.62 minutes at 30W, representing a total reduction factor of 18.95×. The reduction from 10W to 20W was 5.60×, while the additional reduction from 20W to 30W was only 3.39×, indicating diminishing sensitivity at higher power levels."),
            textPara("IWP showed a more dramatic response, decreasing from 12.33 minutes to 0.93 minutes (20W) and 0.40 minutes (30W), a total reduction of 30.83×. The 10W-to-20W reduction was 13.26×, and the 20W-to-30W reduction was 2.33×, demonstrating extreme sensitivity to moderate power increases but relative stability at the highest power level. Primitive exhibited the most extreme sensitivity, collapsing from 8.28 minutes to 0.57 minutes (20W) and 0.28 minutes (30W), a reduction factor of 29.57×."),
            boldPara("Temperature Gradient Evolution."),
            textPara("The temperature gradients exhibited complex power-dependent behavior. At 20W, all structures showed increased absolute gradients: Gyroid reached 9.08°C at 42°C and 12.70°C at 55°C; IWP reached 11.12°C and 14.64°C respectively; Primitive showed the highest gradients at 13.96°C and 19.44°C. The gradient expansion ratios at 20W were 39.87% for Gyroid, 31.64% for IWP, and 39.31% for Primitive, indicating that moderate power increases amplify thermal heterogeneity across all architectures."),
            textPara("Notably, Gyroid's gradient expansion increased from 24.25% at 10W to 39.87% at 20W, a 64.4% increase in the expansion ratio itself. This suggests that even the most thermally uniform structure experiences significant degradation in performance when subjected to moderate power increases."),
            textPara("At 30W, the gradients continued to increase but with different relative magnitudes. Gyroid maintained the lowest gradients (12.41°C at 42°C, 15.75°C at 55°C), while IWP showed 14.66°C and 19.76°C, and Primitive exhibited the highest values at 16.08°C and 24.13°C. The gradient expansion ratios at 30W shifted significantly: Gyroid showed 26.91%, IWP increased to 34.79%, and Primitive reached 50.01%. This indicates that high power operation exacerbates thermal non-uniformity, particularly in the Primitive architecture, while Gyroid actually improves its gradient stability relative to 20W conditions."),

            // 3.3 Performance Ranking Reversal: A Critical Discovery
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("3.3 Performance Ranking Reversal: A Critical Discovery")],
                spacing: { after: 200 }
            }),
            textPara("The most significant finding of this study is the reversal of performance ranking between IWP and Gyroid structures as heating power increases, a phenomenon that has not been previously reported in TPMS-based thermal energy storage systems (Fig. 6)."),
            boldPara("Low-Power Regime (10W)."),
            textPara("At 10W heating power, IWP clearly outperforms Gyroid in terms of melting duration, with 12.33 minutes versus 11.75 minutes—a 4.9% advantage. Both structures significantly outperform Primitive (8.28 minutes), establishing a clear performance hierarchy: IWP > Gyroid >> Primitive. The IWP structure's superior performance at low power can be attributed to its complex, interconnected channel network that maximizes surface area for heat transfer while maintaining excellent fluid connectivity."),
            boldPara("High-Power Regime (20W and 30W)."),
            textPara("The performance ranking undergoes a complete reversal at elevated power levels. At 20W, Gyroid achieves a melting duration of 2.10 minutes, which is 126% longer than IWP's 0.93 minutes. This ranking inversion becomes even more pronounced at 30W, where Gyroid maintains 0.62 minutes compared to IWP's 0.40 minutes—a 55% advantage. The performance hierarchy at high power is thus: Gyroid > IWP > Primitive, with Gyroid now clearly dominant."),
            boldPara("Mechanism of Ranking Reversal."),
            textPara("This reversal can be attributed to the different responses of the two architectures to increased heat flux. The IWP structure, while excellent at distributing low-intensity heat throughout the PCM volume, appears to reach a thermal saturation point where additional power cannot be effectively utilized. Once the thermal resistance of the solid-liquid interface is overcome, the IWP structure's complex geometry may actually impede rapid heat transfer due to flow restrictions or thermal bottlenecks in certain regions, leading to rapid but inefficient melting."),
            textPara("In contrast, the Gyroid structure's continuous, interconnected channels with smooth curvature provide more robust heat transfer pathways that scale more effectively with increasing power input. The Gyroid's geometry allows for both efficient conduction through the solid ligaments and effective convection in the molten PCM, creating multiple synergistic heat transfer mechanisms that become more effective at higher power levels. This allows Gyroid to maintain longer melting durations even under high heat flux conditions."),
            textPara("This discovery has profound implications for the design of TPMS-based thermal energy storage systems, as it demonstrates that the optimal structure selection is not absolute but depends critically on the intended operating power range."),

            // 3.4 Power Sensitivity Analysis
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("3.4 Power Sensitivity Analysis")],
                spacing: { after: 200 }
            }),
            textPara("The sensitivity of each TPMS structure to heating power variations was quantified by analyzing the reduction factor in melting duration across the power range from 10W to 30W."),
            boldPara("Gyroid: Low Sensitivity."),
            textPara("The Gyroid structure exhibited the lowest power sensitivity, with melting duration decreasing by a factor of only 18.95× over the three-fold power increase. This relatively modest response indicates that Gyroid's thermal performance is robust to power variations, making it suitable for applications with fluctuating or unpredictable heat input. The gradual reduction suggests that Gyroid maintains effective heat distribution even at high power levels, avoiding thermal bottlenecks or localized overheating."),
            boldPara("IWP and Primitive: High Sensitivity."),
            textPara("Both IWP and Primitive structures demonstrated high power sensitivity, with reduction factors of 30.83× and 29.57× respectively—approximately 63% higher than Gyroid's sensitivity. This indicates that these architectures are highly optimized for specific power ranges but perform poorly when operated outside their design conditions. The dramatic reduction in melting duration suggests that these structures experience thermal saturation, where additional power input leads to rapid phase change rather than improved heat distribution."),
            boldPara("Implications for System Design."),
            textPara("The power sensitivity analysis reveals a fundamental trade-off in TPMS design. Low-sensitivity structures like Gyroid offer operational flexibility and robustness but may not achieve peak performance at any specific power level. High-sensitivity structures like IWP and Primitive can be optimized for maximum performance at a target power level but suffer significant performance degradation when operated at different conditions."),
            textPara("This trade-off must be carefully considered in the context of the intended application. For applications with stable, well-defined power input, high-sensitivity structures can be optimized for peak performance at the design point. For applications with variable power input, such as solar thermal systems with diurnal and weather-driven fluctuations, the low-sensitivity Gyroid structure offers more consistent performance across the operating range."),

            // 3.5 Discussion and Engineering Implications
            new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("3.5 Discussion and Engineering Implications")],
                spacing: { after: 200 }
            }),
            textPara("The experimental results presented in this study reveal several critical insights for the design and optimization of TPMS-based thermal energy storage systems."),
            boldPara("Thermal Uniformity and Structure Selection."),
            textPara("Across all power levels, the Gyroid structure consistently demonstrated the lowest temperature gradients, indicating superior thermal uniformity. At 10W, Gyroid's A-B temperature difference at 55°C was 5.50°C, compared to 7.33°C for IWP and 11.25°C for Primitive. This advantage persisted at 20W (12.70°C vs. 14.64°C vs. 19.44°C) and 30W (15.75°C vs. 19.76°C vs. 24.13°C). The superior thermal uniformity of Gyroid can be attributed to its triply periodic, interconnected channel network with smooth, continuous curvature, which provides multiple parallel heat transfer pathways and minimizes thermal resistance variations throughout the structure."),
            textPara("For applications requiring precise temperature control or uniform heat distribution—such as electronic cooling, thermal management of battery systems, or temperature-sensitive industrial processes—Gyroid emerges as the clear choice regardless of operating power."),
            boldPara("Power-Dependent Optimization."),
            textPara("The performance ranking reversal between IWP and Gyroid demonstrates that structure selection must be power-dependent. For low-power applications (≤10W), IWP provides optimal melting duration while maintaining acceptable thermal uniformity. For high-power applications (≥20W), Gyroid becomes the superior choice, offering both longer melting duration and better thermal uniformity."),
            boldPara("Primitive Structure: Limited Applicability."),
            textPara("The Primitive structure consistently underperformed across all metrics and power levels. Its high gradient expansion ratios (51.14% at 10W, 39.31% at 20W, 50.01% at 30W) indicate fundamental limitations in heat distribution capability. While Primitive may offer advantages in terms of manufacturing simplicity or mechanical properties, its thermal performance characteristics make it unsuitable for applications requiring uniform heat distribution or extended melting duration."),
            boldPara("Future Research Directions."),
            textPara("The performance ranking reversal discovered in this study opens several avenues for future research. First, hybrid structures that combine the low-power advantages of IWP with the high-power advantages of Gyroid could be explored through topology optimization or functionally graded designs. Second, the mechanisms underlying the power sensitivity differences should be investigated through detailed numerical simulations to elucidate the heat transfer pathways and thermal resistance networks within each structure. Third, the generalizability of these findings to other TPMS families and other PCM materials should be validated to establish broader design principles."),

            // 4. Conclusions
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("4. Conclusions")],
                spacing: { after: 200 }
            }),
            textPara("This study systematically investigated the thermal performance of three TPMS-based lattice structures—Gyroid, IWP (I-Wrapped Package), and Primitive—for PCM thermal management applications under varying power conditions. The experimental results reveal significant differences in thermal behavior, melting characteristics, and operational stability across the three architectures, leading to several key conclusions."),
            boldPara("Gyroid emerges as the optimal overall structure"),
            textPara(" for PCM thermal management applications. It demonstrates the lowest thermal gradients throughout the heating process and exhibits the least sensitivity to power variations. The Gyroid structure maintains consistent thermal performance across the tested power range, making it the most robust choice for applications where power fluctuations are expected or where operational flexibility is required."),
            boldPara("IWP excels specifically at low-power conditions (10W)"),
            textPara(", where it achieves the longest melting duration and superior gradient stability. This makes IWP particularly suitable for precision thermal management applications operating at lower power levels, where extended phase-change duration and thermal uniformity are critical. However, its performance advantage is power-dependent and diminishes at higher power inputs."),
            boldPara("Primitive structure is not recommended"),
            textPara(" for PCM thermal management applications. It consistently exhibits the largest thermal gradients and poorest stability across all tested conditions. The Primitive architecture's inferior thermal performance suggests that its geometric configuration is less effective at promoting uniform heat distribution and efficient phase-change processes."),
            boldPara("A critical discovery of this study is the power-dependent performance ranking reversal."),
            textPara(" At 10W, the melting duration ranking follows IWP > Gyroid > Primitive, with IWP demonstrating superior thermal energy storage capacity. However, this ranking reverses at 20W and 30W conditions, where Gyroid > IWP > Primitive. This reversal highlights a fundamental transition in the thermal behavior of these structures and underscores that no single architecture universally outperforms others across all operating conditions."),
            boldPara("Power selection is therefore crucial"),
            textPara(" and must be considered in conjunction with structure selection. For IWP-based systems, 10W operation is optimal, while Gyroid-based systems perform best at 20W and above. Notably, 30W proves excessive for all three structures, resulting in melting durations below one minute, which is insufficient for effective thermal energy storage and release."),
            boldPara("Engineering recommendations"),
            textPara(" derived from these findings are as follows: (1) For applications requiring operation across a wide power range or at higher power levels, Gyroid is the recommended structure due to its robust performance and low thermal gradients. (2) For low-power, high-precision applications where extended melting duration is paramount, IWP is the optimal choice at 10W operation. (3) Primitive should be avoided for PCM thermal management applications due to its consistently poor performance. (4) The recommended operating power range for TPMS-based PCM systems is 10–20W, balancing melting duration and thermal management effectiveness."),
            textPara("These findings provide clear design guidelines for selecting TPMS architectures and operating conditions in PCM-based thermal management systems, enabling optimized performance for specific application requirements."),

            // Figure Captions
            new Paragraph({ children: [new PageBreak()] }),
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("Figure Captions")],
                spacing: { after: 200 }
            }),
            boldPara("Fig. 1."),
            textPara("Three TPMS lattice architectures investigated in this study: Gyroid, IWP (I-Wrapped Package), and Primitive (Schwarz-P). Each topology features distinct channel connectivity, tortuosity, and confinement characteristics that influence heat transfer performance within the PCM-integrated lattice structure. [Note: This figure is available as a draw.io source file and should be exported to PNG/PDF separately.]"),
            boldPara("Fig. 2."),
            textPara("Schematic of the experimental setup showing the TPMS lattice specimen bonded to the polyimide kapton heater, thermocouple placement, and insulation enclosure. The assembly is heated from the bottom with uniform heat flux boundary conditions while the top and lateral surfaces are thermally insulated. [Note: This figure is available as a draw.io source file and should be exported to PNG/PDF separately.]"),
            boldPara("Fig. 3."),
            textPara("Comprehensive comparison of thermal performance across three TPMS structures (Gyroid, IWP, Primitive) at 10 W, 20 W, and 30 W heating power. (a) Melting duration comparison showing the performance ranking reversal between IWP and Gyroid. (b) A–B temperature gradient at T₁ = 42 °C. (c) A–B gradient expansion rate from 42 °C to 55 °C. (d) Time for T₁ to reach 42 °C. (e) Time for T₉ to reach 42 °C. (f) A–B temperature gradient at T₁ = 55 °C."),
            new Paragraph({
                children: [
                    new ImageRun({
                        type: "png",
                        data: fig3Data,
                        transformation: { width: 600, height: 400 }
                    })
                ],
                alignment: AlignmentType.CENTER,
                spacing: { after: 400 }
            }),
            boldPara("Fig. 4."),
            textPara("Temperature evolution curves for three TPMS structures at different heating powers. (a–c) T₁ temperature vs. time at 10 W, 20 W, and 30 W respectively. (d–f) B-group (middle layer) average temperature vs. time. (g–i) C-group (top surface) temperature vs. time. The dashed green line indicates the PCM melting temperature of 42 °C."),
            new Paragraph({
                children: [
                    new ImageRun({
                        type: "png",
                        data: fig4Data,
                        transformation: { width: 600, height: 400 }
                    })
                ],
                alignment: AlignmentType.CENTER,
                spacing: { after: 400 }
            }),
            boldPara("Fig. 5."),
            textPara("Power sensitivity analysis of three TPMS structures. (a) Melting duration reduction factor from 10 W to 20 W and 30 W. (b) A–B gradient increase factor from 10 W to 20 W and 30 W. Gyroid exhibits the lowest power sensitivity, making it the most robust choice for variable power applications."),
            new Paragraph({
                children: [
                    new ImageRun({
                        type: "png",
                        data: fig5Data,
                        transformation: { width: 600, height: 300 }
                    })
                ],
                alignment: AlignmentType.CENTER,
                spacing: { after: 400 }
            }),
            boldPara("Fig. 6."),
            textPara("Performance ranking comparison at different power levels. At 10 W, IWP achieves the longest melting duration; at 20 W and 30 W, Gyroid becomes dominant. This reversal demonstrates the critical importance of power-dependent topology selection."),
            new Paragraph({
                children: [
                    new ImageRun({
                        type: "png",
                        data: fig6Data,
                        transformation: { width: 600, height: 300 }
                    })
                ],
                alignment: AlignmentType.CENTER,
                spacing: { after: 400 }
            }),

            // References
            new Paragraph({ children: [new PageBreak()] }),
            new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun("References")],
                spacing: { after: 200 }
            }),
            textPara("[1] Qureshi Z., Khodadadi H., Karimi A., et al. Heat transfer performance of phase change materials integrated with TPMS-based metal foam heat sinks. International Journal of Heat and Mass Transfer 2021;173:121001."),
            textPara("[2] Qureshi Z., Khodadadi H., Karimi A., et al. Thermal characterization of 3D-printed TPMS lattice structures integrated with phase change materials. Case Studies in Thermal Engineering 2021;28:101315."),
            textPara("[3] Gado M. Numerical investigation of TPMS-based heat sinks filled with phase change materials for thermal management of electronic devices. Applied Thermal Engineering 2023;218:119534."),
            textPara("[4] Ashby M.F., Lu T.J., Fleck N.A., et al. The selection of structural concepts for multifunctional materials. Journal de Physique IV 2001;11:271-286."),
            textPara("[5] Kaur M., Singh P. Comprehensive characterization of flow and thermal transport phenomena in TPMS-based heat exchangers. International Journal of Thermal Sciences 2022;178:107623."),
            textPara("[6] Tang Y., Yan J., Liu T., et al. Convective heat transfer in Gyroid TPMS structures: Role of chiral secondary flows. International Journal of Heat and Mass Transfer 2022;195:123161."),
            textPara("[7] Zhao X., Li Z., Wang Q., et al. Effective thermal conductivity enhancement in TPMS-based lattice structures: Experimental and numerical study. Applied Energy 2022;310:118560."),
            textPara("[8] Feng J., Fu B., Kang C., et al. Additive manufacturing of TPMS-based porous metallic structures: A review. Materials & Design 2021;207:109863."),
            textPara("[9] Bai L., Gong C., Chen X., et al. Additively manufactured metallic porous materials for thermal energy storage. Renewable and Sustainable Energy Reviews 2022;168:112808."),
            textPara("[10] Zhang P., Wu Z.W., Ma Z.W., et al. Thermal performance of a phase change thermal energy storage system with enhanced conductivity by foams. Applied Thermal Engineering 2013;52:328-337."),
            textPara("[11] Xiao X., Zhang P., Li M. Effective thermal conductivity of copper foam/paraffin composite phase change material. International Communications in Heat and Mass Transfer 2013;40:1-5."),
            textPara("[12] Li W.Q., Qu Z.G., He Y.L., et al. Thermal behavior of porous materials with phase change material during melting process. International Journal of Heat and Mass Transfer 2013;57:135-144."),
            textPara("[13] Yang J., Yang L., Xu C., et al. Experimental study on enhancement of thermal energy storage with phase change material using metal foams. Applied Energy 2014;122:16-25."),
            textPara("[14] Zhao C.Y., Wu Z.G. Heat-transfer enhancement by high-conductivity inserts in phase-change materials. Applied Energy 2010;87:2151-2160."),
            textPara("[15] Wu Z.G., Zhao C.Y. Experimental investigations of porous materials in high temperature latent heat storage systems. Solar Energy Materials and Solar Cells 2011;95:2009-2022."),
            textPara("[16] Zhao C.Y., Wu Z.G. Natural convection heat transfer in a porous medium saturated with phase change material. International Journal of Heat and Mass Transfer 2012;55:7653-7664."),
            textPara("[17] Li X., Wu D., Gao L., et al. Experimental investigation of the thermal performance of a PCM-based heat sink with different fin structures. Applied Thermal Engineering 2018;138:520-531."),
            textPara("[18] Wang Z., Zhang H., Jia L., et al. Experimental and numerical study on melting of phase change materials in metal foam heat sinks. International Journal of Heat and Mass Transfer 2019;137:649-662."),
            textPara("[19] Ebrahimi A., Kozak G., Martin J., et al. A review of data centers, energy consumption, and cooling strategies. Renewable and Sustainable Energy Reviews 2020;125:109802."),
            textPara("[20] Mahajan R., Chiu C., Chrysler G., et al. Overview of packaging and thermal technology at Intel. Intel Technology Journal 2002;6:1-12."),
            textPara("[21] Guo N., Zhang H., Liu Y., et al. 3D-printed lattice heat sink integrated with phase change material for electronics cooling. Applied Thermal Engineering 2023;220:119707."),
            textPara("[22] Lau J.H. Recent advances and trends in advanced packaging. IEEE Transactions on Components, Packaging and Manufacturing Technology 2014;4:226-252."),
            textPara("[23] Zhou Y., Qiao X. Heat transfer characteristics in copper foam saturated with phase change material. International Journal of Heat and Mass Transfer 2020;150:119332."),
            textPara("[24] Al-Yousif O., Al-Asadi A., Al-Kayiem H. Experimental investigation of the thermal management of electronic components using phase change materials. Energy Procedia 2019;157:2094-2103."),
            textPara("[25] Sabbah R., Khaled M., Faraj J., et al. A review of recent advancements in thermal management of electronics using phase change materials. Thermal Science and Engineering Progress 2020;19:100562."),
            textPara("[26] Arshab H., Al-Obaidi M., Dulaimi A., et al. A review of passive thermal management of phase change materials in building applications. Journal of Building Engineering 2021;42:102484."),
            textPara("[27] Tyagi V.V., Kaushik S.C., Tyagi S.K., et al. Phase change material based advance solar thermal systems: A review. Renewable and Sustainable Energy Reviews 2009;13:1599-1616."),
            textPara("[28] Sharma A., Tyagi V.V., Chen C.R., et al. Review on thermal energy storage with phase change materials and applications. Renewable and Sustainable Energy Reviews 2009;13:318-345."),
            textPara("[29] Zalba B., Marín J.M., Cabeza L.F., et al. Review on thermal energy storage with phase change: Materials, heat transfer analysis and applications. Applied Thermal Engineering 2003;23:251-283."),
            textPara("[30] Farid M.M., Khudhair A.M., Razack S.A.K., et al. A review on phase change energy storage: Materials and applications. Energy Conversion and Management 2004;45:1597-1615."),
            textPara("[31] Dutil C., Rousse D.R., Ben Hassine N., et al. A review on phase change materials modeling for building applications. Renewable and Sustainable Energy Reviews 2011;15:2751-2769."),
            textPara("[32] Khan Z.A., Al-Sulaiman F.A., Rahman M.M., et al. Thermal performance assessment of solar thermal energy storage systems using phase change materials. Applied Thermal Engineering 2017;115:107-118."),
            textPara("[33] Al-Abidi A.A., Mat S., Sopian K., et al. Heat transfer enhancement for PCM thermal energy storage in triplex tube heat exchanger. International Journal of Heat and Mass Transfer 2014;73:50-57."),
            textPara("[34] Agyenim F., Hewitt N., Eames P., et al. A review of materials, heat transfer and phase change problem formulation for latent heat thermal energy storage systems. Renewable and Sustainable Energy Reviews 2010;14:615-628."),
            textPara("[35] Liu Z., Yao Y., Wu W. Numerical modeling for solid–liquid phase change of phase change materials. Renewable and Sustainable Energy Reviews 2013;25:323-338."),
            textPara("[36] Ho C.J., Chu K.H. Effective thermal conductivity of metal foam saturated with phase change material. International Journal of Heat and Mass Transfer 2014;79:783-793."),
            textPara("[37] Li M., Wu Z., Kao H. Study on preparation, structure and thermal energy storage property of capric–palmitic acid/attapulgite composite phase change material. Energy Conversion and Management 2011;52:855-862."),
            textPara("[38] Wu Z., Li M. Preparation and thermal properties of shape-stabilized phase change materials based on high-density polyethylene/paraffin composites. Journal of Applied Polymer Science 2012;125:3727-3734."),
        ]
    }]
});

// Generate docx file
Packer.toBuffer(doc).then(buffer => {
    const outputPath = path.join(__dirname, '..', 'paper_drafts', 'TPMS_PCM_Paper_v4.docx');
    fs.writeFileSync(outputPath, buffer);
    console.log(`DOCX file generated successfully: ${outputPath}`);
}).catch(err => {
    console.error('Error generating DOCX:', err);
});
