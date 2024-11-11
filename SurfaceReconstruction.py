
import pickle
import open3d as o3d
import numpy as np
import time
from collections import Counter

#Poisson Surface Reconstruction
def load_and_display_objects(pickle_file_path):
    # load the pickle file
    with open(pickle_file_path, 'rb') as fr:
        objects = pickle.load(fr)
    geos = []
    
    for key, value in objects.items():
        if isinstance(value[0], np.ndarray) and len(value[0]) >= 100:
            start = time.time()
            points = value[0]
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(points)
            point_cloud.voxel_down_sample(voxel_size=0.01)

            # Using voxel to crop the mesh
            voxel_size = 8
            voxels = set(map(tuple, np.floor_divide(np.asarray(point_cloud.points), voxel_size)))
            a = np.asarray(point_cloud.cluster_dbscan(3, 10))
            point_cloud = point_cloud.select_by_index(np.where(a == 0)[0])
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)[0]
            
            # vertices
            vertices = np.asarray(mesh.vertices)
            vertices_voxel = list(map(tuple, np.floor_divide(np.asarray(vertices), voxel_size)))
            vertices_index = []
            for i in range(len(vertices_voxel)):
                if vertices_voxel[i] in voxels:
                    vertices_index.append(i)
            vertices_index = set(vertices_index)
            
            # triangles
            triangles = np.asarray(mesh.triangles)
            triangles_index = []
            for triangle in range(len(triangles)):
                invoxel = []
                for vert in triangles[triangle]:
                    if vert in vertices_index:
                        invoxel.append(1)
                if len(invoxel) > 1:
                    triangles_index.append(triangle)
            triangles_index = np.asarray(triangles_index)
            
            # update mesh
            mesh.triangles = o3d.utility.Vector3iVector(
                np.asarray(mesh.triangles)[triangles_index, :])
            mesh.compute_vertex_normals()
            mesh.paint_uniform_color([1, 0.706, 0])
            geos.append(mesh)
            o3d.visualization.draw_geometries([mesh])
    
    # show all the objects
    o3d.visualization.draw_geometries(geos)


# 示例用法
pickle_file_path = './example.txt'
load_and_display_objects(pickle_file_path)