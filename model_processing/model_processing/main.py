import argparse
import glob
import os
import open3d as o3d

import filtering
import validate
import feature_compare
import photometric_error
import create_mesh

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
if len(point_cloud_path) == 0:
    print(
        "Starting point cloud data not found, please add to input folder with file name 'starting_point_cloud.ply'"
    )
else:
    point_cloud_result = filtering.main(point_cloud_path[0])

    if args.display:
        o3d.visualization.draw_geometries([point_cloud_result])
    if args.controlled or args.all:
        validate.run_controlled_experiment()
    if args.feature or args.all:
        feature_compare.run_feature_compare(point_cloud_result)
    if args.photometric or args.all:
        photometric_error.run_photometric_error(point_cloud_result)

    mesh = create_mesh.create_ball_pivot_mesh(point_cloud_result)

    if args.display:
        o3d.visualization.draw([mesh])
