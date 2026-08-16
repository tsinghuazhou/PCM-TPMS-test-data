# Gyroid vs Primitive at 20W: Comparative Analysis Report

**Date**: 2026-08-06  
**Analysis**: Power-dependent performance comparison between Gyroid and Primitive TPMS

---

## ⚠️ CRITICAL DATA QUALITY ISSUE

**The Gyroid 20W data (tpms_gyroid20w_20260731_195755.csv) shows strong evidence of poor heater-sample contact. The "performance reversal" conclusion is likely an experimental artifact and should NOT be used for design decisions until the experiment is repeated with verified contact quality.**

### Contact Quality Diagnostic

| Metric | Gyroid 10W | Gyroid 20W | Primitive 20W |
|--------|-----------|-----------|---------------|
| T1-B gap (2min, EMA) | **6.3°C** | **64.8°C** | 20.0°C |
| T1-B gap (1min) | 6.2°C | 64.4°C | 10.4°C |
| T1-B gap stability | Stable ~6°C | Stable ~65°C | Grows 10→25°C |
| T1 initial rate (60s) | 9.8°C/min | **71.4°C/min** | 11.9°C/min |
| T1/B rate ratio | 2.8x | **10.7x** | 9.7x |

### Why This Indicates Contact Problem

1. **Gap appears instantly and stays constant**: The 65°C T1-B gap is present at t=1min and remains ~65°C throughout. A topology-driven effect would show a growing gap as heat propagates; a contact resistance produces an immediate, constant offset.

2. **Same sample, different behavior**: The same Gyroid sample at 10W shows only a 6°C gap. The topology did not change—only the contact condition likely degraded over time or between experimental runs.

3. **T1 rises 7× faster than expected**: At 20W (only 2× power), T1 rises 71.4°C/min vs 9.8°C/min at 10W—a 7.3× rate increase for a 2× power increase. This is characteristic of heat accumulating at a contact interface rather than entering the sample.

4. **Primitive 20W shows normal behavior**: Primitive at 20W has a 20°C T1-B gap, which is reasonable and consistent with its 10W behavior (36.8°C A-C gradient). The problem is specific to the Gyroid 20W run.

### Impact on Conclusions

- The "performance reversal" finding (Primitive better than Gyroid at 20W) is **unreliable**
- The Gyroid 20W T1 value (144.7°C) likely reflects the heater surface temperature, not the sample temperature
- The B/C group data may also be affected (reduced heat input due to contact resistance)
- **All Gyroid 20W data should be considered invalid until the experiment is repeated**

---

## Data Summary

| Parameter | Gyroid 10W | Gyroid 20W | Primitive 20W |
|-----------|-----------|-----------|---------------|
| Data file | 20260804_163501.csv | 20260731_195755.csv | 20260806_162603.csv |
| Duration | 25.38 min | 11.12 min | 12.35 min |
| Energy input | 15.23 kJ | 13.34 kJ | 14.82 kJ |
| Contact quality | ✅ Good | ❌ Poor | ⚠️ Acceptable |
| Data validity | ✅ Valid | ❌ Invalid | ⚠️ Use with caution |

---

## Raw Data Comparison (For Reference Only)

**Note**: The Gyroid 20W data is presented here for completeness but should NOT be used for conclusions due to the contact issue identified above.

### Peak Temperatures (20W):

| Group | Gyroid 20W* | Primitive 20W | Difference |
|-------|--------|-----------|------------|
| A (T1, heater) | 144.7°C* | 113.0°C | Gyroid +31.7°C |
| B (mid layer) | 81.0°C* | 87.2°C | Primitive +6.2°C |
| C (top surface) | 78.9°C* | 67.0°C** | Gyroid +11.9°C |

*Gyroid 20W values are unreliable due to contact issue  
**Primitive C-group: only T7 usable (T6/T8/T9 have contact issues)

### Temperature Gradients (20W):

| Gradient | Gyroid 20W* | Primitive 20W | Ratio |
|----------|--------|-----------|-------|
| A-B (heater to mid) | 63.7°C* | 25.8°C | 2.47x |
| A-C (heater to top) | 65.8°C* | 45.9°C | 1.43x |
| B-C (mid to top) | 2.1°C* | 20.1°C | 0.10x |

*Gyroid 20W values are unreliable due to contact issue

### Comparison with Gyroid 10W (Valid Data):

| Metric | Gyroid 10W ✅ | Gyroid 20W ❌ | Primitive 20W ⚠️ |
|--------|-----------|-----------|---------------|
| T1 peak | 93.8°C | 144.7°C | 113.0°C |
| B group peak | 87.3°C | 81.0°C | 87.2°C |
| C group peak | 76.7°C | 78.9°C | 67.0°C |
| A-B gradient | 6.5°C | 63.7°C | 25.8°C |
| A-C gradient | 17.1°C | 65.8°C | 45.9°C |

---

## Valid Conclusions (Based on Reliable Data Only)

### What We CAN Say

1. **Gyroid outperforms Primitive at 10W** (valid data, both experiments good contact):
   - A-C gradient: 17.1°C vs 36.8°C (Gyroid 2× more uniform)
   - T1 peak: 93.8°C vs 106.8°C (Gyroid 13°C cooler)
   - This is consistent with literature (Casini 2024, Iticha 2025)

2. **Primitive 20W data appears reasonable** (with caveats):
   - T1-B gap of 20°C is within expected range
   - A-C gradient of 45.9°C is larger than Gyroid 10W (17.1°C), suggesting power-dependent effects
   - However, C-group data is unreliable (only T7 usable)

3. **Gyroid 20W data is invalid** and must be repeated:
   - 65°C T1-B gap indicates severe contact resistance
   - All temperature values are suspect
   - Cannot be used for topology comparison

### What We CANNOT Say

- ❌ "Primitive outperforms Gyroid at 20W" — based on invalid Gyroid data
- ❌ "There is a critical power threshold at ~15-17W" — based on invalid comparison
- ❌ "Gyroid creates thermal bottlenecks at high power" — contact issue, not topology
- ❌ Any design recommendations based on the 20W comparison

---

## Recommended Actions

### Immediate (Before Next Experiment)

1. **Improve heater-sample contact**:
   - Apply thermal paste/grease between heater and sample bottom surface
   - Use a spring-loaded fixture to apply uniform pressure
   - Consider using a thin thermally conductive pad (e.g., graphite sheet)

2. **Add contact quality verification**:
   - Measure T1-B gap at t=2min; if >15°C, abort and re-seat the sample
   - Use thermal imaging to verify uniform heater-sample interface temperature
   - Record contact pressure if possible

### Short-term (Next Experiments)

3. **Repeat Gyroid 20W** with verified contact:
   - Use the same sample if possible
   - Verify contact quality using the diagnostic above
   - Compare with Primitive 20W data

4. **Repeat Primitive 20W** with improved C-group contact:
   - T6/T8/T9 showed poor contact in this run
   - Verify all sensors before starting

5. **Run 15W experiments** for both topologies:
   - Will help identify if there is a genuine power-dependent effect
   - Use improved contact protocol

### Long-term

6. **CFD simulation** with contact resistance model:
   - Simulate the effect of contact resistance on T1 readings
   - Compare with experimental data to quantify the contact issue
   - Use validated model to predict true topology performance

7. **Consider alternative heating methods**:
   - Oil bath or oven heating for uniform boundary condition
   - Eliminate contact resistance entirely
   - Trade-off: slower heating, less practical for real applications

---

## Data Quality Notes

### Gyroid 10W (20260804):
- Contact quality: ✅ Good (T1-B gap = 6.3°C)
- All sensor groups reliable
- B-group: T3 removed as outlier
- C-group: T6 removed as outlier
- **Data validity: ✅ VALID**

### Gyroid 20W (20260731):
- Contact quality: ❌ Poor (T1-B gap = 64.8°C)
- T1 readings reflect heater surface, not sample
- B/C group data affected by reduced heat input
- **Data validity: ❌ INVALID — do not use for conclusions**

### Primitive 20W (20260806):
- Contact quality: ⚠️ Acceptable (T1-B gap = 20.0°C)
- A-group (T1): Reliable
- B-group: T3 removed as outlier
- C-group: **Only T7 reliable** (T6, T8, T9 have contact issues)
- **Data validity: ⚠️ PARTIAL — A and B groups usable, C group invalid**

---

## Appendix: Previous (Invalid) Analysis

The following analysis was performed before the contact issue was identified. It is preserved for reference but should NOT be used for conclusions.

### Previous Finding: "Power-Dependent Performance Reversal"

At 10W: Gyroid outperformed Primitive (A-C gradient 17.1°C vs 36.8°C)  
At 20W: Primitive appeared to outperform Gyroid (A-C gradient 45.9°C vs 65.8°C)

**This finding is now considered invalid** due to the Gyroid 20W contact issue. The 65.8°C A-C gradient in Gyroid 20W is a contact artifact, not a topology effect.

### Previous Hypothesis: "Thermal Bottleneck Mechanism"

The hypothesis that Gyroid's complex geometry creates thermal bottlenecks at high power is **not supported** by the valid data. The observed effect is explained by contact resistance.

---

**Report generated**: 2026-08-06 (updated)  
**Contact diagnostic script**: check_heater_contact.py  
**Analysis scripts**: compare_gyroid_primitive_20w.py, compare_primitive_10w_20w.py  
**Data files**: 
- Gyroid 10W: tpms_gyroid10w_20260804_163501.csv (✅ valid)
- Gyroid 20W: tpms_gyroid20w_20260731_195755.csv (❌ invalid)
- Primitive 20W: deprecated/tpms_primitive20w_20260806_162603.csv (⚠️ partial)
