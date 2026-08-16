import pandas as pd
import numpy as np

# Primitive 30W - 找到最高温度点
df = pd.read_csv('tpms_primitive30w_20260807_193935.csv', encoding='utf-8-sig')
max_idx = df['T1'].idxmax()
print(f'Primitive 30W T1 max temp: {df.loc[max_idx, "T1"]:.2f} at row {max_idx}')
print(f'Total rows: {len(df)}')
print(f'Rows to keep: {max_idx + 1}')
print()

# 显示最高点前后的数据
print('Data around max point:')
for i in range(max(0, max_idx-5), min(len(df), max_idx+10)):
    print(f'row {i}: T1={df.loc[i, "T1"]:.2f}')
