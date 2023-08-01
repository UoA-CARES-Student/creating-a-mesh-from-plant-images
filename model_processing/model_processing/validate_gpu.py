"""Module providing functions for combining multiple point cloud files into a 
single point cloud file"""
import glob
import os
import open3d as o3d
from metrics_gpu import mean_square_error_two, signal_to_noise_ratio_two
from add_gausian_noise import add_noise_to_target_point_cloud
import filtering
import numpy as np


def run_controlled_experiment():
    print("Starting controlled experiment")
    absolute_path = os.path.abspath(".")
    target_point_cloud_path = glob.glob(absolute_path + "/input/target.ply")

    if len(target_point_cloud_path) == 0:
        print("Point cloud data not found")
    else:
        add_noise_to_target_point_cloud()
        noisy_point_cloud_path = glob.glob(absolute_path + "/input/noisy.ply")

        processed_point_cloud = filtering.main(noisy_point_cloud_path)

        target_point_cloud = o3d.io.read_point_cloud(target_point_cloud_path[0])

        processed_point_cloud_array = np.asarray(processed_point_cloud.points)
        target_point_cloud_array = np.asarray(target_point_cloud.points)

        mse = mean_square_error_two(
            processed_point_cloud_array, target_point_cloud_array
        )
        print("mse 2 : ", mse)
        snr = signal_to_noise_ratio_two(
            processed_point_cloud_array, target_point_cloud_array
        )
        print("snr 2 : ", snr)
        print("Done!")
