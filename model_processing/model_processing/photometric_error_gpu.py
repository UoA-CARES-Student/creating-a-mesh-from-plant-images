import glob
import os
from ruamel import yaml
from scipy.spatial.transform import Rotation as R
import numpy as np
import open3d as o3d
from PIL import Image
from numba import jit
from utils import print_progress_bar
import cv2
import math

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)


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


@jit(target_backend="cuda")
def downsample_point_cloud(pcd):
    voxel_size = 0.001
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    return pcd_down


@jit(target_backend="cuda")
def run_photometric_error(point_cloud_result):
    print("Start photometric error metric")
    absolute_path = os.path.abspath("..")
    image_paths = glob.glob(absolute_path + "/Data/13a/*_camera_info.yaml")

    total_avg_depth_diff_sum = 0
    total_avg_color_diff_sum = 0
    total_image_frames = 0

    for image_path_index, image_path in enumerate(image_paths):
        base_path = image_path[:-17]

        if base_path[-6:] == "marker":
            continue

        total_image_frames += 1

        camera_matrix = read_camera_matrix(base_path + "_camera_info.yaml")

        original_im = cv2.imread(image_path)
        original_im_rgb = original_im[..., ::-1].copy()

        original_depth = Image.open(base_path + "_depth.tif")
        original_depth = np.array(original_depth)

        local_transform = read_pose(base_path + "_transform.yaml")
        global_transform = read_pose(
            absolute_path + "/Data/13a/world_marker_transform.yaml"
        )

        pose_transform = np.matmul(global_transform, local_transform)

        pose_inverse = np.linalg.inv(pose_transform)

        width, height = 2464, 2056

        indices = [[-1 for j in range(width)] for i in range(height)]
        depth = [[-1 for j in range(width)] for i in range(height)]
        color = [[[0 for k in range(3)] for j in range(width)] for i in range(height)]

        point_cloud_result_down = downsample_point_cloud(point_cloud_result)
        point_cloud_result_point_array = np.asarray(point_cloud_result_down.points)
        point_cloud_result_color_array = np.asarray(point_cloud_result_down.colors)

        points_in_frame = 0

        print_progress_bar(
            0,
            len(point_cloud_result_point_array),
            prefix="Projecting onto image frame " + base_path[-2:] + ":",
        )

        for p_index, p in enumerate(point_cloud_result_point_array):
            # inverse translation back to image orientation
            point = np.append(p, [1], axis=0)
            point = np.matmul(pose_inverse, point)
            point = [point[0] / point[3], point[1] / point[3], point[2] / point[3]]
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
                round(point_2d[0]) < width
                and round(point_2d[0]) >= 0
                and round(point_2d[1]) < height
                and round(point_2d[1]) >= 0
            ):
                points_in_frame += 1
                # check if it is the closest point to the image frame
                if (
                    depth[round(point_2d[1])][round(point_2d[0])] == -1
                    or depth[round(point_2d[1])][round(point_2d[0])] > p[2]
                ):
                    indices[round(point_2d[1])][round(point_2d[0])] = i
                    depth[round(point_2d[1])][round(point_2d[0])] = p[2]

                    color[round(point_2d[1])][round(point_2d[0])] = (
                        point_cloud_result_color_array[i] * 255
                    ).astype(np.uint8)
            print_progress_bar(
                p_index + 1,
                len(point_cloud_result_point_array),
                prefix="Projecting onto image frame " + base_path[-2:] + ":",
            )

        cv2.imwrite("test_color_cv2.png", np.array(color)[..., ::-1].copy())
        # np.savetxt("test_indices.csv", indices, delimiter=",")
        # np.savetxt("test_depth.csv", depth, delimiter=",")
        # np.savetxt("test_color.csv", np.reshape(color, (width * 3, height)), delimiter=",")
        # np.save("test_indices.npy", indices)
        # np.save("test_depth.npy", depth)
        # np.save("test_color.npy", color)

        depth_diff_sum = 0
        color_diff_sum = 0

        for row in range(width):
            for col in range(height):
                if depth[col][row] != -1:
                    depth_diff_sum += abs(depth[col][row] - original_depth[col][row])
                    color_diff_sum += np.linalg.norm(
                        color[col][row] - original_im_rgb[col][row]
                    )

        depth_diff_avg = depth_diff_sum / points_in_frame
        color_diff_avg = color_diff_sum / points_in_frame

        print(
            "Average depth difference for image frame " + base_path[-2:] + ":",
            depth_diff_avg,
        )
        print(
            "Average color difference for image frame " + base_path[-2:] + ":",
            color_diff_avg,
        )

        total_avg_depth_diff_sum += depth_diff_avg
        total_avg_color_diff_sum += color_diff_avg

    total_avg_depth_diff = total_avg_depth_diff_sum / total_image_frames
    total_avg_color_diff = total_avg_color_diff_sum / total_image_frames
    print("Average depth difference for all image frames:", total_avg_depth_diff)
    print("Average color difference for all image frames:", total_avg_color_diff)
