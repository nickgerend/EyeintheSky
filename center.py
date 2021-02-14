# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

from scipy import interpolate
import pandas as pd
import numpy as np
import os
from math import isnan, pi, sin, cos, sqrt, tan
import matplotlib.pyplot as plt
import random

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

def Ellipse(x1, x2, half_height, points, upper=True):
    sign = 1.
    if not upper:
        sign = -1.
    width = abs(x2-x1)
    a = width/2.
    b = half_height
    x = np.linspace(-a, a, num=points)
    y = sign*(b/a)*np.sqrt(a**2-x**2)
    x += x1 + (x2-x1)/2.
    return list(zip(x,y))

def Ellipse_xy(x1, x2, height, points):
    width = abs(x2-x1)
    a = width/2
    b = height/2
    x = np.linspace(-a, a, num=points)
    angle = pi-(x+a)/(width)*pi
    u = np.tan(angle/2.)
    xt = a*(1-u**2)/(u**2+1)
    y = -2*b*u/(u**2+1)
    xt += x1 + (x2-x1)/2.
    return list(zip(xt,y))

def Rotate(x, y, angledeg, x_offset, y_offset):
    xa = x*cos(angledeg*pi/180) + y*sin(angledeg*pi/180)
    ya = -x*sin(angledeg*pi/180) + y*cos(angledeg*pi/180)
    xa -= x_offset
    ya -= y_offset
    return xa, ya

def dict_start_end(df, column):
    df_dict = df.groupby([column]).size().to_dict()
    start = 0
    end = 0
    for key in df_dict:
        end = df_dict[key] + start
        df_dict[key] = []
        df_dict[key].append(start) 
        df_dict[key].append(end)
        start = end
    return df_dict

#region load data
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
rows = df.shape[0]
#endregion

#region select circle columns
df_group_circle = df.groupby(['Purpose_Group', 'User_Group'], sort=False)
print(df_group_circle.size())
df_dict_circle_1 = dict_start_end(df, 'Purpose_Group') # item1
df_dict_circle_2 = dict_start_end(df, 'User_Group') # item 2
#endregion

#region algorithm
item_buffer = 200 #500
inner_buffer = 5
list_xy = []
height = 5
scale = 1.1
count = 101
m_count = 50
ix = 0
for items, row in df_group_circle:
    start1 = df_dict_circle_1[items[0]][0]
    start2 = -df_dict_circle_2[items[1]][0]
    end1 = start1 + int(row.count()[0])
    end2 = start2 + int(-row.count()[0])
    item_1_x1 = start1 + item_buffer/2
    item_2_x1 = start2 - item_buffer/2
    item_1_x2 = end1 + item_buffer/2
    item_2_x2 = end2 - item_buffer/2

    #--- vertices:
    # list_xy.append(point(ix, items[0], items[1], 1, item_1_x1, 0., 0))
    # list_xy.append(point(ix, items[0], items[1], 1, item_2_x1, 0., 1))
    # list_xy.append(point(ix, items[0], items[1], 2, item_1_x2, 0., 4))
    # list_xy.append(point(ix, items[0], items[1], 2, item_2_x2, 0., 3))
    #---

    #---
    h_scale = 1.1
    height1 = abs(item_1_x1-item_2_x1)/h_scale
    height2 = abs(item_1_x2-item_2_x2)/h_scale
    e1 = Ellipse_xy(item_1_x1, item_2_x1, height1, count)
    e2 = Ellipse_xy(item_1_x2, item_2_x2, height2, count)
    w1 = int(abs(item_1_x1-item_1_x2)/10)
    w2 = int(abs(item_2_x2-item_2_x1)/10)
    o1 = np.linspace(item_1_x1, item_1_x2, num=w1)
    o2 = np.linspace(item_2_x2, item_2_x1, num=w2)
    xo = (item_1_x1+item_2_x1)/2.
    y1 = np.min([i[1] for i in e1])
    y2 = np.min([i[1] for i in e2])
    m = Ellipse_xy(y1, y2, (abs(y2-y1)*100.)**0.5, m_count)
    i_count = 1
    for i in range(count):
        list_xy.append(point(ix, items[0], items[1], 1, e1[i][0], e1[i][1], i_count, xo))
        i_count += 1
    for i in range(w1):
        list_xy.append(point(ix, items[0], items[1], 2, o1[i], 0., i_count, xo))
        i_count += 1
    for i in range(count, 0, -1):
        list_xy.append(point(ix, items[0], items[1], 3, e2[i-1][0], e2[i-1][1], i_count, xo))
        i_count += 1
    for i in range(w2):
        list_xy.append(point(ix, items[0], items[1], 4, o2[i], 0., i_count, xo))
        i_count += 1
    for i in range(m_count):
        list_xy.append(point(ix, items[0], items[1], 5, xo + m[i][1], m[i][0], i_count, xo))
        i_count += 1
    for i in range(m_count, 0, -1):
        i_path = m_count-i+int(count/2.)+1
        list_xy.append(point(ix, items[0], items[1], 6, xo + m[i-1][1], m[i-1][0], i_path, xo))
        i_count += 1
    #---

    df_dict_circle_1[items[0]][0] = end1
    df_dict_circle_2[items[1]][0] = -end2
    ix += 1
#endregion

#region linear output
# df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
# df_out['x'] = df_out['x'] + rows + item_buffer
# df_out['xo'] = df_out['xo'] + rows + item_buffer
# df_out['y'] = df_out['y'] + 3000
# df_out['group'] = df_out['item1'] + df_out['item2']
# df_out['item_group'] = df_out.apply(lambda i: i['item1'] if (i['x'] > i['xo']) | (i['segment'] == 5) else i['item2'], axis=1)
# #df_out['item_group'] = df_out.apply(lambda i: i['item1'] if (i['x'] < i['xo']) | (i['path'] == 6) else i['item_group'], axis=1)
# print(df_out)
# df_out.to_csv(os.path.dirname(__file__) + '/center_linear.csv', encoding='utf-8', index=False)
#endregion

#region curved output
N = 2*rows + 2*item_buffer
offset = 1.0
min_x = 0
import csv
with open(os.path.dirname(__file__) + '/center_curve.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'group', 'item_group', 'item1', 'item2', 'segment', 'x', 'y', 'xt', 'yt', 'path'])
    for i in range(len(list_xy)):       
        # added columns
        group = list_xy[i].item1 + list_xy[i].item2
        item_group = ''
        if (list_xy[i].x > list_xy[i].xo) or (list_xy[i].segment == 5):
            item_group = list_xy[i].item1
        else:
            item_group = list_xy[i].item2
        
        t = list_xy[i].x + rows + item_buffer
        v = list_xy[i].y + 3000
        angle = (2.*pi)*(((t-min_x)%(N))/(N))
        angle_deg = angle * 180./pi
        angle_rotated = (abs(angle_deg-360.)+90.) % 360. 
        angle_new = angle_rotated * pi/180.

        o = offset

        x_out = (o+v)*cos(angle_new)
        y_out = (o+v)*sin(angle_new)

        x_out, y_out = Rotate(x_out, y_out, 45., 0., 0.)

        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t, v, x_out, y_out, list_xy[i].path])
#endregion

print('finished')