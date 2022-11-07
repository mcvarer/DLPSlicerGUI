from trimesh.voxel.creation import voxelize_subdivide
from trimesh.voxel.creation import local_voxelize
from trimesh import base
import numpy as np


def voxelize(mesh):
    vox = voxelize_subdivide(mesh, 1, max_iter=None)
    return vox