import open3d as o3d
import numpy as np
import create_complete_model
import colorsys


def voxel_downsample_point_cloud(pcd):
    voxel_size = 0.00001
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    return pcd_down


def random_downsample(pcd):
    ratio = 0.2
    print(":: Random downsample with ratio %.3f." % ratio)
    pcd_down = pcd.random_down_sample(ratio)
    return pcd_down


def uniform_downsample(pcd):
    every_k_points = 5
    print(":: Uniform downsample with every k points removed %.3f." % every_k_points)
    pcd_down = pcd.uniform_down_sample(every_k_points)
    return pcd_down


def pass_through_filter_2(pcd):
    depth_cut_off_y = 0.6
    depth_cut_off_x = 0.4
    depth_cut_off_z = 0.6

    pcd_point_array = np.asarray(pcd.points)
    pcd_color_array = np.asarray(pcd.colors)

    print(":: Pass through filter")

    filtered_points = []
    filtered_colors = []

    for p_index, p in enumerate(pcd_point_array):
        # if inside range then include
        if p[1] < depth_cut_off_x and p[2] < depth_cut_off_y and p[2] < depth_cut_off_z:
            filtered_points.append(p)
            filtered_colors.append(increase_saturation(pcd_color_array[p_index]))

    pcd.points = o3d.utility.Vector3dVector(filtered_points)
    pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

    return pcd


def increase_saturation(color_array):
    r = color_array[0] * 255
    g = color_array[1] * 255
    b = color_array[2] * 255
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    s = s * 2
    v = v / 2
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)

    return np.array([r / 255, g / 255, b / 255])


def pass_through_filter(pcd):
    z_threshold = 0.6
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    print(points.shape)
    print(colors.shape)
    mask = points[:, 1] < z_threshold
    print(points[mask].shape)
    pcd.points = o3d.utility.Vector3dVector(points[mask])
    pcd.colors = o3d.utility.Vector3dVector(colors[mask])
    return pcd


def radius_outlier_removal(pcd):
    print("::  radius outlier removal")
    point_cloud_result, ind = pcd.remove_radius_outlier(nb_points=1000, radius=1)
    return point_cloud_result


def statistical_outlier_removal(pcd):
    print("::  statistical outlier removal")
    point_cloud_result, ind = pcd.remove_statistical_outlier(
        nb_neighbors=2000, std_ratio=2.0
    )
    return point_cloud_result


def main(path):
    if path is None:
        point_cloud = create_complete_model.create_point_cloud()
    else:
        print("Reading from path: ", path)
        point_cloud = o3d.io.read_point_cloud(path)

    # point_cloud = pass_through_filter_2(point_cloud)

    # point_cloud = voxel_downsample_point_cloud(point_cloud)
    point_cloud = random_downsample(point_cloud)
    point_cloud = statistical_outlier_removal(point_cloud)
    # point_cloud = radius_outlier_removal(point_cloud)

    return point_cloud
