
import numpy, scipy, lxml, networkx, shapely, rtree, requests
import sympy, xxhash, msgpack, chardet, colorlog, svg.path
import jsonschema, collada, pyglet
import pyglet
#import glooey
import meshio
import skimage
import mapbox_earcut, psutil

import trimesh as trimesh
from trimesh.voxel.creation import local_voxelize


import numpy as np

import matplotlib.pyplot as plt





def createResolution(mymesh,width = 1024, height = 768, slices = 1200):
    
    
    reqRadius = ((radius/1)/2)
    print(reqRadius,'The radius')

    grid = trimesh.voxel.creation.local_voxelize(mymesh,width=1024,height =768, slices = 1200)#Input mesh, point, pitch, radius
    #pitch is the width of each vox, radius is the distance from the center to edge of the cube
    #Voxel radius consumes a lot of memory

    #grid.fill(method='base')


    gridMatrix = grid.matrix
    gridMatrix.shape
    print(grid.points)
    Points = grid.points_to_indices(grid.points)
    print(gridMatrix)
    print(Points)

    

    width = 1024
    height = 768
    slices = 1200

    #slices,height,width
    Resolution = np.zeros((slices,height,width))#Correct

    gridwidth = grid.shape[0]


    print(Resolution)
    offsetWidth = int((width-gridwidth)/2)+1
    offsetHeight = int((height-gridwidth)/2)+1


    minz = -1
    maxz = -1
 

    for (x, y, z) in Points:
        try: #x is z value
            Resolution[z][y+offsetHeight][x+offsetWidth]= 255
            if z < minz or minz ==-1:
                minz = z
            if z > maxz:
                maxz = z
        except:
            print('index out of range')
            pass



    return Resolution,minz,maxz, height, width


if __name__ == "__main__":  
    mymesh = trimesh.load_mesh(r'C:\Users\20kev\OneDrive\Documents\GitHub\DLPSlicerPrivate\Demostrations\ME59 - 1.25x1.25 [ORIGIN Centered update].STL'
    )
    createResolution(mymesh)
