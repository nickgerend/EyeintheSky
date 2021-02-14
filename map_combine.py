# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import os

df_lc = pd.read_csv(os.path.dirname(__file__) + '/launch_curve.csv')
df_mb = pd.read_csv(os.path.dirname(__file__) + '/map_base.csv')
df_mr = pd.read_csv(os.path.dirname(__file__) + '/map_ring_curve.csv')
df_bl = pd.read_csv(os.path.dirname(__file__) + '/map_base_link.csv')
mask = df_mr.applymap(type) != bool
d = {True: 'TRUE', False: 'FALSE'}
df_mr = df_mr.where(mask, df_mr.replace(d))
df_curves = []

offset = 35. #28.34
df_lc = df_lc.loc[(df_lc['yt'] >= -offset)]
df_curves.append(df_lc)

df_mb['yt'] = df_mb['yt']-offset-4.0/3.
df_curves.append(df_mb)

df_bl['yt'] = df_bl['yt']-offset-4.0/3.
df_curves.append(df_bl)

df_curves.append(df_mr)

df_combined = pd.concat(df_curves, axis=0)
df_combined.to_csv(os.path.dirname(__file__) + '/launch.csv', encoding='utf-8', index=False)
print('finished')