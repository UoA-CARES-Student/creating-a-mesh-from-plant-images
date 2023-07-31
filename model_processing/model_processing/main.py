import argparse
import open3d as o3d

import filtering
import validate
import feature_compare
import photometric_error

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--display",
    help="displays the filtered result",
    action="store_true",
)
parser.add_argument(
    "-c",
    "--controlled",
    help="runs the controlled experiment metrics without gpu",
    action="store_true",
)
parser.add_argument(
    "-cgpu",
    "--controlledgpu",
    help="runs the controlled experiment metrics with gpu",
    action="store_true",
)
parser.add_argument(
    "-f",
    "--feature",
    help="runs the feature compare metric without gpu",
    action="store_true",
)
parser.add_argument(
    "-fgpu",
    "--featuregpu",
    help="runs the feature compare metric with gpu",
    action="store_true",
)
parser.add_argument(
    "-p",
    "--photometric",
    help="runs the photometric error metric without gpu",
    action="store_true",
)
parser.add_argument(
    "-pgpu",
    "--photometricgpu",
    help="runs the photometric error metric with gpu",
    action="store_true",
)

args = parser.parse_args()


point_cloud_result = filtering.main()

if args.display:
    o3d.visualization.draw_geometries([point_cloud_result])
if args.controlled:
    validate.run_controlled_experiment_without_gpu()
if args.controlledgpu:
    validate.run_controlled_experiment_with_gpu()
if args.feature:
    feature_compare.run_feature_compare_without_gpu(point_cloud_result)
if args.featuregpu:
    feature_compare.run_feature_compare_with_gpu(point_cloud_result)
if args.photometric:
    photometric_error.run_photometric_error_without_gpu(point_cloud_result)
if args.photometricgpu:
    photometric_error.run_photometric_error_with_gpu(point_cloud_result)
