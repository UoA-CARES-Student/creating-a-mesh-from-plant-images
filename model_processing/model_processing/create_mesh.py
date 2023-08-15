import open3d as o3d
import os


def create_ball_pivot_mesh(point_cloud):
    # radius_normal = 1
    # point_cloud.estimate_normals(
    #     o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    # )
    point_cloud.estimate_normals()
    point_cloud.orient_normals_consistent_tangent_plane(100)
    radii = [0.0005, 0.005, 0.01, 0.02, 0.04, 0.5, 1]
    print("Running ball pivoting surface reconstruction ...")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        point_cloud, o3d.utility.DoubleVector(radii)
    )

    absolute_path = os.path.abspath(".")
    o3d.io.write_triangle_mesh(
        absolute_path + "/output/mesh_output.obj",
        mesh,
        print_progress=True,
    )
    return mesh


def create_poissons_mesh(point_cloud):
    radius_normal = 1
    point_cloud.estimate_normals()
    point_cloud.orient_normals_consistent_tangent_plane(100)
    print("Running Poisson surface reconstruction ...")
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        point_cloud, depth=9
    )

    absolute_path = os.path.abspath(".")
    o3d.io.write_triangle_mesh(
        absolute_path + "/output/mesh_output.obj",
        mesh,
        print_progress=True,
    )
    return mesh
