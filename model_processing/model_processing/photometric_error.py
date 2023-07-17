import glob
import os
from ruamel import yaml
from scipy.spatial.transform import Rotation as R
import numpy as np
import open3d as o3d
from PIL import Image
import cv2


def read_camera_matrix(path):
    with open(path, "r") as fp:
        read_data = yaml.safe_load(fp)
        camera_matrix = read_data["K"]
    return camera_matrix


def read_pose(path):
    with open(path, "r") as fp:
        read_data = yaml.safe_load(fp)
        quaternion = np.array(
            [
                read_data["rotation"]["w"],
                read_data["rotation"]["x"],
                read_data["rotation"]["y"],
                read_data["rotation"]["z"],
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
        np.array(r.as_matrix()), np.reshape(translation, (3, 1)), axis=1
    )
    transform = np.append(transform, [[0, 0, 0, 1]], axis=0)
    return transform


def read_pose_separate(path):
    with open(path, "r") as fp:
        read_data = yaml.safe_load(fp)
        quaternion = np.array(
            [
                read_data["rotation"]["w"],
                read_data["rotation"]["x"],
                read_data["rotation"]["y"],
                read_data["rotation"]["z"],
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
    rotation = np.array(r.as_matrix())
    return rotation, translation


def downsample_point_cloud(pcd):
    voxel_size = 0.01
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    return pcd_down


camera_matrix = read_camera_matrix(
    r"C:\Code\creating-a-mesh-from-plant-images\Data\Raw\13-42-50-tree\13a\1_camera_info.yaml"
)

local_rotation, local_translation = read_pose_separate(
    r"C:\Code\creating-a-mesh-from-plant-images\Data\Raw\13-42-50-tree\13a\1_transform.yaml"
)

global_rotation, global_translation = read_pose_separate(
    r"C:\Code\creating-a-mesh-from-plant-images\Data\Raw\13-42-50-tree\13a\world_marker_transform.yaml"
)

pose_rotation = np.matmul(np.transpose(global_rotation), np.transpose(local_rotation))
pose_translation = local_translation + global_translation

width, height = 2464, 2056

indices = [[-1 for j in range(width)] for i in range(height)]
depth = [[-1 for j in range(width)] for i in range(height)]
color = [[[0 for k in range(3)] for j in range(width)] for i in range(height)]

print("indices & depth shape:", np.array(indices).shape)
print("color shape:", np.array(color).shape)

absolute_path = os.path.abspath(".")
output_point_cloud_paths = glob.glob(absolute_path + "/input/output.ply")
pcd0 = o3d.io.read_point_cloud(output_point_cloud_paths[0])
pcd0_down = downsample_point_cloud(pcd0)
pcd0_point_array = np.asarray(pcd0_down.points)
pcd0_color_array = np.asarray(pcd0_down.colors)
print(pcd0_point_array.shape)

points_in_frame = 0

for i, p in enumerate(pcd0_point_array):
    # inverse translation back to image orientation
    point = p - pose_translation
    point = np.matmul(pose_rotation, point)
    # reprojection into 2d space
    fx = camera_matrix[0]
    fy = camera_matrix[4]
    cx = camera_matrix[2]
    cy = camera_matrix[5]
    u = ((fx * point[0]) / point[2]) + cx
    v = ((fy * point[1]) / point[2]) + cy
    point_2d = [u, v]
    # check if in image frame
    if (
        round(point_2d[0]) < height
        and round(point_2d[0]) >= 0
        and round(point_2d[1]) < width
        and round(point_2d[1]) >= 0
    ):
        points_in_frame += 1
        # check if it is the closest point to the image frame
        if (
            depth[round(point_2d[0])][round(point_2d[1])] == -1
            or depth[round(point_2d[0])][round(point_2d[1])] > p[2]
        ):
            indices[round(point_2d[0])][round(point_2d[1])] = i
            depth[round(point_2d[0])][round(point_2d[1])] = p[2]
            color[round(point_2d[0])][round(point_2d[1])] = (
                pcd0_color_array[i] * 255
            ).astype(np.uint8)
    print(i, "/", pcd0_point_array.shape[0])
print("number of points in frame / number of points")
print(
    points_in_frame,
    "/",
    pcd0_point_array.shape[0],
)
im = Image.fromarray(np.array(color), mode="RGB")
cv2.imwrite("test_color_cv2.png", np.array(color))
im.save("test_color.png")
np.savetxt("test_indices.csv", indices, delimiter=",")
np.savetxt("test_depth.csv", depth, delimiter=",")
np.savetxt("test_color.csv", np.reshape(color, (height * 3, width)), delimiter=",")
np.save("test_indices.npy", indices)
np.save("test_depth.npy", depth)
np.save("test_color.npy", color)
