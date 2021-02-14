# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import os

df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
# mask = df.applymap(type) != bool
# d = {True: 'TRUE', False: 'FALSE'}
# df = df.where(mask, df.replace(d))
df_LS_1 = df.groupby('Launch Site').size().to_frame('Count').reset_index().rename({'Launch Site': 'Item'}, axis=1)
df_UG_2 = df.groupby('User_Group').size().to_frame('Count').reset_index().rename({'User_Group': 'Item'}, axis=1)
df_SOC_3 = df.groupby('Same_Owner_Contractor').size().to_frame('Count').reset_index().rename({'Same_Owner_Contractor': 'Item'}, axis=1)
df_PG_4 = df.groupby('Purpose_Group').size().to_frame('Count').reset_index().rename({'Purpose_Group': 'Item'}, axis=1)
df_YB_5 = df.groupby('Year_Bin').size().to_frame('Count').reset_index().rename({'Year_Bin': 'Item'}, axis=1)
df_O_6 = df.groupby('Orbit').size().to_frame('Count').reset_index().rename({'Orbit': 'Item'}, axis=1)
df_LV_7 = df.groupby('Launch Vehicle').size().to_frame('Count').reset_index().rename({'Launch Vehicle': 'Item'}, axis=1)
df_VG_8 = df.groupby('Vehicle Group').size().to_frame('Count').reset_index().rename({'Vehicle Group': 'Item'}, axis=1)

dfs = []
dfs.append(df_LS_1)
dfs.append(df_UG_2)
dfs.append(df_SOC_3)
dfs.append(df_PG_4)
dfs.append(df_YB_5)
dfs.append(df_O_6)
dfs.append(df_LV_7)
dfs.append(df_VG_8)

df_combined = pd.concat(dfs, axis=0)
# df_combined.reset_index()
# df_combined.columns =['Item', 'Count']
#print(df_combined)

#df_combined.to_csv(os.path.dirname(__file__) + '/data_counts.csv', encoding='utf-8', index=False)
#df_combined.to_csv(os.path.dirname(__file__) + '/data_counts2.csv', encoding='utf-8', index=False)


df2 = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
mask = df2.applymap(type) != bool
d = {True: 'TRUE', False: 'FALSE'}
df2 = df2.where(mask, df2.replace(d))

df_group_PGYG = df2.groupby(['Purpose_Group', 'Year_Bin'], sort=False).size().to_frame('Count').reset_index().rename({'Purpose_Group': 'Item1', 'Year_Bin': 'Item2'}, axis=1)
df_group_PGUG = df2.groupby(['Purpose_Group', 'User_Group'], sort=False).size().to_frame('Count').reset_index().rename({'Purpose_Group': 'Item1', 'User_Group': 'Item2'}, axis=1)
df_group_UGO = df2.groupby(['User_Group', 'Orbit'], sort=False).size().to_frame('Count').reset_index().rename({'User_Group': 'Item1', 'Orbit': 'Item2'}, axis=1)
df_group_SOLS = df2.groupby(['Same_Owner_Contractor', 'Launch Site'], sort=False).size().to_frame('Count').reset_index().rename({'Same_Owner_Contractor': 'Item1', 'Launch Site': 'Item2'}, axis=1)

df_group_inner = df.groupby(['Same_Owner_Contractor', 'Launch Vehicle'], sort=False).size().to_frame('Count').reset_index().rename({'Same_Owner_Contractor': 'Item1', 'Launch Vehicle': 'Item2'}, axis=1)
df_group_outer = df.groupby(['Launch Vehicle', 'Vehicle Group'], sort=False).size().to_frame('Count').reset_index().rename({'Launch Vehicle': 'Item1', 'Vehicle Group': 'Item2'}, axis=1)


dfgs = []
dfgs.append(df_group_PGYG)
dfgs.append(df_group_PGUG)
dfgs.append(df_group_UGO)
dfgs.append(df_group_SOLS)
dfgs.append(df_group_inner)
dfgs.append(df_group_outer)
df_combined2 = pd.concat(dfgs, axis=0)
#print(df_combined2)

#df_combined2.to_csv(os.path.dirname(__file__) + '/data_group_counts.csv', encoding='utf-8', index=False)
df_combined2.to_csv(os.path.dirname(__file__) + '/data_group_counts2.csv', encoding='utf-8', index=False)
#print(df_combined2)