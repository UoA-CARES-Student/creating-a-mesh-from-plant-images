import open3d as o3d
import numpy as np


def downsample_point_cloud(pcd):
    voxel_size = 0.01
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    return pcd_down


def main(path):
    point_cloud = o3d.io.read_point_cloud(path)
    point_cloud_down = downsample_point_cloud(point_cloud)
    point_cloud_result, ind = point_cloud_down.remove_radius_outlier(
        nb_points=16, radius=0.05
    )
    return point_cloud_result
