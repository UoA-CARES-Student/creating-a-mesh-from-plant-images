# Creating a mesh from plant point clouds

## Introduction

The following are a set of python projects for filtering and down sampling point clouds, then creating a mesh.

## Prerequisites

Please specify all the dependencies for your project. For example,

- Python 3.10
- virtualenv 20.23.1

## Installation guide

Full installation guide is detailed in model_processing README.md and MaaraTools README.md.

## How to run

Full run guide is detailed in model_processing README.md and MaaraTools README.md.

## Directory hierarchy & Code structure

<pre>
creating-a-mesh-from-plant-images
├── LICENSE
├── MaaraTools
│   ├── LICENSE
│   ├── Libraries
│   │   └── NVLib
│   │       ├── CMakeLists.txt
│   │       └── NVLib
│   │           ├── ...
│   ├── README.md
│   └── Utils
│       ├── CloudGen
│       │   ├── ArgReader.h
│       │   ├── CMakeLists.txt
│       │   ├── Frame.h
│       │   ├── PathHelper.cpp
│       │   ├── PathHelper.h
│       │   └── Source.cpp
│       └── Importer
│           ├── ArgReader.h
│           ├── CMakeLists.txt
│           ├── Frame.h
│           ├── FrameSet.cpp
│           ├── FrameSet.h
│           ├── Resources
│           │   ├── Input
│           │   │   └── input.txt
│           │   └── Output
│           │       └── output.txt
│           └── Source.cpp
├── README.md
└── model_processing
    ├── README.md
    ├── input
    │   └── README.md
    ├── model_processing
    │   ├── add_gausian_noise.py
    │   ├── create_complete_model.py
    │   ├── create_mesh.py
    │   ├── feature_compare.py
    │   ├── feature_compare_gpu.py
    │   ├── feature_compare_test.py
    │   ├── filtering.py
    │   ├── gpu_test.py
    │   ├── main.py
    │   ├── main_gpu.py
    │   ├── metrics.py
    │   ├── metrics_gpu.py
    │   ├── photometric_error.py
    │   ├── photometric_error_gpu.py
    │   ├── test.py
    │   ├── utils.py
    │   ├── validate.py
    │   └── validate_gpu.py
    ├── output
    │   └── README.md
    ├── requirements.txt
    └── setup.py

</pre>

And describe what each file does.

- LICENSE: license for this project
- README.md: Project information
- MaaraTools/LICENSE: license for Maara tools project
- MaaraTools/Libraries: library of dependencies for Maara tools project
- MaaraTools/README.md: Maara tools project information
- MaaraTools/Utils/CloudGen: Takes the images of an _imported Maaratech dataset_ and converts them into a set of point clouds in PLY format
- MaaraTools/Utils/Importer: Takes the standard output of the _Maaratech_ capture system and converts it into a format more compatible with OpenCV.
- model_processing/README.md: Model processing project information
- model_processing/input: folder for reading point cloud input
- model_processing/input/README.md: description of file input naming conventions
- model_processing/model_processing/main.py: main file which controls the running process and flags for runs without gpu
- model_processing/model_processing/main_gpu.py: main file which controls the running process and flags for runs with gpu
- model_processing/model_processing/filtering.py: controls running all filtering on point cloud
- model_processing/model_processing/add_gausian_noise.py: adds gausian noise to a point cloud
- model_processing/model_processing/create_complete_model.py: combines all point clouds within the input/data folder
- model_processing/model_processing/create_mesh.py: methods to create a mesh from a point cloud
- model_processing/model_processing/feature_compare.py: runs feature compare metrics on a point cloud
- model_processing/model_processing/feature_compare_test.py: test file for feature compare dev
- model_processing/model_processing/gpu_test.py: test file for gpu programs
- model_processing/model_processing/metrics.py: runs metrics for controlled experiment metric
- model_processing/model_processing/metrics_gpu.py: runs metrics for controlled experiment metric on gpu
- model_processing/model_processing/photometric_error.py: runs photometric error metrics on a point cloud
- model_processing/model_processing/photometric_error_gpu.py: runs photometric error metrics on a point cloud on gpu
- model_processing/model_processing/utils.py: utils methods
- model_processing/model_processing/validate.py: controls running controlled experiment metrics
- model_processing/model_processing/validate_gpu.py: controls running controlled experiment metrics on gpu
- model_processing/output: folder for model processing point cloud outputs
- model_processing/output/README.md: description of file output naming conventions
- model_processing/requirements.txt: project dependencies
- model_processing/requirements_gpu.txt: project dependencies on gpu
- model_processing/setup.py: project set up description

## Known issues & workaround

Full issues guide is detailed in model_processing README.md and MaaraTools README.md.
