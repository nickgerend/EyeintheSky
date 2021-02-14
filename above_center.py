# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import pandas as pd
import numpy as np
import os
from math import pi, exp, sqrt, log10, sin, cos, atan2
import random
import matplotlib.pyplot as plt

class point:
    def __init__(self, index, item1, item2, segment, x, y, path, y1 = 0., y2 = 0.): 
        self.index = index
        self.item1 = item1
        self.item2 = item2
        self.segment = segment
        self.x = x
        self.y = y
        self.path = path
        self.y1 = y1
        self.y2 = y2
    def to_dict(self):
        return {
            'index' : self.index,
            'item1' : self.item1,
            'item2' : self.item2,
            'segment' : self.segment,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'y1' : self.y1,
            'y2' : self.y2 }

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

def Ellipse_xy(x1, x2, height, points, sign=1.):
    width = abs(x2-x1)
    a = width/2
    b = height/2
    x = np.linspace(-a, a, num=points)
    angle = pi-(x+a)/(width)*pi
    u = np.tan(angle/2.)
    xt = a*(1-u**2)/(u**2+1)
    y = sign*2*b*u/(u**2+1)
    xt += x1 + (x2-x1)/2.
    return list(zip(xt,y))

def AngleByTwoPnts(x1, y1, x2, y2):
    return atan2(x2-x1, y2-y1)*180/pi - 90

def DistBtwTwoPnts(x1, y1, x2, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def Rotate(x, y, angledeg, x_offset, y_offset):
    xa = x*cos(angledeg*pi/180) + y*sin(angledeg*pi/180)
    ya = -x*sin(angledeg*pi/180) + y*cos(angledeg*pi/180)
    xa += x_offset
    ya += y_offset
    return xa, ya

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

def dict_start_end(df, column, factor = 1., start = 0.):
    df_dict = df.groupby([column]).size()/factor
    df_dict = df_dict.to_dict()
    #start = 0
    end = 0
    for key in df_dict:
        end = df_dict[key] + start
        df_dict[key] = []
        df_dict[key].append(start) 
        df_dict[key].append(end)
        start = end
    return df_dict

def rescale(x, xmin, xmax, newmin, newmax):
    rescaled = (newmax-newmin)*((x-xmin)/(xmax-xmin))+newmin
    return rescaled

def pinch(x, scale = 10.):
    p = x * log10(x)**scale
    return p

#region load data
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
rows = df.shape[0]
# mask = df.applymap(type) != bool
# d = {True: 'TRUE', False: 'FALSE'}
# df = df.where(mask, df.replace(d))

factor = 4.8 #2.4 is even, 4.8 half, 3.4 margin
inc = rows/2.-(rows/factor)/2.

df_group_circle = df.groupby(['Purpose_Group', 'Year_Bin'], sort=False)
df_dict_circle_1 = dict_start_end(df, 'Purpose_Group') # item1
df_dict_circle_2 = dict_start_end(df, 'Year_Bin', factor, inc) # item 2
#endregion

#region algorithm
y1 = 0.
y2 = 1000.

item_buffer = 200 #500
inner_buffer = 5
list_xy = []
height = 5
scale = 1.1
count = 5001
m_count = 50
ix = 0
for items, row in df_group_circle:
    start1 = df_dict_circle_1[items[0]][0]
    start2 = df_dict_circle_2[items[1]][0]
    end1 = start1 + int(row.count()[0])
    end2 = start2 + int(row.count()[0])/factor

    #--- vertices:
    # list_xy.append(point(ix, items[0], items[1], 1, start1, y1, 0))
    # list_xy.append(point(ix, items[0], items[1], 1, end1, y1, 1))
    # list_xy.append(point(ix, items[0], items[1], 2, start2, y2, 3))
    # list_xy.append(point(ix, items[0], items[1], 2, end2, y2, 2))
    #---

    s1 = sigmoid_xy(start1, y1, start2, y2, count, 'v', 8.)
    s2 = sigmoid_xy(end1, y1, end2, y2, count, 'v', 8.)

    w1 = int(abs(end2-start2)/10)
    w2 = int(abs(end1-start1)/10)
    o1 = np.linspace(start2, end2, num=w1)
    o2 = np.linspace(end1, start1, num=w2)
    yo = (y1+y2)/2.
    xo1 = s1[int(count/2)+1][0]
    xo2 = s2[int(count/2)+1][0]
    xo = (start2+end1)/2.
    xo = (xo1+xo2)/2.

    d1 = [DistBtwTwoPnts(xo, yo, point[0], point[1]) for point in s1]
    i1 = d1.index(min(d1))
    d2 = [DistBtwTwoPnts(xo, yo, point[0], point[1]) for point in s2]
    i2 = d2.index(min(d2))
    #i2 = count-i1-1
    e_dist = DistBtwTwoPnts(s1[i1][0], s1[i1][1], s2[i2][0], s2[i2][1])
    a = (AngleByTwoPnts(s1[i1][0], s1[i1][1], s2[i2][0], s2[i2][1]))

    mi = Ellipse_xy(0., e_dist, (abs(e_dist)*100.)**0.5, m_count, -1.)
    m = [Rotate(point[0], point[1], a, s1[i1][0], s1[i1][1]) for point in mi]

    i_count = 1
    for i in range(count):
        list_xy.append(point(ix, items[0], items[1], 1, s1[i][0], s1[i][1], i_count, m[0][1], m[m_count-1][1]))
        i_count += 1
    for i in range(w1):
        list_xy.append(point(ix, items[0], items[1], 2, o1[i], y2, i_count, m[0][1], m[m_count-1][1]))
        i_count += 1
    for i in range(count, 0, -1):
        list_xy.append(point(ix, items[0], items[1], 3, s2[i-1][0], s2[i-1][1], i_count, m[0][1], m[m_count-1][1]))
        i_count += 1
    for i in range(w2):
        list_xy.append(point(ix, items[0], items[1], 4, o2[i], y1, i_count, m[0][1], m[m_count-1][1]))
        i_count += 1
    for i in range(m_count):
        i_path = i+i1
        list_xy.append(point(ix, items[0], items[1], 5, m[i][0], m[i][1], i_path, m[0][1], m[m_count-1][1]))
    for i in range(m_count):
        i_path = (m_count+i_count)-i
        list_xy.append(point(ix, items[0], items[1], 6, m[i][0], m[i][1], i_path, m[0][1], m[m_count-1][1]))
    #---

    df_dict_circle_1[items[0]][0] = end1
    df_dict_circle_2[items[1]][0] = end2
    ix += 1
#endregion

#region rescale
N = rows
ymax = 26.
ymin = 10.
xmax = 100.
yp = pinch(ymax)
for i in range(len(list_xy)):
    yi = list_xy[i].y
    yi1 = list_xy[i].y1
    yi2 = list_xy[i].y2
    yi = rescale(yi, 0., y2, ymin, ymax)
    yi1 = rescale(yi1, 0., y2, ymin, ymax)
    yi2 = rescale(yi2, 0., y2, ymin, ymax)

    yi = pinch(yi)
    yi = rescale(yi, ymin, yp, ymin, ymax)
    yi1 = pinch(yi1)
    yi1 = rescale(yi1, ymin, yp, ymin, ymax)
    yi2 = pinch(yi2)
    yi2 = rescale(yi2, ymin, yp, ymin, ymax)

    list_xy[i].y = yi
    list_xy[i].y1 = yi1
    list_xy[i].y2 = yi2

    xi = list_xy[i].x
    xi = (xmax)*(xi)/(N)
    list_xy[i].x = xi

#endregion

#region write linear
df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
df_out['group'] = df_out['item1'] + df_out['item2']
df_out['item_group'] = df_out.apply(lambda i: i['item2'] if (((i['y'] > i['y1']) & (i['segment'] == 1)) | ((i['y'] > i['y2']) & (i['segment'] == 3)) | (i['segment'] == 6) | (i['segment'] == 2)) & (i['segment'] != 5) else i['item1'], axis=1)
df_out.to_csv(os.path.dirname(__file__) + '/above_center_linear.csv', encoding='utf-8', index=False)
#endregion

#region write curved
item_buffer = 200
Ni = 2*rows + 2*item_buffer
xmax_scaled_to_center = xmax/rows
item_buffer_scaled_to_center = item_buffer*xmax_scaled_to_center
N = 2*xmax + 2.*item_buffer_scaled_to_center
offset_angle_scaled_to_center = (item_buffer_scaled_to_center/2./N)*360
y_range = ymax-ymin
x_shift = (xmax)/2.
offset = 1.0
min_x = -x_shift
import csv
with open(os.path.dirname(__file__) + '/above_center_curve.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'group', 'item_group', 'item1', 'item2', 'segment', 'x', 'y', 'xt', 'yt', 'path'])
    for i in range(len(list_xy)):       
        
        group = list_xy[i].item1+list_xy[i].item2
        item_group = ''
        if (((list_xy[i].y > list_xy[i].y1) and (list_xy[i].segment == 1)) or ((list_xy[i].y > list_xy[i].y2) and (list_xy[i].segment == 3)) or (list_xy[i].segment == 6) or (list_xy[i].segment == 2)) and (list_xy[i].segment != 5):
            item_group = list_xy[i].item2
        else:
            item_group = list_xy[i].item1

        t = list_xy[i].x-x_shift
        v = list_xy[i].y

        angle = (2.*pi)*(((t-min_x)%(N))/(N))
        angle_deg = angle * 180./pi

        #--
        angle_deg += 90. - 45. + offset_angle_scaled_to_center
        #--

        angle_rotated = (abs(angle_deg-360.)+90.) % 360. 
        angle_new = angle_rotated * pi/180.
        fade = (ymax-v)/y_range
        fade = x_curve(fade,1.,1.5)
        o = offset + 4.

        #6:
        #o = offset - 4.*offset*(t-min_x)/(N)
        #e:
        #o = offset - 1.*offset*(x_shift-t)/(N)

        x_out = (o+v)*cos(angle_new)*-1
        y_out = (o+v)*sin(angle_new)
        x_out = (1-fade)*t + (fade)*x_out
        y_out = -(1-fade)*v + (fade)*y_out
        writer.writerow([i+1, group, item_group, list_xy[i].item1, list_xy[i].item2, list_xy[i].segment, t+x_shift, v, x_out, y_out, list_xy[i].path])
#endregion

print('finished')