"""Gyroid 30W NEW data check (2026-08-08)"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

df = load('temperature_record_20260808_203206.csv')

print("=" * 70)
print("GYROID 30W NEW 数据检查")
print("=" * 70)

print(f"\n[基本信息]")
print(f"行数: {len(df)}")
print(f"时长: {df.elapsed.iloc[-1]/60:.2f} min")
print(f"采样间隔: {df.elapsed.diff().median():.1f} s")
print(f"起始: {df.time.iloc[0]}")
print(f"结束: {df.time.iloc[-1]}")
print(f"T1末值: {df.T1.iloc[-1]:.1f}°C")
print(f"T1最大: {df.T1.max():.1f}°C")

# 检查中断
gaps = df.elapsed.diff()
big_gaps = gaps[gaps > 10]
print(f"\n[中断检查]")
print(f">10s中断: {len(big_gaps)} 个")

# 检查B组一致性
print(f"\n[B组一致性 (T2-T5)]")
for t1_val in [42, 45, 50]:
    i = df.T1.sub(t1_val).abs().idxmin()
    vals = df.loc[i, ['T2','T3','T4','T5']]
    spread = vals.max() - vals.min()
    print(f"  T1={t1_val}°C: spread={spread:.1f}°C  (T2={vals['T2']:.1f}, T3={vals['T3']:.1f}, T4={vals['T4']:.1f}, T5={vals['T5']:.1f})")

# 检查C组接触 (T1=45°C时相对T9偏差)
print(f"\n[C组接触检查 (T1=45°C)]")
i = df.T1.sub(45).abs().idxmin()
ref = df.T9.iloc[i]
print(f"  T9参考: {ref:.1f}°C")
for c in ['T6', 'T7', 'T8']:
    off = df[c].iloc[i] - ref
    print(f"  {c}: {df[c].iloc[i]:.1f}°C (偏差{off:+.1f}°C)")

# 到达42°C时间
print(f"\n[到达42°C时间]")
for c in ['T1', 'T2', 'T3', 'T4', 'T5', 'T9']:
    idx = df.loc[df[c] >= 42, 'elapsed']
    t = idx.iloc[0]/60 if len(idx) > 0 else np.nan
    print(f"  {c}: {t:.1f} min")

# A-B梯度 (C=T9)
print(f"\n[梯度随T1变化]")
print(f"{'T1(°C)':>8} | {'A-B':>8} | {'A-C':>8}")
for t1_val in [38, 40, 42, 44, 46, 48, 50, 52, 55]:
    i = df.T1.sub(t1_val).abs().idxmin()
    b_raw = df.loc[i, ['T2','T3','T4','T5']].mean()
    worst = np.abs(df.loc[i, ['T2','T3','T4','T5']] - b_raw).idxmax()
    b3 = df.loc[i, [c for c in ['T2','T3','T4','T5'] if c != worst]].mean()
    ab = df.T1.iloc[i] - b3
    ac = df.T1.iloc[i] - df.T9.iloc[i]
    print(f"{t1_val:>8} | {ab:>8.1f} | {ac:>8.1f}")

# 熔融时长
win = df.elapsed.loc[(df.T1 >= 42) & (df.T1 <= 52)]
dur = (win.iloc[-1] - win.iloc[0]) / 60 if len(win) > 0 else 0
print(f"\n[熔融时长 (T1 in 42-52°C)]")
print(f"  {dur:.1f} min")
