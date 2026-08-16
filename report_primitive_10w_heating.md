# Primitive TPMS - 10W Heating Report

**Date**: 2026-08-05  
**Structure**: Primitive TPMS lattice (AlSi10Mg, L-PBF)  
**Heating Power**: 10W  
**Data file**: tpms_primitive10w_20260805_200423.csv  

## Summary

| Metric | Value |
|--------|-------|
| Total records | 1377 |
| Total duration | 27.55 min (1653 s) |
| Heating duration (to T1 peak) | 26.93 min (1616 s) |
| Initial temperature | ~28°C |

## Peak Temperatures

| Sensor | Peak (°C) | Time (min) |
|--------|-----------|------------|
| T1 (A) | 106.80 | 26.93 |
| T2 (B) | 92.66 | 26.93 |
| T3 (B) | 94.37 | 26.93 |
| T4 (B) | 93.05 | 26.93 |
| T5 (B) | 93.45 | 26.93 |
| T6 (C) | 72.63 | 26.73 |
| T7 (C) | 48.33 | 26.95 |
| T8 (C) | 70.25 | 26.93 |
| T9 (C) | 67.54 | 26.93 |

## Group Averages at T1 Peak

| Group | Sensors | Avg Temp (°C) |
|-------|---------|---------------|
| A | T1 | 106.80 |
| B | T2-T5 | 93.38 |
| C | T6-T9 | 63.47 |

## Temperature Gradients

| Gradient | Value (°C) |
|----------|------------|
| A-B | 13.42 |
| A-C | 43.33 |
| B-C | 29.91 |

## Outliers

- **T7**: 43.66°C at peak (deviation: -19.81°C from C group avg)  
  → Significant outlier; may indicate sensor issue or cold spot in Primitive structure

## Comparison: Primitive vs Gyroid (10W)

| Metric | Primitive | Gyroid | Difference |
|--------|-----------|--------|------------|
| Heating duration (min) | 26.93 | 25.40 | +6.0% |
| T1 peak (°C) | 106.80 | 93.77 | +13.9% |
| B group avg (°C) | 93.38 | 87.27 | +7.0% |
| C group avg (°C) | 63.47 | 76.65 | -17.2% |
| A-B gradient (°C) | 13.42 | 6.50 | +106% |
| A-C gradient (°C) | 43.33 | 17.12 | +153% |

## Key Findings

1. **Longer heating duration**: Primitive takes ~6% longer to reach T1 peak (26.93 vs 25.40 min)
2. **Higher T1 peak**: Primitive T1 reaches 106.80°C vs Gyroid 93.77°C (+13°C)
3. **Poorer thermal uniformity**: 
   - A-B gradient is 2× larger (13.42 vs 6.50°C)
   - A-C gradient is 2.5× larger (43.33 vs 17.12°C)
4. **Lower C group temperature**: Primitive C group averages 63.47°C vs Gyroid 76.65°C (-13°C)
5. **T7 outlier**: 43.66°C is ~20°C below C group average — possible sensor issue or structural cold spot

## Interpretation

The Primitive TPMS structure exhibits **worse thermal performance** than Gyroid at 10W:
- Higher thermal gradients suggest lower effective thermal conductivity
- Heat is less effectively distributed from the heater (T1) to the far field (C group)
- The structure may have higher thermal resistance or less efficient heat spreading pathways

This is consistent with the geometric differences: Gyroid's bicontinuous, zero-mean-curvature surface may provide more efficient heat conduction paths than Primitive's simpler cubic geometry.

## Generated Files

- `stats_primitive10w_20260805.csv` — sensor-level statistics
- `output/paper/figures/fig_primitive_10w_temperature_curves.png/pdf` — temperature curves
- `output/paper/figures/fig_primitive_10w_summary.png/pdf` — summary comparison plots
