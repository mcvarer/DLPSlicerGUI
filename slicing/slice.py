from multiprocessing.sharedctypes import Value
from trimesh import Trimesh
import trimesh as trimesh
from numpy import ndarray
from trimesh.voxel.creation import voxelize_subdivide
from trimesh.voxel.creation import local_voxelize
from trimesh import transformations as tr
from trimesh.voxel import base
import numpy as np
from scipy import ndimage
from math import ceil, floor


def getSlices(mesh : Trimesh, num_layers: int, stl_unit_resolution: float=1, scale : tuple = (1, 1, 1), rotation : tuple = (0,0,0), allow_non_watertight = False, fill=True) -> ndarray:
    """
    Convert a mesh into a 3D array
    Parameters
    -----------
    mesh : trimesh.Trimesh
      Source mesh
    num_layers : int
      Number of layers to create
    stl_unit_resolution: float
      How many stl units per pixel
    scale : tuple
      Factor to scale the mesh by (x, y, z)
    rotation : tuple
      Rotation to apply to the mesh (x, y, z) rotation in radians.
    max_slices : int
      Maximum number of slices or None for no limit.
    fill : bool
      Whether or not to fill internal regions.
    allow_non_watertight : bool
      Whether or not to allow non-watertight meshes.
    Returns
    -----------
    numpy.ndarray instance representing the mesh.
    """

    if not mesh.is_watertight and not allow_non_watertight:
        raise ValueError('Mesh is not watertight, set `allow_non_watertight` to True if intended')

    if not isinstance(num_layers, int):
        raise ValueError("Number of layers must be integer")

    if len(scale) != 3:
        raise ValueError('scale must be length 3 tuple, (z, y, x)')

    if len(rotation) != 3:
        raise ValueError('rotation must be length 3 tuple, (z, y, x) in radians')        

    
    #Scale mesh by user input value
    transformed_mesh = mesh.copy().apply_scale(scale)

    #Scale the mesh such that 1 unit in the mesh space equals the user input "stl_unit_resolution"
    #Eg. If the stl_unit_resolution is 2, the mesh is scaled by 1/2.
    totalScale = 1/stl_unit_resolution
    transformed_mesh = transformed_mesh.apply_scale((totalScale, totalScale, totalScale))
    
    #Scale the mesh such that it's height equals the number of slices requested
    z_length = transformed_mesh.extents[0]
    z_scale = (num_layers-1)/z_length
    transformed_mesh = transformed_mesh.apply_scale((z_scale, 1, 1))
    


    pitch = 1
    point = transformed_mesh.centroid
    radius = ceil(max(transformed_mesh.extents)/2.0)

    voxels = local_voxelize(transformed_mesh, point, pitch, radius,max_iter=200)

    d = voxels.matrix
    
    print(voxels.points_to_indices(voxels.points))

    # find indexes in all axis
    xs,ys,zs = np.where(d!=0)
    
    # extract cube with extreme limits of where are the values != 0
    result = d[min(xs):max(xs)+1,min(ys):max(ys)+1,min(zs):max(zs)+1] 

    # result = d[min(xs):max(xs)+1,:,:]
    print(np.invert(result))
 
    return result




if __name__ == "__main__":  
  from convertobmp import BMP
  mymesh= trimesh.load_mesh(r'C:\Users\20kev\Downloads\1278865_XYZ_20mm_Calibration_Cube\files\cube.STL')
  Resolution = getSlices(mesh=mymesh,num_layers=10,stl_unit_resolution=.1,scale=(1,1,1))
  print(type(Resolution))
  folder_name = r'Testing'
  BMP(folder_name,Resolution,768,1024,2580 )

  
