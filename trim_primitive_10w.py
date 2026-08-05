import pandas as pd

df = pd.read_csv('temperature_record_20260805_200423.csv')
peak_idx = df['T1'].idxmax()
print('T1 peak: idx=%d, T1=%.2f, time=%s' % (peak_idx, df.loc[peak_idx,'T1'], df.loc[peak_idx,'时间戳']))

df_clean = df.iloc[:peak_idx+1].copy()
df_clean.to_csv('temperature_record_20260805_200423.csv', index=False)

df2 = pd.read_csv('temperature_record_20260805_200423.csv')
print('Saved: %d rows, last time=%s, T1 last=%.2f' % (len(df2), df2.iloc[-1,0], df2['T1'].iloc[-1]))
