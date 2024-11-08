import numpy
import numpy as np
import open3d
from icecream import ic
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import matplotlib.tri as tri

class APP():
    def __init__(self):
        self.app = gui.Application.instance
        self.app.initialize()
        self.vis = o3d.visualization.O3DVisualizer("ProMap")
        self.vis.show_settings = True
        self.vis.size_to_fit()

    def add_points_from_numpy(self, name: str, points: numpy.ndarray, colors=None):
        points_class = open3d.geometry.PointCloud()
        points_class.points = open3d.utility.Vector3dVector(points)
        if colors == None:
            points_class.colors = open3d.utility.Vector3dVector(self.random_color_generate())
        else:
            points_class.colors = open3d.utility.Vector3dVector(colors)
        self.vis.add_geometry(name, points_class)

    def add_geometry(self, name: str, geometry):
        self.vis.add_geometry(name, geometry)

    def random_color_generate(self):
        return np.random.randint(0, 255, 3)/255

    def add_text(self, point, text):
        self.vis.add_3d_label(point, text)

    def run(self):
        self.vis.reset_camera_to_default()
        self.app.add_window(self.vis)
        self.app.run()


# Example
"""
app = APP()
import pickle

pickle_file_path = 'P:\文稿\HKU\group meeting\meeting\dataFile_09132024-11-08_.txt'
with open(pickle_file_path, 'rb') as fr:
    objects = pickle.load(fr)
# 创建一个列表来存储所有的PointCloud对象
point_clouds = []

for key, value in objects.items():
    if isinstance(value[0], np.ndarray) and value[2]>15:
        print("loading..")
        points = value[0]
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        point_cloud.paint_uniform_color(np.random.randint(0, 255, 3)/255)
        app.add_geometry("instance"+str(key), point_cloud)

app.run()
"""