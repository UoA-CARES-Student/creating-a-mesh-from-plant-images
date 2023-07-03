"""Module providing functions for combining multiple point cloud files into a 
single point cloud file"""
import glob
import os
import open3d as o3d
from metrics import *

print("Starting validation")
absolute_path = os.path.abspath(".")
processed_point_cloud_path = glob.glob(absolute_path + "/input/processed.ply")
target_point_cloud_path = glob.glob(absolute_path + "/input/target.ply")

if len(processed_point_cloud_path) == 0 or len(target_point_cloud_path) == 0:
    print("No point cloud data found")
else:
    processed_point_cloud = o3d.io.read_point_cloud(processed_point_cloud_path[0])
    target_point_cloud = o3d.io.read_point_cloud(target_point_cloud_path[0])
    o3d.visualization.draw_geometries([processed_point_cloud])
    o3d.visualization.draw_geometries([target_point_cloud])
    print(
        "mse 1 : "
        + mean_square_error_test_one(processed_point_cloud, target_point_cloud)
    )
    print("Done!")
