# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import os

df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
df = df.groupby('Launch Site').size()
df.to_csv(os.path.dirname(__file__) + '/temp.csv', encoding='utf-8', index=False)