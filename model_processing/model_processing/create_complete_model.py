"""Module providing functions for combining multiple point cloud files into a 
single point cloud file"""
import glob
import os
import open3d as o3d

print("Starting point cloud combination")
absolute_path = os.path.abspath(".")
ply_point_cloud_paths = glob.glob(absolute_path + "/input/*.ply")

complete_point_cloud = o3d.geometry.PointCloud()

for ply_point_cloud_path in ply_point_cloud_paths:
    point_cloud_section = o3d.io.read_point_cloud(ply_point_cloud_path)
    complete_point_cloud += point_cloud_section

# o3d.visualization.draw_geometries([complete_point_cloud])

o3d.io.write_point_cloud(
    absolute_path + "/output/output.ply",
    complete_point_cloud,
    write_ascii=True,
    print_progress=True,
)

print("Done! The output.ply file has been written to the output folder")
