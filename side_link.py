# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import os

def rescale(x, xmin, xmax, newmin, newmax):
    rescaled = (newmax-newmin)*((x-xmin)/(xmax-xmin))+newmin
    return rescaled

df_c = pd.read_csv(os.path.dirname(__file__) + '/center_linear.csv')
df_ac = pd.read_csv(os.path.dirname(__file__) + '/Year_Bin_Purpose_Group_Link.csv')
df_bc = pd.read_csv(os.path.dirname(__file__) + '/Orbit_User_Group.csv')
df_cr = pd.read_csv(os.path.dirname(__file__) + '/center_ring_linear.csv')
df_tb = pd.read_csv(os.path.dirname(__file__) + '/top_bar.csv')
df_bb = pd.read_csv(os.path.dirname(__file__) + '/bottom_bar.csv')
df_curves = []

df_c['xt'] = df_c['y']-3200.
df_c['yt'] = df_c['x']
df_c['link'] = 'Purpose_Group' + ' - ' + 'User_Group'
df_c['chart'] = 'Side'
df_c['xt'] = [rescale(x, -3000., 0., -2., 0.) for x in df_c['xt']]
df_curves.append(df_c)

df_ac['xt'] = df_ac['y']
df_ac['yt'] = df_ac['x']
df_c['link'] = 'Year_Bin' + ' - ' + 'Purpose_Group'
df_ac['chart'] = 'Side'
df_ac['yt'] = [rescale(x, 0., 1., 3087., 5874.) for x in df_ac['yt']]
df_curves.append(df_ac)

df_bc['xt'] = df_bc['y']
df_bc['yt'] = 1.-df_bc['x']
df_c['link'] = 'User_Group' + ' - ' + 'Orbit'
df_bc['chart'] = 'Side'
df_bc['yt'] = [rescale(x, 0., 1., 100., 2887.) for x in df_bc['yt']]
df_curves.append(df_bc)

df_cr['xt'] = df_cr['y']-3200.
df_cr['yt'] = df_cr['x']
df_cr['link'] = 'Purpose_Group' + ' - ' + 'User_Group' + ' ' + 'Count'
df_cr['chart'] = 'Side'
df_cr['xt'] = [rescale(x, -1500., 0., -1., 0.) for x in df_cr['xt']]
df_curves.append(df_cr)

df_tb['xt'] = df_tb['y']/14. + 1.
df_tb['yt'] = [rescale(x, -10.4166666666667, 10.4166666666667, 3087., 5874.) for x in df_tb['x']]
df_tb['link'] = 'Year_Bin' + ' ' + 'Count'
df_tb = df_tb.loc[(df_tb['path'] != 5) & (df_tb['path'] != 6) & (df_tb['path'] != 7)].reset_index(drop = True)
df_tb['chart'] = 'Side'
df_curves.append(df_tb)

df_bb['xt'] = -df_bb['y']/14. + 1.
df_bb['yt'] = [rescale(x, -10.4166666666667, 10.4166666666667, 100., 2887.) for x in df_bb['x']]
df_bb['link'] = 'Orbit' + ' ' + 'Count'
df_bb = df_bb.loc[(df_bb['path'] != 5) & (df_bb['path'] != 6) & (df_bb['path'] != 7)].reset_index(drop = True)
df_bb['chart'] = 'Side'
df_curves.append(df_bb)

df_combined = pd.concat(df_curves, axis=0)
#print(df_combined)
df_combined.to_csv(os.path.dirname(__file__) + '/side_link_chart.csv', encoding='utf-8', index=False)
print('finished')