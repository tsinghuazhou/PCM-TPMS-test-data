## 2. Experimental Section

### 2.1 Materials and Specimen Preparation

The triply periodic minimal surface (TPMS) lattice structures investigated in this study were fabricated from AlSiMg alloy (AlSi10Mg) using selective laser melting (SLM), a powder-bed fusion additive manufacturing technique. Two distinct TPMS topologies were examined: the Gyroid and Primitive (Schwarz Primitive) surfaces, both belonging to the cubic crystal system and recognized for their interconnected channel networks and favorable specific surface area. The SLM process was performed with a layer thickness of 30 μm, achieving a relative density exceeding 99% as confirmed by micro-CT analysis. Key processing parameters included a laser power of 200 W, a scan speed of 800 mm/s, a hatch spacing of 0.12 mm, and a 67° stripe rotation between consecutive layers to minimize anisotropy.

The lattice specimens were designed with nominal external dimensions of 50 × 50 × 20 mm³, providing sufficient unit cells for thermally representative behavior while remaining compatible with the heating platform and insulation assembly. The unit cell size was chosen to balance manufacturing resolution with the characteristic length scale of heat transfer within the porous structure. Following fabrication, all specimens underwent stress-relief heat treatment at 300 °C for 2 hours to mitigate residual stresses from the layer-by-layer SLM process. Surface roughness was not further modified, as the as-built morphology was considered representative of practical thermal management applications.

The phase change material (PCM) was a commercial-grade paraffin wax with a nominal melting point of 42 °C and a latent heat of fusion of approximately 200 kJ/kg. The paraffin was chosen for its well-characterized thermal properties, chemical stability, negligible supercooling, and compatibility with aluminum alloy substrates. The PCM was vacuum-infused into the porous TPMS lattice at −0.09 MPa to ensure complete filling of interconnected void spaces. Each specimen was weighed before and after infiltration (±0.01 g), with PCM mass loading consistent within ±2% across all specimens.

### 2.2 Experimental Setup

The experimental apparatus comprised a constant-power resistive heating system, a thermocouple-based temperature measurement array, a multi-channel data acquisition system, and a thermal insulation enclosure. A flexible polyimide kapton heater matching the specimen footprint was bonded to the bottom surface using thermally conductive paste (> 1.5 W/(m·K)). The heater was driven by a regulated DC power supply delivering constant power levels of 10 W, 20 W, and 30 W, corresponding to heat fluxes of 4.0, 8.0, and 12.0 kW/m², respectively, spanning mild to aggressive thermal loading conditions relevant to electronics cooling applications.

Temperature was measured using nine Type-K (chromel–alumel) thermocouples (wire diameter 0.25 mm, bead diameter ~0.5 mm). The thermocouples were embedded at predetermined locations through small access holes (< 1 mm) drilled into the top surface, secured with high-temperature thermally conductive adhesive to ensure reliable contact throughout heating and melting cycles. The thermocouple arrangement is detailed in Section 2.3.

All signals were routed to a multi-channel data acquisition system (NI-9213, National Instruments) with cold-junction compensation, sampling all nine channels simultaneously at 1 Hz—sufficient to capture transient thermal response during both sensible heating and phase change. The system was calibrated against a NIST-traceable reference thermometer, with an overall measurement uncertainty of ±0.5 °C.

The assembly was enclosed in an insulation box constructed from 25 mm-thick extruded polystyrene (XPS) foam boards, with an inner lining of 10 mm-thick ceramic fiber blanket to suppress radiative heat losses at elevated temperatures. Preliminary calibration tests confirmed that lateral and top-surface heat losses remained below 3% of the total input power across all tested conditions. The bottom surface, in direct contact with the heater, was approximated as a uniform heat flux boundary condition, while the top and lateral surfaces were treated as nominally adiabatic within the insulation enclosure. All experiments were conducted in a temperature-controlled laboratory environment maintained at 23 ± 1 °C.

### 2.3 Thermocouple Layout

The nine thermocouples were arranged to capture the three-dimensional temperature distribution within the TPMS lattice and enable calculation of through-thickness temperature gradients, as illustrated in Fig. 1 (thermocouple_layout_3d.png) and Fig. 2 (thermocouple_layout_top.png).

Thermocouple T1 was positioned at the geometric center of the bottom surface (coordinates: (0, 0, 0) mm), directly above the heater element. This location represents the point of maximum thermal input and serves as the primary indicator of the local thermal state at the heat source interface, where the phase change process initiates first.

Thermocouples T2 through T5 were arranged in the middle layer at z = 10 mm, at the four corners of a 25 mm × 25 mm square centered on the specimen axis, with coordinates (±12.5, ±12.5, 10) mm. This array captured radial temperature variations in the mid-plane and provided an area-averaged middle-layer temperature.

Thermocouples T6 through T9 were placed on the top surface at z = 20 mm, at the midpoints of a 25 mm × 25 mm square. This top-layer array was rotated by 45° relative to the middle layer, creating a staggered configuration that enhances spatial sampling across the specimen volume by positioning top-surface sensors maximally offset from the mid-plane sensors.

### 2.4 Data Processing

The raw temperature data from all nine thermocouples were processed to extract representative thermal metrics for performance evaluation. Due to a sensor malfunction during the experimental campaign, thermocouple T4 (one of the four mid-plane sensors) produced unreliable readings and was excluded from all subsequent analyses. The remaining eight functional channels were organized into three measurement groups:

Group A comprised T1 at the bottom surface, representing the heater-side thermal response. Group B was the arithmetic average of T2, T3, and T5, providing a spatially averaged middle-layer temperature. Group C was represented by T9 on the top surface, selected over T6–T8 for its superior and most stable thermal contact with the lattice struts.

Two through-thickness temperature gradients were defined: the A–B gradient (ΔT_mid = T1 − T_B), representing the thermal drop across the middle layer; and the A–C gradient (ΔT_total = T1 − T9), representing the total thermal drop from the heated bottom to the top surface. These gradients indicate the effective thermal resistance of the TPMS lattice–PCM composite under transient heating.

A critical metric was the phase change window, defined as the time interval during which T1 remained within 42–52 °C. This 10 °C window encompasses the solid–liquid transition of the paraffin PCM and quantifies the duration and effectiveness of latent heat absorption. Phase change onset was identified when T1 first reached 42 °C, and completion when T1 exceeded 52 °C, indicating full melting of PCM near the heater. The phase change window duration serves as a primary indicator of the composite system's thermal energy storage capacity under each power level.
