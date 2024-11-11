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
