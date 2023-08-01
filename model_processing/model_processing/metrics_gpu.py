"""Module providing functions for calculating metrics from a point cloud"""
import math
from numba import jit

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)


@jit(target_backend="cuda")
def mean_square_error_one(processed_point_cloud, target_point_cloud):
    """Return a float representing the mse between the point clouds
    Implementation of MSE algorithm from https://arxiv.org/abs/1807.00253
    """
    print("starting mean square error one")
    print("processed point cloud array shape:", processed_point_cloud.shape)
    print("target point cloud array shape:", target_point_cloud.shape)
    distance_sum = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        for index_j, p_j in enumerate(target_point_cloud):
            distance_vector = p_i - p_j
            distance_sum += (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )
    return distance_sum / len(target_point_cloud)


@jit(target_backend="cuda")
def mean_square_error_two(processed_point_cloud, target_point_cloud):
    """Return a float representing the mse between the point clouds
    Implementation of MSE algorithm from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9002461/
    """
    print("starting mean square error two")
    print("processed point cloud array shape:", processed_point_cloud.shape)
    print("target point cloud array shape:", target_point_cloud.shape)
    distance_sum = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        min_distance = -1
        for index_j, p_j in enumerate(target_point_cloud):
            distance_vector = p_i - p_j
            distance = (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_one = distance_sum / len(processed_point_cloud)

    distance_sum = 0.0
    for index_i, p_i in enumerate(target_point_cloud):
        min_distance = -1
        for index_j, p_j in enumerate(processed_point_cloud):
            distance_vector = p_i - p_j
            distance = (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_two = distance_sum / len(target_point_cloud)

    return (section_one + section_two) / 2


@jit(target_backend="cuda")
def signal_to_noise_ratio_one(processed_point_cloud, target_point_cloud):
    """Return a float representing the snr between the point clouds
    Implementation of MSE algorithm from https://arxiv.org/abs/1807.00253
    """
    print("starting signal to noise ratio one")
    print("processed point cloud array shape:", processed_point_cloud.shape)
    print("target point cloud array shape:", target_point_cloud.shape)
    sum_processed_point_cloud = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        sum_processed_point_cloud += (
            math.sqrt(p_i[0] ** 2 + p_i[1] ** 2 + p_i[2] ** 2) ** 2
        )

    distance_sum = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        for index_j, p_j in enumerate(target_point_cloud):
            distance_vector = p_i - p_j
            distance_sum += (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )

    return 20 * math.log(sum_processed_point_cloud / distance_sum)


@jit(target_backend="cuda")
def signal_to_noise_ratio_two(processed_point_cloud, target_point_cloud):
    """Return a float representing the snr between the point clouds
    Implementation of MSE algorithm from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9002461/
    """
    print("starting signal to noise ratio two")
    print("processed point cloud array shape:", processed_point_cloud.shape)
    print("target point cloud array shape:", target_point_cloud.shape)
    sum_processed_point_cloud = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        sum_processed_point_cloud += (
            math.sqrt(p_i[0] ** 2 + p_i[1] ** 2 + p_i[2] ** 2) ** 2
        )

    distance_sum = 0.0
    for index_i, p_i in enumerate(processed_point_cloud):
        min_distance = -1
        for index_j, p_j in enumerate(target_point_cloud):
            distance_vector = p_i - p_j
            distance = (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_one = distance_sum / len(processed_point_cloud)

    distance_sum = 0.0
    for index_i, p_i in enumerate(target_point_cloud):
        min_distance = -1
        for index_j, p_j in enumerate(processed_point_cloud):
            distance_vector = p_i - p_j
            distance = (
                math.sqrt(
                    distance_vector[0] ** 2
                    + distance_vector[1] ** 2
                    + distance_vector[2] ** 2
                )
                ** 2
            )
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        distance_sum += min_distance
    section_two = distance_sum / len(target_point_cloud)

    total = ((2.0 / len(processed_point_cloud)) * sum_processed_point_cloud) / (
        section_one + section_two
    )

    return 10 * math.log(total)
