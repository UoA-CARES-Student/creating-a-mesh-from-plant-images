# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2023 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import glob
import os
import numpy as np
import open3d as o3d
from numba import jit

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)


@jit(target_backend="cuda")
def preprocess_point_cloud(pcd):
    voxel_size = 0.05
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = 1
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )

    radius_feature = 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100),
    )
    return pcd_down, pcd_fpfh


@jit(target_backend="cuda")
def run_feature_compare(point_cloud_result):
    print("Start feature compare metric")
    absolute_path = os.path.abspath(".")
    ply_point_cloud_paths = glob.glob(absolute_path + "/input/data/*.ply")

    total_avg_distance_sum = 0

    for partial_point_cloud_index, partial_point_cloud_path in enumerate(
        ply_point_cloud_paths
    ):
        partial_point_cloud = o3d.io.read_point_cloud(partial_point_cloud_path)

        partial_point_cloud_down, partial_point_cloud_fpfh = preprocess_point_cloud(
            partial_point_cloud
        )
        point_cloud_result_down, point_cloud_result_fpfh = preprocess_point_cloud(
            point_cloud_result
        )

        partial_point_cloud_down.paint_uniform_color([1, 0.706, 0])
        point_cloud_result_down.paint_uniform_color([0, 0.651, 0.929])
        # o3d.visualization.draw_geometries(
        #     [partial_point_cloud_down, point_cloud_result_down]
        # )

        print("Load their FPFH feature and evaluate.")
        print("Black : matching distance > 0.8")
        print("White : matching distance = 0")

        total_dis = 0.0

        fpfh_tree = o3d.geometry.KDTreeFlann(point_cloud_result_fpfh)
        for point_index, point in enumerate(partial_point_cloud_down.points):
            [_, idx, _] = fpfh_tree.search_knn_vector_xd(
                partial_point_cloud_fpfh.data[:, point_index], 1
            )
            dis = np.linalg.norm(
                partial_point_cloud_down.points[point_index]
                - point_cloud_result_down.points[idx[0]]
            )
            total_dis += dis
            c = (0.8 - np.fmin(dis, 0.8)) / 0.8
            partial_point_cloud_down.colors[point_index] = [c, c, c]
        # o3d.visualization.draw_geometries([partial_point_cloud_down])

        avg_dis = total_dis / len(partial_point_cloud_down.points)
        print(
            "Average feature distance for partial point cloud",
            partial_point_cloud_index,
            ":",
            avg_dis,
        )
        total_avg_distance_sum += avg_dis
    total_avg_distance = total_avg_distance_sum / len(ply_point_cloud_paths)
    print(
        "Average feature distance across all partial point clouds:", total_avg_distance
    )
