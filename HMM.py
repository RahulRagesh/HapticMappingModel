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
    for point in xyz_Cart:
        xyz_Cyl.append(CartToCyl_Point(point[0], point[1], point[2]))
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

    return reversed(ZListSorted)


for a in ZLayering(CartToCyl(ParseVertices("TestModel2.obj"))):
    print(a)
