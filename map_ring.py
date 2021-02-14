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

#region load data
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
mask = df.applymap(type) != bool
d = {True: 'TRUE', False: 'FALSE'}
df = df.where(mask, df.replace(d))
rows = df.shape[0]
#endregion

#region select circle columns
df_dict_circle_1 = dict_start_end(df, 'Same_Owner_Contractor') # item1
#endregion

#region algorithm
list_xy = []
ix = 0

h_points_scale = 1.
v_points = 10
rise = 1.3

ring_fill(list_xy, df_dict_circle_1, 0., h_points_scale, v_points, rise, ix)
#endregion

#region linear output
# df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
# df_out['y'] = df_out['y'] + 3000
# df_out['group'] = df_out['item1'] + df_out['item2']
# df_out['item_group'] = df_out.apply(lambda i: i['item1'] if (i['x'] > i['xo']) | (i['segment'] == 5) else i['item2'], axis=1)
# #df_out['item_group'] = df_out.apply(lambda i: i['item1'] if (i['x'] < i['xo']) | (i['path'] == 6) else i['item_group'], axis=1)
# print(df_out)
# df_out.to_csv(os.path.dirname(__file__) + '/map_ring_linear.csv', encoding='utf-8', index=False)
#endregion

#region curved output
N = rows/(1./3.)
offset = 2.0-0.3
min_x = 0
import csv
with open(os.path.dirname(__file__) + '/map_ring_curve.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'group', 'item_group', 'item1', 'item2', 'segment', 'x', 'y', 'xt', 'yt', 'path'])
    for i in range(len(list_xy)):       
        # added columns
        group = list_xy[i].item1 + '_' + list_xy[i].item2
        item_group = ''
        if (list_xy[i].x > list_xy[i].xo) or (list_xy[i].segment == 5):
            item_group = list_xy[i].item1
        else:
            item_group = list_xy[i].item2
        
        t = list_xy[i].x
        v = list_xy[i].y + 10.
        angle = (2.*pi)*(((t-min_x)%(N))/(N))
        angle_deg = angle * 180./pi + (360*(2./3.))/2.

        angle_rotated = (abs(angle_deg-360.)+90.) % 360. 
        angle_new = angle_rotated * pi/180.

        o = offset

        x_out = (o+v)*cos(angle_new)
        y_out = (o+v)*sin(angle_new)

        #x_out, y_out = Rotate(x_out, y_out, 45., 0., 0.)

        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t, v, x_out, y_out, list_xy[i].path])
#endregion

print('finished')