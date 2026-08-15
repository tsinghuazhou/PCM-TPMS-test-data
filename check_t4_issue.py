"""验证T4在所有数据中的异常"""
import pandas as pd
import numpy as np

def load(path):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = ['time','T1','T2','T3','T4','T5','T6','T7','T8','T9']
    df['time'] = pd.to_datetime(df['time'])
    df['elapsed'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    return df

datasets = {
    'Gyroid 10W': 'temperature_record_20260808_165138gyroid10w.csv',
    'Gyroid 20W': 'temperature_record_20260808_190451 (4).csv',
    'Gyroid 30W': 'temperature_record_20260808_203206.csv',
}

print("T4 vs T2/T3/T5 对比 (到达42°C时间 & T1=45°C温度)")
print("=" * 70)

for name, path in datasets.items():
    df = load(path)
    print(f"\n[{name}]")
    # 到达42°C时间
    print(f"  到达42°C时间:")
    for c in ['T2','T3','T4','T5']:
        idx = df.loc[df[c] >= 42, 'elapsed']
        t = idx.iloc[0]/60 if len(idx) > 0 else np.nan
        print(f"    {c}: {t:.1f} min")
    # T1=45°C时温度
    i = df.T1.sub(45).abs().idxmin()
    print(f"  T1=45°C时:")
    for c in ['T2','T3','T4','T5']:
        print(f"    {c}: {df[c].iloc[i]:.1f}°C")
    # T4相对于T2/T3/T5均值的偏差
    t235_mean = df.loc[i, ['T2','T3','T5']].mean()
    t4_val = df.loc[i, 'T4']
    print(f"  T4 vs T2/T3/T5均值: {t4_val:.1f} vs {t235_mean:.1f} (偏差{t4_val-t235_mean:+.1f}°C)")
