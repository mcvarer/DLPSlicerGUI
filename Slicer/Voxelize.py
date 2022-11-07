
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

import ZipFolder
#https://trimsh.org/examples.section.html
from createResolution import createResolution




def start(mymesh,scale,num_slices=100):
   
      
   mymesh.apply_scale((scale,scale,(scale/4)*(1/5)))#Change the scaling of the mesh

   # middleZ = (mymesh.bounds[1][2] - mymesh.bounds[0][2])/2
   # middleY=(mymesh.bounds[1][1] - mymesh.bounds[0][1])/2
   # middleX=(mymesh.bounds[1][0] - mymesh.bounds[0][0])/2
   middleZ= mymesh.centroid[2]
   middleY= mymesh.centroid[1]
   middleX= mymesh.centroid[0]

   zSize = mymesh.bounds[1][2]-mymesh.bounds[0][2]
   ySize = mymesh.bounds[1][1]-mymesh.bounds[0][1]
   xSize = mymesh.bounds[1][0]-mymesh.bounds[0][0]




 
   Size = [zSize,ySize,xSize] #find out what is the maximum bounds so we know what radius needs to be
   print(mymesh.bounds)
   print("_")
   print(Size)
   print(mymesh.extents)
   
   return
   radius = max(mymesh.extents)

   print(middleX,middleY,middleZ)
   zScale = zSize/num_slices

   print(radius,zScale) 


   Resolution,minz,maxz, height, width = createResolution(mymesh,middleX=middleX,middleY=middleY,middleZ=middleZ,radius=radius)

   #Folder
   import os
   from ConvertToBmp import BMP
   from PIL import Image


   folder_name = input('Name folder')  
   dpi = input('enter dpi')
   if not os.path.isdir(folder_name):
      os.makedirs(folder_name)


   BMP(folder_name,Resolution,minz,maxz,height,width, dpi,num_slices=100,Reverse=False)


   ZipFolder.Zip('.\{}'.format(folder_name), folder_name)

if __name__ == "__main__": 
   print('start')
   mymesh = trimesh.load_mesh(r'C:\Users\20kev\Documents\GitHub\DLPSlicerPrivate\Demostrations\ME59 - 1x1 [ORIGIN Centered update].STL')
   print('starting to voxelize')

   start(mymesh,1)