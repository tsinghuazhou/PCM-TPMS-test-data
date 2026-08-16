# Primitive vs Gyroid at 10W: Comparative Analysis

**Date**: 2026-08-05  
**Structures**: Primitive vs Gyroid TPMS (AlSi10Mg, L-PBF)  
**Heating Power**: 10W (both)  
**Data files**: 
- Gyroid: `tpms_gyroid10w_20260804_163501.csv` (1239 records, 25.38 min)
- Primitive: `tpms_primitive10w_20260805_200423.csv` (1377 records, 27.55 min)

---

## Executive Summary

Primitive TPMS exhibits **significantly poorer thermal performance** compared to Gyroid at 10W heating:
- **2× larger temperature gradients** (A-B: 13.42 vs 6.53°C; A-C: 43.33 vs 23.04°C)
- **Less uniform heat distribution** despite similar total energy absorption
- **T7 severe outlier** in Primitive (-19.8°C from group avg vs +4.6°C in Gyroid)
- **Shorter PCM melting plateau** (9.8 vs 10.8 min)

These findings suggest Primitive topology has **lower effective thermal conductivity** or **less efficient heat spreading pathways** compared to Gyroid.

---

## Key Findings

### 1. Temperature Gradients — Primitive is 2× Less Uniform

| Gradient | Gyroid | Primitive | Ratio |
|----------|--------|-----------|-------|
| A-B (heater to mid) | 6.53°C | 13.42°C | **2.06×** |
| A-C (heater to far) | 23.04°C | 43.33°C | **1.88×** |
| B-C (mid to far) | 16.51°C | 29.91°C | **1.81×** |

**Interpretation**: Primitive structure fails to distribute heat as effectively as Gyroid. The heater zone (T1) reaches much higher temperatures while the far field (C group) remains significantly cooler.

### 2. Peak Temperatures — Primitive Runs Hotter at Source, Cooler at Far Field

| Sensor | Gyroid | Primitive | Δ (P-G) |
|--------|--------|-----------|---------|
| T1 (A) | 93.77°C | **106.80°C** | **+13.03°C** |
| T2-T5 (B) | 87.2°C avg | 93.4°C avg | +6.2°C |
| T6 (C) | 52.80°C | **72.63°C** | **+19.83°C** |
| T7 (C) | 75.37°C | **48.33°C** | **-27.04°C** |
| T8-T9 (C) | 77.4°C avg | 68.9°C avg | -8.5°C |

**Critical observation**: T6 in Primitive is anomalously hot (+19.8°C vs Gyroid), while T7 is anomalously cold (-27.0°C). This suggests either:
- **Sensor issue**: T7 may be malfunctioning or poorly positioned
- **Structural cold spot**: Primitive geometry may create a localized low-conductivity zone near T7

### 3. Heating Rate — Primitive Heats Faster at Source, Slower at Periphery

First 5 minutes heating rate (°C/min, EMA smoothed):

| Sensor | Gyroid | Primitive | Δ |
|--------|--------|-----------|---|
| T1 | 4.03 | **4.23** | +0.21 |
| T2-T5 | 2.81 avg | 2.27 avg | **-0.54** |
| T6 | 1.24 | 1.15 | -0.10 |
| T7 | **2.21** | **0.51** | **-1.70** |
| T8-T9 | 2.32 avg | 1.46 avg | **-0.86** |

**Interpretation**: Heat concentrates near the source in Primitive, with slower propagation to B and C groups. T7's extremely low heating rate (0.51 vs 2.21 °C/min) confirms it's in a thermally isolated zone.

### 4. Time to Reach 42°C (PCM Melting Point)

| Sensor | Gyroid (s) | Primitive (s) | Δ (s) |
|--------|------------|---------------|-------|
| T1 | 147 | **104** | **-43** |
| T2 | 735 | 768 | +33 |
| T3 | 670 | 663 | -7 |
| T4 | 723 | 765 | +42 |
| T5 | 750 | 777 | +27 |
| T6 | 1151 | **1021** | **-130** |
| T7 | 939 | **1546** | **+607** |
| T8 | 875 | 906 | +31 |
| T9 | 910 | 943 | +33 |

**Anomalies**:
- T1 and T6 reach 42°C **faster** in Primitive (heat concentrates at source and T6 zone)
- T7 takes **607s longer** (10 min!) to reach 42°C in Primitive — confirms thermal isolation

### 5. PCM Melting Plateau

| Structure | Plateau Duration | T1 Range |
|-----------|------------------|----------|
| Gyroid | **10.8 min** (199–846s) | 44.8 → 50.2°C |
| Primitive | **9.8 min** (188–777s) | 47.6 → 54.5°C |

**Interpretation**: Gyroid maintains a longer phase-change plateau, indicating more effective PCM melting and thermal energy storage. Primitive's shorter plateau suggests less efficient latent heat utilization.

### 6. Energy Absorption — Similar Total, Different Distribution

| Metric | Gyroid | Primitive |
|--------|--------|-----------|
| T1 temperature rise | 67.45°C | **78.49°C** |
| Mean all-sensor rise | 54.22°C | 53.86°C |
| Ratio (T1 rise / mean rise) | 1.24 | **1.46** |

**Key insight**: Both structures absorb similar total energy (mean rise ~54°C), but Primitive concentrates more heat at the source (T1 rise is 1.16× higher). The ratio of T1 rise to mean rise is 1.46 for Primitive vs 1.24 for Gyroid, confirming **poorer thermal homogenization**.

### 7. Group Uniformity (Within-Group Std at T1 Peak)

| Group | Gyroid std | Primitive std |
|-------|------------|---------------|
| B (T2-T5) | 0.25°C | 0.73°C |
| C (T6-T9) | 12.05°C | 13.36°C |

**Note**: Primitive C-group std is inflated by T7 outlier. Excluding T7, Primitive C-group std would be ~2.5°C, actually **better** than Gyroid. This suggests the T7 anomaly is a localized issue, not a global Primitive deficiency.

---

## T7 Anomaly — Deep Dive

### Comparison Across Experiments

| Metric | Gyroid T7 | Primitive T7 |
|--------|-----------|--------------|
| Mean temp | 46.37°C | **34.13°C** |
| Max temp | 75.37°C | **48.33°C** |
| Deviation from C avg (peak) | +4.64°C | **-19.81°C** |
| Heating rate (first 5 min) | 2.21°C/min | **0.51°C/min** |
| Time to 42°C | 939s | **1546s** |

### Hypotheses

1. **Sensor malfunction**: T7 may have poor thermal contact or calibration drift in Primitive experiment
2. **Structural cold spot**: Primitive geometry may create a low-conductivity zone near T7 location
3. **Assembly issue**: PCM may not fully fill the lattice near T7, creating an air gap

### Evidence For/Against

**For sensor issue**:
- T7 in Gyroid was slightly warm (+4.6°C), not cold
- T6, T8, T9 in Primitive are all reasonably warm
- Sudden change suggests experimental artifact

**For structural cold spot**:
- T7 is consistently cold throughout Primitive experiment (not just at peak)
- Heating rate is 4.3× slower than Gyroid T7
- If sensor were just poorly positioned, we'd expect more variability, not consistent low readings

**Recommendation**: Inspect T7 sensor placement and thermal contact in Primitive sample. If sensor is confirmed good, this is a **real structural effect** — Primitive topology may have inherent thermal isolation zones.

---

## Temporal Evolution — Group Averages Over Time

| Time | Gyroid A | Prim A | Δ | Gyroid B | Prim B | Δ | Gyroid C | Prim C | Δ |
|------|----------|--------|---|----------|--------|---|----------|--------|---|
| 5 min | 46.5°C | 49.5°C | +3.0 | 40.5°C | 39.9°C | -0.5 | 36.6°C | 33.7°C | -2.9 |
| 10 min | 47.8°C | 51.4°C | +3.6 | 41.5°C | 41.0°C | -0.5 | 38.2°C | 34.9°C | -3.2 |
| 15 min | 54.2°C | 63.4°C | **+9.2** | 48.0°C | 52.8°C | +4.8 | 40.3°C | 38.6°C | -1.7 |
| 20 min | 75.1°C | 83.7°C | **+8.6** | 68.7°C | 71.9°C | +3.2 | 57.1°C | 49.1°C | **-8.1** |
| 25 min | 92.6°C | 100.9°C | **+8.4** | 86.1°C | 88.1°C | +2.0 | 69.9°C | 60.2°C | **-9.7** |

**Pattern**: 
- A group (heater) in Primitive runs **8–9°C hotter** after 15+ minutes
- B group runs slightly hotter (+2–5°C)
- C group runs **3–10°C cooler** (diverging over time)

This confirms Primitive's heat stays concentrated near the source and doesn't propagate as effectively to the far field.

---

## Conclusions for Paper

### 1. Gyroid Outperforms Primitive in Thermal Homogenization

At 10W heating, Gyroid TPMS achieves **significantly more uniform temperature distribution**:
- 2× smaller thermal gradients (A-B, A-C, B-C)
- Longer PCM melting plateau (10.8 vs 9.8 min)
- More effective heat spreading from source to far field

### 2. Primitive Shows Poorer Effective Thermal Conductivity

Despite similar total energy absorption, Primitive concentrates heat near the source:
- T1 rises 16% more for same input power
- B and C groups heat more slowly
- Temperature gradients are 1.8–2.1× larger

This suggests Primitive's bicontinuous but simpler cubic geometry provides **less efficient heat conduction pathways** compared to Gyroid's zero-mean-curvature, triply-periodic surface.

### 3. T7 Anomaly Requires Investigation

The severe T7 outlier in Primitive (-19.8°C from group avg) is either:
- **Experimental artifact** (sensor issue) — needs verification
- **Structural cold spot** — would be a novel finding suggesting Primitive topology has inherent thermal isolation zones

If confirmed as structural, this would be a **significant discovery** for TPMS design: topology affects not just average performance but also spatial uniformity.

### 4. Implications for TPMS Heat Exchanger Design

For applications requiring **uniform temperature distribution** (electronics cooling, battery thermal management):
- **Gyroid is superior** to Primitive
- Primitive may be acceptable for applications where heat concentration at source is acceptable

For applications requiring **maximum heat storage capacity**:
- Both topologies perform similarly (mean rise ~54°C)
- Gyroid achieves this with better uniformity

### 5. Recommendations for Future Work

1. **Verify T7 sensor** in Primitive sample — rule out experimental artifact
2. **Repeat Primitive experiment** with different sensor placement to confirm T7 anomaly
3. **CFD simulation** of Primitive vs Gyroid to understand heat flow pathways
4. **Test at higher power** (20W, 30W) to see if differences amplify or diminish
5. **Measure effective thermal conductivity** of both structures independently

---

## Generated Files

- `compare_primitive_vs_gyroid_10w.py` — detailed comparison script
- `report_primitive_vs_gyroid_10w.md` — this report
- `stats_primitive10w_20260805.csv` — Primitive sensor statistics
- `output/paper/figures/fig_primitive_10w_*.png/pdf` — Primitive temperature curves and summary plots

---

**Bottom line**: Gyroid TPMS is a **better thermal management structure** than Primitive at 10W, achieving more uniform temperatures and more effective PCM melting. The T7 anomaly in Primitive is a critical finding that warrants further investigation — it may reveal topology-dependent thermal isolation zones.
