import math

import numpy as np


# Returns a list of (x,y,z) tuples
def ParseVertices(fileName):
    xyz = []
    file = open(fileName, 'r')
    for line in file:
        lineContents = line.split();
        if lineContents[0] == 'v':
            xyz.append((float(lineContents[1]), float(lineContents[3]), float(lineContents[2])))
    return (xyz)


# Returns the 2D Cartesian Coordinates (x,y) in Polar Coordinates (rho,phi) in degrees
def CartToPol_Point(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x) * 180.0 / math.pi

    # Processing The Numericals
    if phi < 0:
        phi = 360 + phi
    rho = int(rho * 1000) / 1000
    phi = round(phi)

    return (rho, phi)


# Returns the 3D Cartesian Coordinates (x,y,z) in Cylindrical Coordinates (rho,phi,z) in degrees
def CartToCyl_Point(x, y, z):
    rho, phi = CartToPol_Point(x, y)
    return (rho, phi, z)


def CartToCyl(xyz_Cart):
    xyz_Cyl = []
    for x, y, z in xyz_Cart:
        xyz_Cyl.append(CartToCyl_Point((x, y, z)))
    return xyz_Cyl


def ZLayering(xyz_Cyl):
    xyz_Cyl = sorted(xyz_Cyl, key=lambda x: x[2])  # Sort With Respect to Z coordinates
    ZSet = set()
    ZList = []
    temp = []
    for rho, phi, z in xyz_Cyl:
        if z not in ZSet:
            ZList.append(temp)
            temp = [(rho, phi)]
            ZSet.add(z)
        else:
            temp.append((rho, phi))
    ZList.append(temp)
    ZList.remove([])
    ZListSorted = []
    for a in ZList:
        ZListSorted.append(sorted(a, key=lambda x: x[1]))  # Sort Each Z layer With Respect To Phi

    return ZListSorted


















x = []
y = []
Z = []
XYZ = []
print(ParseVertices('Cube.obj'))


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
    xxx, yyy = CartToPol_Point(xx, yy)
    xxx = int(xxx * 1000)/1000
    if zz not in ZSet:
        ZList.append(temp)
        temp = [(xxx,yyy)]
        ZSet.add(zz)
    else:
        temp.append((xxx, round(yyy)))
ZList.append(temp)
ZList.remove([])
ZListSorted = []
for a in ZList:
    ZListSorted.append(sorted(a, key= lambda  x : x[1]))
    print(sorted(a, key=lambda x: x[1]))
#print(ZListSorted)
PhiSamplingRate = 60
PhiSamples = list(range(0,360,PhiSamplingRate))
NormalizedPhiSamples = []
for layer in ZListSorted:
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





