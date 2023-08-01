import argparse
import glob
import os
import open3d as o3d

import filtering
import validate_gpu
import feature_compare_gpu
import photometric_error_gpu

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--display",
    help="displays the filtered result",
    action="store_true",
)
parser.add_argument(
    "-a",
    "--all",
    help="runs all metrics without gpu",
    action="store_true",
)
parser.add_argument(
    "-c",
    "--controlled",
    help="runs the controlled experiment metrics without gpu",
    action="store_true",
)
parser.add_argument(
    "-f",
    "--feature",
    help="runs the feature compare metric without gpu",
    action="store_true",
)
parser.add_argument(
    "-p",
    "--photometric",
    help="runs the photometric error metric without gpu",
    action="store_true",
)

args = parser.parse_args()


absolute_path = os.path.abspath(".")
point_cloud_path = glob.glob(absolute_path + "/input/starting_point_cloud.ply")
point_cloud_result = filtering.main(point_cloud_path)

if args.display:
    o3d.visualization.draw_geometries([point_cloud_result])
if args.controlled or args.all:
    validate_gpu.run_controlled_experiment()
if args.feature or args.all:
    feature_compare_gpu.run_feature_compare(point_cloud_result)
if args.photometric or args.all:
    photometric_error_gpu.run_photometric_error(point_cloud_result)
