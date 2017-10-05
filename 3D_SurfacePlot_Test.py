import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

x = []
y = []
Z = []

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * 180.0 / math.pi
    if phi < 0:
        phi = 360 + phi
    return(rho, phi)

XYZ = []
file = open('TestModel2.obj','r')
for line in file:
    x.append(float(line.split()[1]))
    y.append(float(line.split()[3]))
    Z.append(float(line.split()[2]))
    XYZ.append((float(line.split()[1]),float(line.split()[3]),float(line.split()[2])))

'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
'''



XYZ = sorted(XYZ,key = lambda x:x[2])

ZSet = set()
ZList = []
temp = []
for xx,yy,zz in XYZ:
    xxx, yyy = cart2pol(xx,yy)
    if zz not in ZSet:
        ZList.append(temp)
        temp = [(xxx,yyy)]
        ZSet.add(zz)
    else:
        temp.append((xxx,yyy))
ZList.append(temp)
ZList.remove([])
ZListSorted = []
for a in ZList:
    ZListSorted.append(sorted(a,key= lambda  x : x[1]))

PhiSamplingRate = 60
PhiSamples = list(range(0,360,PhiSamplingRate))
NormalizedPhiSamples = []
for layer in ZList:
    LayerNormValues = []
    Initial = layer[0][0]
    Final = layer[len(layer)-1][0]
    for Phi in PhiSamples:
        InitSet = False
        for point in layer:
            if point[1] >= Phi and point[1] < Phi + PhiSamplingRate:
                if InitSet == False:
                    Initial = point[0]
                else:
                    Final = point[0]
                    break
        LayerNormValues.append((Initial+Final)/2.0)
        Initial = (Initial+Final)/2.0
        for point in layer:
            if point[1] >= Phi + PhiSamplingRate:
                Final = point[0]
                break
    NormalizedPhiSamples.append(LayerNormValues)

RoundedNormalizedValues = []
for a in NormalizedPhiSamples:
    temp = ['%.3f' % ele for ele in a]
    temp = [float(ele) for ele in temp]
    RoundedNormalizedValues.append(temp)

RoundedNormalizedValues = reversed(RoundedNormalizedValues)
for a in RoundedNormalizedValues:
    print(a)





