"""Gyroid 新旧数据综合对比 (10W + 20W)"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

def b3_avg(df):
    raw = df[['T2','T3','T4','T5']].mean(axis=1)
    worst = np.abs(df[['T2','T3','T4','T5']].subtract(raw, axis=0)).mean(axis=0).idxmax()
    return df[[c for c in ['T2','T3','T4','T5'] if c != worst]].mean(axis=1), worst

# Load all
g10_old = load('temperature_record_20260804_163501.csv')
g10_new = load('temperature_record_20260808_165138gyroid10w.csv')
g20_old = load('temperature_record_20260731_195755.csv')
g20_new = load('temperature_record_20260808_190451 (4).csv')

b10_old, _ = b3_avg(g10_old)
b10_new, _ = b3_avg(g10_new)
b20_old, _ = b3_avg(g20_old)
b20_new, _ = b3_avg(g20_new)

print("=" * 80)
print("GYROID 新旧数据综合对比")
print("=" * 80)

print("\n[1] 数据概况")
print(f"{'数据集':<20} | {'时长(min)':>10} | {'T1末值':>10} | {'B组spread':>12}")
for name, df, b in [('Gyroid 10W OLD', g10_old, b10_old),
                     ('Gyroid 10W NEW', g10_new, b10_new),
                     ('Gyroid 20W OLD', g20_old, b20_old),
                     ('Gyroid 20W NEW', g20_new, b20_new)]:
    dur = df.elapsed.iloc[-1] / 60
    t1_end = df.T1.iloc[-1]
    # B组spread at T1=45C
    i = df.T1.sub(45).abs().idxmin()
    spread = df.loc[i, ['T2','T3','T4','T5']].max() - df.loc[i, ['T2','T3','T4','T5']].min()
    print(f"{name:<20} | {dur:>10.1f} | {t1_end:>10.1f} | {spread:>12.1f}")

print("\n[2] A-B 梯度对比 (T1=42°C, 50°C, 55°C)")
print(f"{'T1 (C)':>8} | {'10W OLD':>10} | {'10W NEW':>10} | {'20W OLD':>10} | {'20W NEW':>10}")
for t1 in [42, 50, 55]:
    row = []
    for df, b in [(g10_old, b10_old), (g10_new, b10_new), (g20_old, b20_old), (g20_new, b20_new)]:
        i = df.T1.sub(t1).abs().idxmin()
        row.append(df.T1.iloc[i] - b.iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>10.1f} | {row[2]:>10.1f} | {row[3]:>10.1f}")

print("\n[3] A-C 梯度对比 (C=T9, T1=42°C, 50°C, 55°C)")
print(f"{'T1 (C)':>8} | {'10W OLD':>10} | {'10W NEW':>10} | {'20W OLD':>10} | {'20W NEW':>10}")
for t1 in [42, 50, 55]:
    row = []
    for df, b in [(g10_old, b10_old), (g10_new, b10_new), (g20_old, b20_old), (g20_new, b20_new)]:
        i = df.T1.sub(t1).abs().idxmin()
        row.append(df.T1.iloc[i] - df.T9.iloc[i])
    print(f"{t1:>8} | {row[0]:>10.1f} | {row[1]:>10.1f} | {row[2]:>10.1f} | {row[3]:>10.1f}")

print("\n[4] 熔融持续时间 (T1 in 42-52°C)")
for name, df in [('10W OLD', g10_old), ('10W NEW', g10_new), ('20W OLD', g20_old), ('20W NEW', g20_new)]:
    win = df.elapsed.loc[(df.T1 >= 42) & (df.T1 <= 52)]
    dur = (win.iloc[-1] - win.iloc[0]) / 60 if len(win) > 0 else 0
    print(f"  {name:<10}: {dur:.1f} min")

print("\n[5] 到达 42°C 时间 (T1, B组均值, T9)")
print(f"{'sensor':>10} | {'10W OLD':>10} | {'10W NEW':>10} | {'20W OLD':>10} | {'20W NEW':>10}")
for c, b in [('T1', None), ('B', None), ('T9', None)]:
    row = []
    for df, b_avg in [(g10_old, b10_old), (g10_new, b10_new), (g20_old, b20_old), (g20_new, b20_new)]:
        if c == 'B':
            idx = b_avg.loc[b_avg >= 42, 'elapsed'] if hasattr(b_avg, 'loc') else df.elapsed.loc[df.T2 >= 42]
        else:
            idx = df.loc[df[c] >= 42, 'elapsed']
        row.append(idx.iloc[0]/60 if len(idx) > 0 else np.nan)
    print(f"{c:>10} | {row[0]:>10.1f} | {row[1]:>10.1f} | {row[2]:>10.1f} | {row[3]:>10.1f}")

print("\n[6] C组接触检查 (T1=45°C时相对T9偏差)")
print(f"{'sensor':>8} | {'10W OLD':>10} | {'10W NEW':>10} | {'20W OLD':>10} | {'20W NEW':>10}")
for c in ['T6', 'T7', 'T8']:
    row = []
    for df in [g10_old, g10_new, g20_old, g20_new]:
        i = df.T1.sub(45).abs().idxmin()
        row.append(df[c].iloc[i] - df.T9.iloc[i])
    print(f"{c:>8} | {row[0]:>+10.1f} | {row[1]:>+10.1f} | {row[2]:>+10.1f} | {row[3]:>+10.1f}")

print("\n[7] 关键差异总结")
print("10W: OLD vs NEW")
print("  - A-B梯度(42°C): 5.8 vs 4.2 (NEW小28%)")
print("  - 熔融时长: 12.1 vs 11.8 min (基本一致)")
print("  - C组接触: OLD仅T6离群(-5.4°C), NEW仅T7离群(-5.2°C)")
print("  - 结论: NEW数据质量略优，但两次高度可复现")
print()
print("20W: OLD vs NEW")
print("  - A-B梯度(42°C): 14.1 vs 8.8 (NEW小38%)")
print("  - A-B梯度(55°C): 29.0 vs 12.4 (NEW小57%)")
print("  - 熔融时长: 0.0 vs 2.2 min (OLD无法反映相变)")
print("  - C组接触: OLD偏高+3°C, NEW偏低-3~4°C (模式完全相反)")
print("  - 结论: OLD数据无效，NEW数据质量显著改善")
