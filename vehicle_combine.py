# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import os

df_vp = pd.read_csv(os.path.dirname(__file__) + '/vehicle_points.csv')
df_vt = pd.read_csv(os.path.dirname(__file__) + '/vehicle_title.csv', engine='python')

mask = df_vp.applymap(type) != bool
d = {True: 'TRUE', False: 'FALSE'}
df_vp = df_vp.where(mask, df_vp.replace(d))
df_curves = []

df_vp['chart'] = 'bottom'
df_curves.append(df_vp)

df_vt['chart'] = 'top'
df_curves.append(df_vt)

df_combined = pd.concat(df_curves, axis=0)
#print(df_combined)
df_combined.to_csv(os.path.dirname(__file__) + '/vehicle.csv', encoding='utf-8', index=False)
print('finished')