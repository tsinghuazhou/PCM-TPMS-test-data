import pandas as pd
import numpy as np

df = pd.read_csv('temperature_record_20260805_200423.csv')
df['时间戳'] = pd.to_datetime(df['时间戳'])
df['elapsed'] = (df['时间戳'] - df['时间戳'].iloc[0]).dt.total_seconds()

print("=" * 60)
print("PRIMITIVE TPMS - 10W Heating Analysis")
print("=" * 60)
print(f"Total records: {len(df)}")
print(f"Total duration: {df['elapsed'].iloc[-1]:.0f}s = {df['elapsed'].iloc[-1]/60:.2f}min")
print(f"Time range: {df['时间戳'].iloc[0]} → {df['时间戳'].iloc[-1]}")

# Find peak for each sensor
print("\n" + "=" * 60)
print("PEAK TEMPERATURES (Heating Phase)")
print("=" * 60)
peaks = {}
for col in ['T1','T2','T3','T4','T5','T6','T7','T8','T9']:
    idx = df[col].idxmax()
    peak_temp = df[col].iloc[idx]
    peak_time = df['elapsed'].iloc[idx]
    peaks[col] = {'temp': peak_temp, 'time': peak_time}
    print(f"{col}: {peak_temp:6.2f}°C at {peak_time:6.1f}s ({peak_time/60:5.2f}min)")

# Heating duration = time to T1 peak
heating_duration = peaks['T1']['time']
print(f"\n>>> Heating duration (T1 peak): {heating_duration:.0f}s = {heating_duration/60:.2f}min")
print(f">>> Total records during heating: {df[df['elapsed'] <= heating_duration].shape[0]}")

# Group analysis at peak time
print("\n" + "=" * 60)
print("GROUP TEMPERATURES AT T1 PEAK")
print("=" * 60)
peak_idx = df['T1'].idxmax()
groups = {'A': ['T1'], 'B': ['T2','T3','T4','T5'], 'C': ['T6','T7','T8','T9']}
group_temps = {}
for gname, cols in groups.items():
    temps = [df[c].iloc[peak_idx] for c in cols]
    avg = np.mean(temps)
    group_temps[gname] = avg
    print(f"Group {gname}: {', '.join([f'{t:.2f}' for t in temps])}°C → avg {avg:.2f}°C")

# Temperature differences
print("\n" + "=" * 60)
print("TEMPERATURE GRADIENTS")
print("=" * 60)
print(f"A-B difference: {group_temps['A'] - group_temps['B']:.2f}°C")
print(f"A-C difference: {group_temps['A'] - group_temps['C']:.2f}°C")
print(f"B-C difference: {group_temps['B'] - group_temps['C']:.2f}°C")

# Identify outliers (sensors that deviate >10°C from group avg)
print("\n" + "=" * 60)
print("OUTLIER DETECTION (>10°C from group avg at peak)")
print("=" * 60)
for gname, cols in groups.items():
    avg = group_temps[gname]
    for col in cols:
        temp = df[col].iloc[peak_idx]
        if abs(temp - avg) > 10:
            print(f"  {col} ({gname}): {temp:.2f}°C (deviation: {temp-avg:+.2f}°C)")

# Comparison with Gyroid 10W
print("\n" + "=" * 60)
print("COMPARISON: Primitive vs Gyroid (10W)")
print("=" * 60)
print(f"{'Metric':<30} {'Primitive':<15} {'Gyroid':<15}")
print("-" * 60)
print(f"{'Heating duration (min)':<30} {heating_duration/60:<15.2f} {'25.40':<15}")
print(f"{'T1 peak (°C)':<30} {peaks['T1']['temp']:<15.2f} {'93.77':<15}")
print(f"{'B group avg at T1 peak (°C)':<30} {group_temps['B']:<15.2f} {'87.27':<15}")
print(f"{'C group avg at T1 peak (°C)':<30} {group_temps['C']:<15.2f} {'76.65':<15}")
print(f"{'A-B gradient (°C)':<30} {group_temps['A']-group_temps['B']:<15.2f} {'6.50':<15}")
print(f"{'A-C gradient (°C)':<30} {group_temps['A']-group_temps['C']:<15.2f} {'17.12':<15}")

# Save comprehensive stats
stats_df = pd.DataFrame({
    'sensor': list(peaks.keys()),
    'peak_temp_C': [p['temp'] for p in peaks.values()],
    'peak_time_s': [p['time'] for p in peaks.values()],
    'peak_time_min': [p['time']/60 for p in peaks.values()]
})
stats_df.to_csv('stats_primitive_10w_heating.csv', index=False)
print(f"\nStats saved to stats_primitive_10w_heating.csv")
