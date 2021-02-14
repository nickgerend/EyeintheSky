# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import numpy as np
import os
from math import isnan, pi, sin, cos, sqrt, tan

class point:
    def __init__(self, index, item1, item2, segment, x, y, path, xo = 0.): 
        self.index = index
        self.item1 = item1
        self.item2 = item2
        self.segment = segment
        self.x = x
        self.y = y
        self.path = path
        self.xo = xo
    def to_dict(self):
        return {
            'index' : self.index,
            'item1' : self.item1,
            'item2' : self.item2,
            'segment' : self.segment,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'xo' : self.xo }

def dict_start_end(df, column, r=False):
    df_dict = df.groupby([column]).size()
    df_dict = df_dict.to_dict()
    start = 0
    end = 0
    if r:
        for key in reversed(tuple(df_dict)):
            end = df_dict[key] + start
            df_dict[key] = []
            df_dict[key].append(start) 
            df_dict[key].append(end)
            start = end
    else:
        for key in df_dict:
            end = df_dict[key] + start
            df_dict[key] = []
            df_dict[key].append(start) 
            df_dict[key].append(end)
            start = end
    return df_dict

def ring_fill(list_xy, dict_, shift, h_points_scale, v_points, rise, ix = 0):
    path = 1
    for key in dict_:
        x_start = dict_[key][0] + shift
        x_end = dict_[key][1] + shift
        h_points = int((x_end-x_start)*h_points_scale)
        h = np.linspace(x_start, x_end, num=h_points)
        hr = np.linspace(x_end, x_start, num=h_points)
        v = np.linspace(0., rise, num=v_points)
        vr = np.linspace(rise, 0., num=v_points)
        for i in range(len(h)):
            list_xy.append(point(ix, key, key, 1, h[i], 0., path))
            path += 1
            ix += 1
        for i in range(len(v)):
            list_xy.append(point(ix, key, key, 1, x_end, v[i], path))
            path += 1
            ix += 1
        for i in range(len(hr)):
            list_xy.append(point(ix, key, key, 1, hr[i], rise, path))
            path += 1
            ix += 1
        for i in range(len(vr)):
            list_xy.append(point(ix, key, key, 1, x_start, vr[i], path))
            path += 1
            ix += 1

def rescale(x, xmin, xmax, newmin, newmax):
    rescaled = (newmax-newmin)*((x-xmin)/(xmax-xmin))+newmin
    return rescaled

#region load data
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
rows = df.shape[0]
#endregion

#region select circle columns
column = 'Orbit'
df_dict_circle_1 = dict_start_end(df, column, True) # item1
#endregion

#region algorithm
list_xy = []
ix = 0

item1 = column
item2 = column
rise = -1.7
cutoff = 100.
#endregion

#region vertices
for key in df_dict_circle_1:
    x_start = df_dict_circle_1[key][0]
    x_end = df_dict_circle_1[key][1]
    c_i = (x_end-x_start)
    if c_i > cutoff:
        c_i = cutoff
    list_xy.append(point(ix, key, key, 1, x_start, 0., 1))
    list_xy.append(point(ix, key, key, 1, x_end, 0., 2))
    list_xy.append(point(ix, key, key, 1, x_end, rise, 3))
    list_xy.append(point(ix, key, key, 1, x_start, rise, 4))
    #list_xy.append(point(ix, key, key, 1, x_start, 0., 5))
    list_xy.append(point(ix, key, key, 1, x_start, rise/2., 5))
    list_xy.append(point(ix, key, key, 1, x_end-c_i, rise/2., 6))
    list_xy.append(point(ix, key, key, 1, x_start, rise/2., 7))
    list_xy.append(point(ix, key, key, 1, x_start, 0., 8))

for i in range(len(list_xy)):
    list_xy[i].x = rescale(list_xy[i].x, 0, rows, -10.4166666666667, 10.4166666666667)
#endregion

#region linear output
df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
df_out['xt'] = df_out['x']
df_out['yt'] = df_out['y']
df_out['group'] = df_out['item1'] + df_out['item2']
df_out['item_group'] = df_out.apply(lambda i: i['item1'] if (i['x'] > i['xo']) | (i['segment'] == 5) else i['item2'], axis=1)
df_out.to_csv(os.path.dirname(__file__) + '/bottom_bar.csv', encoding='utf-8', index=False)
#endregion

print('finished')