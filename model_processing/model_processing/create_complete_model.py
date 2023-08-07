"""Module providing functions for combining multiple point cloud files into a 
single point cloud file"""
import glob
import os
import open3d as o3d

from ruamel import yaml
from scipy.spatial.transform import Rotation as R
import numpy as np


def pass_through_filter(pcd, index):
    depth_range = [0.2, 1]

    # read pose
    absolute_path = os.path.abspath("..")
    local_transform = read_pose(
        absolute_path + "/Data/13-42-50-tree/13a/" + index + "_transform.yaml"
    )
    global_transform = read_pose(
        absolute_path + "/Data/13-42-50-tree/13a/world_marker_transform.yaml"
    )
    pose_transform = np.matmul(global_transform, local_transform)

    pose_inverse = np.linalg.inv(pose_transform)

    pcd_point_array = np.asarray(pcd.points)
    pcd_color_array = np.asarray(pcd.colors)

    filtered_points = []
    filtered_colors = []

    for p_index, p in enumerate(pcd_point_array):
        # inverse translation back to image orientation
        point = np.append(p, [1], axis=0)
        point = np.matmul(pose_inverse, point)
        point = [point[0] / point[3], point[1] / point[3], point[2] / point[3]]
        depth = point[2]

        # if inside range then include
        if depth > depth_range[0] and depth < depth_range[1]:
            filtered_points.append(point)
            filtered_colors.append(pcd_color_array[p_index])

    pcd.points = o3d.utility.Vector3dVector(filtered_points)
    pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

    return pcd


def extract_index(path):
    filename = path.split("/")[-1].split(".")[0]
    padded_index = filename.split("_")[-1]
    index = str(int(padded_index))
    return index


def read_pose(path):
    with open(path, "r") as fp:
        read_data = yaml.safe_load(fp)
        quaternion = np.array(
            [
                read_data["rotation"]["x"],
                read_data["rotation"]["y"],
                read_data["rotation"]["z"],
                read_data["rotation"]["w"],
            ]
        )
        translation = np.array(
            [
                read_data["translation"]["x"],
                read_data["translation"]["y"],
                read_data["translation"]["z"],
            ]
        )
    r = R.from_quat(quaternion)
    transform = np.append(
        np.array(r.as_matrix()),
        np.reshape(translation, (3, 1)),
        axis=1,
    )
    transform = np.append(transform, [[0, 0, 0, 1]], axis=0)
    return transform


def create_point_cloud():
    print("Starting point cloud combination")
    absolute_path = os.path.abspath(".")
    ply_point_cloud_paths = glob.glob(absolute_path + "/input/data/*.ply")

    complete_point_cloud = o3d.geometry.PointCloud()

    for ply_point_cloud_path in ply_point_cloud_paths:
        point_cloud_section = o3d.io.read_point_cloud(ply_point_cloud_path)
        point_cloud_section = pass_through_filter(
            point_cloud_section, extract_index(ply_point_cloud_path)
        )
        complete_point_cloud += point_cloud_section

    # o3d.visualization.draw_geometries([complete_point_cloud])

    o3d.io.write_point_cloud(
        absolute_path + "/output/output.ply",
        complete_point_cloud,
        write_ascii=True,
        print_progress=True,
    )

    print("Done! The output.ply file has been written to the output folder")


create_point_cloud()
