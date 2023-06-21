import numpy as np
import open3d as o3d
import glob
import os

print("attempt 1")
absolute_path = os.path.abspath("./input")
ply_point_cloud_paths = glob.glob(absolute_path + "/*.ply")

complete_point_cloud = o3d.geometry.PointCloud()

for ply_point_cloud_path in ply_point_cloud_paths:
    point_cloud_section = o3d.io.read_point_cloud(ply_point_cloud_path)
    complete_point_cloud += point_cloud_section

o3d.visualization.draw_geometries(
    [complete_point_cloud],
    zoom=0.3412,
    front=[0.4257, -0.2125, -0.8795],
    lookat=[2.6172, 2.0475, 1.532],
    up=[-0.0694, -0.9768, 0.2024],
)
