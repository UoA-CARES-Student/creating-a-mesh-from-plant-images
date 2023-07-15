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


if __name__ == "__main__":
    print("Load two aligned point clouds.")
    absolute_path = os.path.abspath(".")
    ply_point_cloud_paths = glob.glob(absolute_path + "/input/data/*.ply")
    output_point_cloud_paths = glob.glob(absolute_path + "/input/output.ply")
    pcd0 = o3d.io.read_point_cloud(ply_point_cloud_paths[3])
    pcd1 = o3d.io.read_point_cloud(output_point_cloud_paths[0])

    pcd0_down, pcd0_fpfh = preprocess_point_cloud(pcd0)
    pcd1_down, pcd1_fpfh = preprocess_point_cloud(pcd1)

    pcd0_down.paint_uniform_color([1, 0.706, 0])
    pcd1_down.paint_uniform_color([0, 0.651, 0.929])
    o3d.visualization.draw_geometries([pcd0_down, pcd1_down])

    print("Load their FPFH feature and evaluate.")
    print("Black : matching distance > 0.8")
    print("White : matching distance = 0")

    total_dis = 0.0

    fpfh_tree = o3d.geometry.KDTreeFlann(pcd1_fpfh)
    for i in range(len(pcd0_down.points)):
        [_, idx, _] = fpfh_tree.search_knn_vector_xd(pcd0_fpfh.data[:, i], 1)
        dis = np.linalg.norm(pcd0_down.points[i] - pcd1_down.points[idx[0]])
        total_dis += dis
        c = (0.8 - np.fmin(dis, 0.8)) / 0.8
        pcd0_down.colors[i] = [c, c, c]
    o3d.visualization.draw_geometries([pcd0_down])

    avg_dis = total_dis / len(pcd0_down.points)
    print("Average distance", avg_dis)
