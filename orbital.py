# Written by: Nick Gerend, @dataoutsider
# Viz: "Eye in the Sky", enjoy!

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#region alias
cos = np.cos
sin = np.sin
pi = np.pi
dot = np.dot
#endregion

#region plot
fig = plt.figure(figsize=plt.figaspect(1))
ax = fig.add_subplot(111, projection='3d')
#endregion

class point:
    def __init__(self, index, item, x, y, z, path, value1=0., value2=0., value3=0.): 
        self.index = index
        self.item = item
        self.x = x
        self.y = y
        self.z = z
        self.path = path
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
    def to_dict(self):
        return {
            'index' : self.index,
            'item' : self.item,
            'x' : self.x,
            'y' : self.y,
            'z' : self.z,
            'path' : self.path,
            'value1' : self.value1,
            'value2' : self.value2,
            'value3' : self.value3 }

def earth():
    Earth_radius = 6371. # km
    coefs = (1, 1, 1)  
    rx, ry, rz = [Earth_radius/np.sqrt(coef) for coef in coefs]

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)

    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))

    x = np.reshape(x, -1)
    y = np.reshape(y, -1)
    z = np.reshape(z, -1)

    return list(zip(x,y,z))

def orbital(apogee, eccentricity=0, inclination=0, ascension=0, perigee=0):
    inc = inclination * pi / 180.
    M1 = np.matrix([ [0, cos(inc), -sin(inc)], [0, sin(inc), cos(inc)], [1, 0, 0] ])

    rotation = (ascension + perigee) * pi/180
    M2 = np.matrix([ [0, 0, 1], [cos(rotation), -sin(rotation), 0], [sin(rotation), cos(rotation), 0] ])    
    angle = np.linspace(0,2*pi, 182)
    r = (apogee * (1-eccentricity**2)) / (1 + eccentricity*cos(angle))

    xr = r*cos(angle)
    yr = r*sin(angle)
    zr = 0.

    pts = np.matrix(list(zip(xr,yr,zr)))
    pts =  (M1 * M2 * pts.T).T
    xr,yr,zr = pts[:,0].A.flatten(), pts[:,1].A.flatten(), pts[:,2].A.flatten()

    # ax.plot(xr, yr, zr, '-')
    # plt.show()

    return list(zip(xr,yr,zr))

#region orbits
df = pd.read_csv(os.path.dirname(__file__) + '/UCS-Satellite-Database-8-1-2020_Clean.csv')
df = df.replace(',','', regex=True)
list_xy = []
for j, row in df.iterrows():
    name = row['Name of Satellite, Alternate Names']
    ap = float(row['Apogee (km)'])
    pe = float(row['Perigee (km)'])
    ec = float(row['Eccentricity'])
    val1 = float(str(row['Dry Mass (kg.)']).replace('1500-1900', '1700'))
    val2 = float(str(row['Power (watts)']).replace(' (EOL)', '').replace(' (BOL)', ''))
    val3 = float(row['Expected Lifetime (yrs.)'])
    xyz = orbital(6371+ap, ec, 0.0, 0.0, 6371+pe)
    for i in range(len(xyz)):
        list_xy.append(point(j, name, xyz[i][0], xyz[i][1], xyz[i][2], i, val1, val2, val3))
#endregion

#region earth
earth_grid = earth()
for i in range(len(earth_grid)):
    list_xy.append(point(-1, 'earth', earth_grid[i][0], earth_grid[i][1], earth_grid[i][2], i))
#endregion

#region write data
import csv
with open(os.path.dirname(__file__) + '/orbital.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'item', 'x', 'y', 'z', 'path', 'Dry Mass (kg.)', 'Power (watts)', 'Expected Lifetime (yrs.)'])
    for i in range(len(list_xy)):       
        writer.writerow([i+1, list_xy[i].item, list_xy[i].x, list_xy[i].y, list_xy[i].z, list_xy[i].path, list_xy[i].value1, list_xy[i].value2, list_xy[i].value3])
#endregion

print('finished')