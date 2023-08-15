import open3d as o3d
import numpy as np
import create_complete_model


def downsample_point_cloud(pcd):
    voxel_size = 0.01
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    return pcd_down


def pass_through_filter(pcd):
    z_threshold = 0
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    print(points.shape)
    print(colors.shape)
    mask = points[:, 2] < z_threshold
    print(points[mask].shape)
    pcd.points = o3d.utility.Vector3dVector(points[mask])
    pcd.colors = o3d.utility.Vector3dVector(colors[mask])
    return pcd


def radius_outlier_removal(pcd):
    point_cloud_result, ind = pcd.remove_radius_outlier(nb_points=16, radius=0.05)
    return point_cloud_result


def statistical_outlier_removal(pcd):
    point_cloud_result, ind = pcd.remove_statistical_outlier(
        nb_neighbors=20, std_ratio=2.0
    )
    return point_cloud_result


def main(path):
    point_cloud = create_complete_model.create_point_cloud()
    # point_cloud = downsample_point_cloud(point_cloud)
    # point_cloud = pass_through_filter(point_cloud)
    point_cloud = statistical_outlier_removal(point_cloud)

    return point_cloud
