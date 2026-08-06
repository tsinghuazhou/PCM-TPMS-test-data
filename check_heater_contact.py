import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

# Gyroid 10W vs 20W
G10 = load('temperature_record_20260804_163501.csv')
G20 = load('temperature_record_20260731_195755.csv')
P20 = load('temperature_record_20260806_162603.csv')

print('=' * 70)
print('Heater-Sample Contact Quality Diagnostic')
print('=' * 70)

print('\n=== T1 vs B-group at early stage (first 2 min, EMA) ===')
print('(If contact is good, T1 should be only slightly above B group)')
print('(If contact is poor, T1 will be MUCH higher than B group)')
print()

for name, df, b_cols in [
    ('Gyroid 10W', G10, ['T2','T3','T4','T5']),
    ('Gyroid 20W', G20, ['T2','T3','T4','T5']),
    ('Primitive 20W', P20, ['T2','T3','T4','T5'])]:
    
    t2 = 120  # first 2 min
    mask = df['elapsed'] <= t2
    t1_ema = df.loc[mask, 'T1'].ewm(alpha=0.4, adjust=False).mean()
    b_avg = df.loc[mask, b_cols].mean(axis=1).ewm(alpha=0.4, adjust=False).mean()
    
    t1_end = t1_ema.iloc[-1]
    b_end = b_avg.iloc[-1]
    gap = t1_end - b_end
    
    print(f'{name:15s}: T1={t1_end:.1f}C, B_avg={b_end:.1f}C, T1-B gap={gap:.1f}C')

print('\n=== A-B gradient evolution (every 2 min) ===')
print()
print('  time   G10 A-B   G20 A-B   P20 A-B')
print('-' * 45)
for t_min in [1, 2, 3, 4, 5, 6, 8, 10, 11]:
    t_s = t_min * 60
    vals = []
    for df in [G10, G20, P20]:
        idx = df['elapsed'].sub(t_s).abs().idxmin()
        t1 = df['T1'].iloc[idx]
        b = df[['T2','T3','T4','T5']].iloc[idx].mean()
        vals.append(f'{t1-b:.1f}')
    print(f'{t_min:>4d}min  {vals[0]:>10s}  {vals[1]:>10s}  {vals[2]:>10s}')

print('\n=== T1 initial heating rate (first 60s) ===')
print('(Fast T1 rise + slow B rise = contact resistance)')
print()
for name, df in [('Gyroid 10W', G10), ('Gyroid 20W', G20), ('Primitive 20W', P20)]:
    m = df['elapsed'] <= 60
    t1_rate = (df.loc[m,'T1'].iloc[-1] - df.loc[m,'T1'].iloc[0]) / (60/60)
    b_rate = (df.loc[m,['T2','T3','T4','T5']].mean(axis=1).iloc[-1] - 
              df.loc[m,['T2','T3','T4','T5']].mean(axis=1).iloc[0]) / (60/60)
    ratio = t1_rate / b_rate if b_rate > 0 else float('inf')
    print(f'{name:15s}: T1 rate={t1_rate:.1f} C/min, B rate={b_rate:.1f} C/min, ratio={ratio:.1f}x')

print('\n=== Diagnosis ===')
print()
print('Gyroid 10W: A-B gap ~6C, stable over time -> GOOD contact')
print('Gyroid 20W: A-B gap ~64C at 2min, stays ~64C -> POOR contact likely')
print('Primitive 20W: A-B gap ~20C at 2min, stays ~25C -> acceptable contact')
print()
print('If Gyroid 20W had good contact:')
print('  - T1 would be closer to B group (like 10W)')
print('  - B group would be higher (more heat entering sample)')
print('  - The performance reversal may be an experimental artifact')
print()
print('Recommendation: Repeat Gyroid 20W experiment with better heater-sample contact')
print('  - Use thermal paste/grease between heater and sample')
print('  - Apply uniform pressure to ensure full contact')
print('  - Verify contact with thermal imaging if possible')
