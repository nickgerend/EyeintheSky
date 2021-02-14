# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import numpy as np
import os
from math import isnan, pi, sin, cos, sqrt, tan, exp, log10

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

def dict_start_end(df, column, x_start, x_end, y_start, y_end, r=False):
    df_dict = df.groupby([column]).size()
    df_dict = df_dict.to_dict()
    x = np.linspace(x_start, x_end, num=len(df_dict))
    y = np.linspace(y_start, y_end, num=len(df_dict))
    i = 0
    if r:
        for key in reversed(tuple(df_dict)):
            count = df_dict[key]
            df_dict[key] = []
            df_dict[key].append(x[i])
            df_dict[key].append(y[i])
            df_dict[key].append(count)
            i += 1
    else:
        for key in df_dict:
            count = df_dict[key]
            df_dict[key] = []
            df_dict[key].append(x[i])
            df_dict[key].append(y[i])
            df_dict[key].append(count)
            i += 1
    return df_dict

def sigmoid_xy(x1, y1, x2, y2, points, orientation = 'h', limit = 6):
    x_1 = x1
    y_1 = y1
    x_2 = x2
    y_2 = y2
    if orientation == 'v':
        x1 = y_1
        y1 = x_1
        x2 = y_2
        y2 = x_2
    x = []
    y = []
    amin = 1./(1.+exp(limit))
    amax = 1./(1.+exp(-limit))
    da = amax-amin
    for i in range(points):
        i += 1
        xi = (i-1.)*((2.*limit)/(points-1.))-limit
        yi = ((1.0/(1.0+exp(-xi)))-amin)/da
        x.append((xi-(-limit))/(2.*limit)*(x2-x1)+x1)
        y.append((yi-(0.))/(1.)*(y2-y1)+y1)
    return { 'h': list(zip(x,y)), 'v': list(zip(y,x))}.get(orientation, None)

def x_curve(x, max_x, scale):
    half_x = max_x/2.
    # if x == 0 or x == half_x or x == max_x:
    #     return x
    rem = 0
    if x <= half_x:
        rem = x
    else:
        rem = max_x - x
    x_i = rem/half_x
    #x_curve = sqrt(1.-x_i**2.)
    x_curve = 1.-x_i**scale
    x_scale = half_x*x_curve
    if x <= half_x:
        return half_x-x_scale
    else:
        return half_x+x_scale

def rescale(x, xmin, xmax, newmin, newmax):
    rescaled = (newmax-newmin)*((x-xmin)/(xmax-xmin))+newmin
    return rescaled

def pinch(x, scale = 10., r=False):
    p = x * log10(x)**scale
    if r:
        p = 1/(x**scale)
    return p

#region data prep
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
mask = df.applymap(type) != bool
d = {True: 'TRUE', False: 'FALSE'}
df = df.where(mask, df.replace(d))
df_items = df.groupby('Launch Vehicle').size()
df['Vehicle Group'] = df['Launch Vehicle'].str.split(' ').str[0]
df['Vehicle Group'] = ['Long March' if i == 'Long' else i for i in df['Vehicle Group']]
df['Vehicle Group'] = ['Nanorack' if i == 'Nanoracks' else i for i in df['Vehicle Group']]
df['Vehicle Group'] = ['Space Shuttle' if i == 'Space' else i for i in df['Vehicle Group']]
df['Vehicle Group'] = ['Soyuz' if (i == 'Soyuz.2.1a/Fregat') | (i == 'Soyuz-Fregat(Soyuz') | (i == 'Soyuz-ST') | (i == 'Soyuz-Fregat') | (i == 'Soyuz-Fregat') | (i == 'Soyuz-ST-B') | (i == 'Soyuz-2.1b') else i for i in df['Vehicle Group']]
df['Vehicle Group'] = ['PSLV' if (i == 'PSLV-CA') | (i == 'PSLV-C29') | (i == 'PSLV-XL') | (i == 'PSLV-C27') | (i == 'PSLX-XL') else i for i in df['Vehicle Group']]
df['Vehicle Group'] = ['Minotaur' if (i == 'Minotaur-1') | (i == 'Minotaur-C') else i for i in df['Vehicle Group']]
df_sub_items = df.groupby('Vehicle Group').size()
#df.to_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv', encoding='utf-8', index=False)
#endregion

#region group setup
VG_y = 13.
p_true = [33.33/2., 2.]
p_false = [66.66+33.33/2., 2.]
SC_dict = {'TRUE': p_true, 'FALSE': p_false}
df_group_inner = df.groupby(['Same_Owner_Contractor', 'Launch Vehicle'], sort=False)
df_group_outer = df.groupby(['Launch Vehicle', 'Vehicle Group'], sort=False)
df_dict_V = dict_start_end(df, 'Launch Vehicle', 0.0, 100.0, 9.0, 9.0)
items = len(df_items)
sub_items = len(df_sub_items)
sub_start = (0.5-(sub_items/items)/2.)*100.
sub_end = (0.5+(sub_items/items)/2.)*100.
df_dict_VG = dict_start_end(df, 'Vehicle Group', sub_start, sub_end, VG_y, VG_y) #11.7
#endregion

#region algorithm
points = 50
list_xy = []
for items, row in df_group_inner:
    start_x = SC_dict[items[0]][0]
    start_y = SC_dict[items[0]][1]
    end_x = df_dict_V[items[1]][0]
    end_y = df_dict_V[items[1]][1]
    value = int(row.count()[0])
    s = sigmoid_xy(start_x, start_y, end_x, end_y, points, orientation = 'v')
    for i in range(len(s)):
        list_xy.append(point(0, items[0], items[1], value, s[i][0], s[i][1], i))
for items, row in df_group_outer:
    start_x = df_dict_V[items[0]][0]
    start_y = df_dict_V[items[0]][1]
    end_x = df_dict_VG[items[1]][0]
    end_y = df_dict_VG[items[1]][1]
    value = int(row.count()[0])
    s = sigmoid_xy(start_x, start_y, end_x, end_y, points, orientation = 'v')
    for i in range(len(s)):
        list_xy.append(point(0, items[0], items[1], value, s[i][0], s[i][1], i))
#endregion

#region test
# items = len(df_items)
# sub_items = len(df_sub_items)
# sub_start = (0.5-(sub_items/items)/2.)*100.
# sub_end = (0.5+(sub_items/items)/2.)*100.
# x = np.linspace(0.0, 100.0, num=items)
# y = np.linspace(8.0, 8.0, num=items)
# x2 = np.linspace(sub_start, sub_end, num=sub_items)
# y2 = np.linspace(11.7, 11.7, num=sub_items)

# list_xy = []
# list_xy.append(point(0, 'TRUE', 'TRUE', 1, p_true[0], p_true[1], 0))
# list_xy.append(point(0, 'FALSE', 'FALSE', 1, p_false[0], p_false[1], 0))

# i = 0
# df_group = df.groupby('Launch Vehicle')
# for name, row in df_group:
#     list_xy.append(point(i, name, name, 1, x[i], y[i], 0))
#     i += 1
# i = 0
# df_group2 = df.groupby('Vehicle Group')
# for name, row in df_group2:
#     list_xy.append(point(i, name, name, 2, x2[i], y2[i], 0))
#     i += 1
#endregion

#region curved output
N = 100.
#/(2./3.)
offset = 0.0
min_x = 0
import csv
with open(os.path.dirname(__file__) + '/vehicle_points.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'group', 'item_group', 'item1', 'item2', 'segment', 'x', 'y', 'xt', 'yt', 'path'])
    for i in range(len(list_xy)):       
        # added columns
        group = list_xy[i].item1 + '_' + list_xy[i].item2
        item_group = list_xy[i].item1
        
        t = list_xy[i].x
        v = list_xy[i].y
        angle = (2.*pi)*(((t-min_x)%(N))/(N))
        angle_deg = angle * 180./pi - 180. 
        #+ (360*(1./3.))/2.- 180.

        angle_rotated = (abs(angle_deg-360.)+90.) % 360. 
        angle_new = angle_rotated * pi/180.

        o = offset

        x_out = (o+v)*cos(angle_new)
        y_out = (o+v)*sin(angle_new)

        #x_out, y_out = Rotate(x_out, y_out, 45., 0., 0.)

        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t, v, x_out, y_out, list_xy[i].path])
#endregion

#region group setup 2
title_height = 30.
df_group_title = df.groupby(['Name of Satellite, Alternate Names', 'Vehicle Group'], sort=False)
df_dict_S = dict_start_end(df, 'Name of Satellite, Alternate Names', 48.0, 52.0, title_height, title_height) #45.0, 55.0
points = 50
list_xy = []
for items, row in df_group_title:
    start_x = df_dict_S[items[0]][0]
    start_y = df_dict_S[items[0]][1]
    end_x = df_dict_VG[items[1]][0]
    end_y = df_dict_VG[items[1]][1]
    value = int(row.count()[0])
    s = sigmoid_xy(start_x, start_y, end_x, end_y, points, orientation = 'v')
    for i in range(len(s)):
        list_xy.append(point(0, items[0], items[1], value, s[i][0], s[i][1], i))
#endregion

#region rescale
ymin = VG_y
xmax = 100.
y_range = title_height-ymin
ymax = title_height
pinch_scale1 = 2.
pinch_scale2 = 10.
yp_min1 = pinch(ymin,pinch_scale1,True)
yp_max1 = pinch(ymax,pinch_scale1,True)
yp_min2 = pinch(ymin,pinch_scale2)
yp_max2 = pinch(ymax,pinch_scale2)
for i in range(len(list_xy)):
    yi = list_xy[i].y
    # yi = pinch(yi,pinch_scale1,True)
    # yi = rescale(yi, yp_min1, yp_max1, ymin, ymax)
    yi = pinch(yi,pinch_scale2)
    yi = rescale(yi, yp_min2, yp_max2, ymin, ymax)
    list_xy[i].y = yi
#endregion

#region write title curved
N = xmax
x_shift = (xmax)/2.
offset = 0.0
min_x = -x_shift
import csv
with open(os.path.dirname(__file__) + '/vehicle_title.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'group', 'item_group', 'item1', 'item2', 'segment', 'x', 'y', 'xt', 'yt', 'path'])
    for i in range(len(list_xy)):       
        
        group = list_xy[i].item1+list_xy[i].item2
        item_group = list_xy[i].item1

        t = list_xy[i].x-x_shift
        v = list_xy[i].y

        angle = (2.*pi)*(((t-min_x)%(N))/(N))
        angle_deg = angle * 180./pi 

        angle_rotated = (abs(angle_deg-360.)+90.) % 360. 
        angle_new = angle_rotated * pi/180.
        fade = (ymax-v)/y_range
        fade = x_curve(fade,1.,1.5)
        o = offset

        x_out = (o+v)*cos(angle_new)*-1
        y_out = (o+v)*sin(angle_new)
        x_out = (1-fade)*t + (fade)*x_out
        y_out = -(1-fade)*v + (fade)*y_out
        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t+x_shift, v, x_out, -y_out, list_xy[i].path])
    
    title_height2 = 70. #50
    df_group_title = df.groupby(['Name of Satellite, Alternate Names'], sort=False)
    df_dict_S2 = dict_start_end(df, 'Name of Satellite, Alternate Names', 27.0, 68.0, title_height2, title_height2)
    points = 50
    list_xy = []
    for item, row in df_group_title:
        start_x = df_dict_S[item][0]
        start_y = df_dict_S[item][1]
        end_x = df_dict_S2[item][0]
        end_y = df_dict_S2[item][1]
        value = int(row.count()[0])
        s = sigmoid_xy(start_x, start_y, end_x, end_y, points, orientation = 'v')
        for i in range(len(s)):
            list_xy.append(point(0, item, item, value, s[i][0], s[i][1], i))
    ymin = title_height
    y_range = title_height2-title_height
    ymax = title_height2
    pinch_scale1 = 2.
    yp_min1 = pinch(ymin,pinch_scale1,True)
    yp_max1 = pinch(ymax,pinch_scale1,True)
    for i in range(len(list_xy)):
        yi = list_xy[i].y
        yi = pinch(yi,pinch_scale1,True)
        yi = rescale(yi, yp_min1, yp_max1, ymin, ymax)
        list_xy[i].y = yi
    for i in range(len(list_xy)):       
        group = list_xy[i].item1+list_xy[i].item2
        item_group = list_xy[i].item1
        t = list_xy[i].x
        v = list_xy[i].y
        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t, v, t-x_shift, v, -list_xy[i].path])
#endregion

print('finished')