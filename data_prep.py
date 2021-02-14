# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import numpy as np
import os

#region load data
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020.csv')
rows = df.shape[0]
#endregion

# region data prep

#region outline
# top-down columns = 1.[Purpose], 2.[Date], 3.[Users], 4.[Owner/Contractor], 5.[Class of Orbit], 6.[Type of Orbit]
# title group columns = 1.[Launch Site], 2.[Launch Vehicle]
# data columns = [Apogee(km)], [Perigee(km)], [Period (minutes)], [Launch Mass (kg.)], [Dry Mass (kg.)], [Power (watts)]

# Top: ['Same_Owner_Contractor']-[Year]
# Above Center: [Year]-[Purpose_Group]
# Center: [Purpose_Group]-[User_Group]
# Below Center: [User_Group]-[Class of Orbit]
# Bottom: [Class of Orbit]-[Type of Orbit]
#endregion

df['Launch Site'] = df['Launch Site'].str.strip()
df['Launch Vehicle'] = df['Launch Vehicle'].str.strip()

#region [Users] to [User_Group]
df['Users'] = df['Users'].str.strip()
#print(df['Users'].unique())
df['User_Group'] = [x if (x == 'Commercial') | (x == 'Civil') | (x == 'Military') | (x == 'Government') else 'Other' for x in df['Users']]
#print(df['User_Group'].unique())
#endregion

#region [Country of Operator/Owner]-[Country of Contractor] to [Same_Owner_Contractor]
df['Country of Operator/Owner'] = df['Country of Operator/Owner'].str.strip()
#print(df['Country of Operator/Owner'].unique())
df['Country of Contractor'] = df['Country of Contractor'].str.strip()
#print(df['Country of Contractor'].unique())
df['Country of Contractor'] = ['USA' if (x == 'SpaceX') else x for x in df['Country of Contractor']]
df['Same_Owner_Contractor'] = np.where(pd.isna(df['Country of Contractor']), 'Unknown', np.where(df['Country of Contractor'] == df['Country of Operator/Owner'], 'True', 'False'))
#print(df.groupby(['Same_Owner_Contractor']).size())
#endregion

#region [Purpose_Group]
df['Purpose'] = df['Purpose'].str.strip()
df['Purpose'] = ['Earth_Space' if ('Earth' in x) | ('Space' in x) else x for x in df['Purpose']]
df['Purpose'] = ['Communications_Navigation' if ('Comm' in x) | ('Nav' in x) else x for x in df['Purpose']]
df['Purpose_Group'] = ['Technology_Other' if (x != 'Earth_Space') & (x != 'Communications_Navigation') else x for x in df['Purpose']]
#print(df['Purpose_Group'].unique())
#endregion

#region [Year_Bin]
bins = [0, 2010, 2015, 2020]
df['Year'] = pd.DatetimeIndex(df['Date of Launch']).year
# s = df.groupby(pd.cut(df['Year'], bins=bins)).size()
df['Year_Bin'] = pd.cut(df['Year'], bins)
df1 = df.groupby(['Year_Bin', 'Purpose_Group'], sort=False).size().reset_index()
#print (df1)
#endregion

#region [Orbit]
df['Orbit'] = df['Class of Orbit'].str.strip()
# print(df['Orbit'].unique())
# print(df.groupby(['Orbit']).size())
#endregion

#endregion

#print(df)
df.to_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv', encoding='utf-8', index=False)
print('finished')