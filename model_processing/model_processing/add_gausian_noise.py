"""Module providing functions for combining multiple point cloud files into a 
single point cloud file"""
import glob
import os
import random
import open3d as o3d
import numpy as np


def add_noise_to_target_point_cloud():
    print("Adding noise")
    absolute_path = os.path.abspath(".")
    target_point_cloud_path = glob.glob(absolute_path + "/input/target.ply")

    if len(target_point_cloud_path) == 0:
        print("No point cloud data found")

    target_point_cloud = o3d.io.read_point_cloud(target_point_cloud_path[0])

    target_point_cloud_array = np.asarray(target_point_cloud.points)

    print(target_point_cloud_array.shape)

    noise_probability = 0.4

    mu, sigma = 0.0, 0.01

    for i, number in enumerate(target_point_cloud_array):
        if random.random() < noise_probability:
            target_point_cloud_array[i][0] += np.random.normal(mu, sigma)
            target_point_cloud_array[i][1] += np.random.normal(mu, sigma)
            target_point_cloud_array[i][2] += np.random.normal(mu, sigma)

    o3d.io.write_point_cloud(
        absolute_path + "/input/noisy.ply",
        target_point_cloud,
        print_progress=True,
    )

    print("Done! The noisy.ply file has been written to the output folder")
