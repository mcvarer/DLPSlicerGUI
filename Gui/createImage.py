from turtle import colormode
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from timeit import default_timer as timer

def stlImage(name):
    mymesh = trimesh.load_mesh('{}'.format(name))
    title = name.split("/")[-1]
    vertices = mymesh.vertices
    array = np.array(vertices)
    minZ = np.min(array[:,2])
    maxZ = np.max(array[:,2])
    print(title)





    slices = []

    for z in np.linspace(minZ, maxZ, 500):
        l = mymesh.section(plane_normal=[0,0,-1],plane_origin=[0, 0, z]
                            )

        slices.append(l)
        
    

    
    slices = [slice for slice in slices if slice is not None]


    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')



    for idx, slice in enumerate(slices):
        x = [slice.vertices[:,0]]
        y = [slice.vertices[:,1]]
        z = [slice.vertices[:,2]]




        ax.scatter(x, y, z,alpha=.04,linewidths=.5, s=1,marker='D',facecolors= 'dimgray') #Alpha is transparency


    ax.grid(False)
    ax.set_title(title)
    ax.set_zlabel('Z')
    fig.tight_layout()
    #Saves this into ImageSTL
    plt.savefig('./ImageSTL/file.png')
    print('done')




