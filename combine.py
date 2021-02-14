# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import numpy as np
import pandas as pd
import os

df_ac = pd.read_csv(os.path.dirname(__file__) + '/above_center_curve.csv')
df_c = pd.read_csv(os.path.dirname(__file__) + '/center_curve.csv')
df_bc = pd.read_csv(os.path.dirname(__file__) + '/below_center_curve.csv')
df_b = pd.read_csv(os.path.dirname(__file__) + '/bottom_curve.csv')
df_cr = pd.read_csv(os.path.dirname(__file__) + '/center_ring_curve.csv')
df_tb = pd.read_csv(os.path.dirname(__file__) + '/top_bar.csv')
df_bb = pd.read_csv(os.path.dirname(__file__) + '/bottom_bar.csv')
df_sl = pd.read_csv(os.path.dirname(__file__) + '/side_link_chart.csv')
df_curves = []

df_ac['yt'] = df_ac['yt']*-1.
df_ac['link'] = 'Year_Bin' + ' - ' + 'Purpose_Group'
df_ac['chart'] = 'Main'
df_curves.append(df_ac)

df_c['xt'] = df_c['xt']/213.
df_c['yt'] = df_c['yt']/213.
df_c['link'] = 'Purpose_Group' + ' - ' + 'User_Group'
df_c['chart'] = 'Main'
df_curves.append(df_c)

df_bc['xt'] = df_bc['xt']*-1.
df_bc['link'] = 'User_Group' + ' - ' + 'Orbit'
df_bc['chart'] = 'Main'
df_curves.append(df_bc)

df_b['xt'] = df_b['xt']/2.+0.05
df_b['yt'] = -1.*df_b['yt']/2. - 44. - 1.4
df_b['link'] = 'Orbit'
df_b = df_b.loc[(df_b['segment'] != 5) & (df_b['segment'] != 6)].reset_index(drop = True)
df_b = df_b.loc[(df_b['yt'] <= -39.7)].reset_index(drop = True)
df_b['chart'] = 'Main'
df_curves.append(df_b)

df_cr['xt'] = df_cr['xt']/213.
df_cr['yt'] = df_cr['yt']/213.
df_cr['link'] = 'Purpose_Group' + ' - ' + 'User_Group' + ' ' + 'Count'
df_cr['chart'] = 'Main'
df_curves.append(df_cr)

df_tb['xt'] = df_tb['xt']
df_tb['yt'] = df_tb['yt']+26.
df_tb['link'] = 'Year_Bin' + ' ' + 'Count'
df_tb['chart'] = 'Main'
df_curves.append(df_tb)

df_bb['xt'] = df_bb['xt']
df_bb['yt'] = df_bb['yt']-38.
df_bb['link'] = 'Orbit' + ' ' + 'Count'
df_bb['chart'] = 'Main'
df_curves.append(df_bb)

df_curves.append(df_sl)

df_combined = pd.concat(df_curves, axis=0)
#print(df_combined)
df_combined.to_csv(os.path.dirname(__file__) + '/link_chart.csv', encoding='utf-8', index=False)
print('finished')