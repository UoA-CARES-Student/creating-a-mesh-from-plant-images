"""Module providing functions for calculating metrics from a point cloud"""
import math
import numpy as np


def mean_square_error_test_one(processed_point_cloud, target_point_cloud):
    """Return a float representing the mse between the point clouds
    Implementation of MSE algorithm from https://arxiv.org/abs/1807.00253
    """
    processed_point_cloud_array = np.array(processed_point_cloud)
    target_point_cloud_array = np.array(target_point_cloud)
    distance_sum = calc_distance_between_points_test_one(
        processed_point_cloud_array, target_point_cloud_array
    )
    return distance_sum / len(target_point_cloud_array)


def mean_square_error_test_two(processed_point_cloud, target_point_cloud):
    """Return a float representing the mse between the point clouds
    Implementation of MSE algorithm from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9002461/
    """
    processed_point_cloud_array = np.array(processed_point_cloud)
    target_point_cloud_array = np.array(target_point_cloud)

    section_one, section_two = calc_distance_between_points_test_two(
        processed_point_cloud_array, target_point_cloud_array
    )

    return (section_one + section_two) / 2


def signal_to_noise_ratio_test_one(processed_point_cloud, target_point_cloud):
    """Return a float representing the snr between the point clouds
    Implementation of MSE algorithm from https://arxiv.org/abs/1807.00253
    """
    processed_point_cloud_array = np.array(processed_point_cloud)
    target_point_cloud_array = np.array(target_point_cloud)

    sum_processed_point_cloud = 0.0
    for p_i in np.nditer(processed_point_cloud_array):
        sum_processed_point_cloud += np.linalg.norm(p_i)

    distance_sum = calc_distance_between_points_test_one(
        processed_point_cloud_array, target_point_cloud_array
    )

    return 20 * math.log(sum_processed_point_cloud / distance_sum)


def signal_to_noise_ratio_test_two(processed_point_cloud, target_point_cloud):
    """Return a float representing the snr between the point clouds
    Implementation of MSE algorithm from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9002461/
    """
    processed_point_cloud_array = np.array(processed_point_cloud)
    target_point_cloud_array = np.array(target_point_cloud)

    sum_processed_point_cloud = 0.0
    for p_i in np.nditer(processed_point_cloud_array):
        sum_processed_point_cloud += np.linalg.norm(p_i)

    section_one, section_two = calc_distance_between_points_test_two(
        processed_point_cloud_array, target_point_cloud_array
    )

    total = ((2.0 / len(processed_point_cloud_array)) * sum_processed_point_cloud) / (
        section_one + section_two
    )

    return 10 * math.log(total)


def calc_distance_between_points_test_one(
    processed_point_cloud_array, target_point_cloud_array
):
    """Return a float representing the distance between all points"""
    distance_sum = 0.0
    for p_i in np.nditer(processed_point_cloud_array):
        for p_j in np.nditer(target_point_cloud_array):
            distance_sum += np.linalg.norm(p_i - p_j)
    return distance_sum


def calc_distance_between_points_test_two(
    processed_point_cloud_array, target_point_cloud_array
):
    """Return a float representing the distance between all points"""
    distance_sum = 0.0
    for p_i in np.nditer(processed_point_cloud_array):
        min_distance = -1
        for p_j in np.nditer(target_point_cloud_array):
            distance = np.linalg.norm(p_i - p_j)
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_one = distance_sum / len(processed_point_cloud_array)

    distance_sum = 0.0
    for p_i in np.nditer(target_point_cloud_array):
        min_distance = -1
        for p_j in np.nditer(processed_point_cloud_array):
            distance = np.linalg.norm(p_i - p_j)
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_two = distance_sum / len(target_point_cloud_array)

    return section_one, section_two
