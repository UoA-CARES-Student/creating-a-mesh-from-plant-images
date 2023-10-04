# 3D Model processing and mesh generation

The following are a set of python projects which take multiple points cloud, pre aligned to each other, combines them and applies filtering to create a complete less noisy point cloud.

## Running the Virtual Environment

Install virtualenv

```
pip3 install virtualenv
```

Then create the virtual environment folder, where the version is the locally installed version of python and the venv is the folder name or path to where you want the virtual environment folder to be created

```
virtualenv -p python3.10 venv
```

Next run the correct activation script to start the virtual environment

For Linux and Mac
| Shell | Command |
| ----------- | ----------- |
| bash/zsh | `source venv/bin/activate`|
| PowerShell | `venv/bin/Activate.ps1`|
| fish | `source venv/bin/activate.fish` |
| csh/tcsh | `source venv/bin/activate.csh` |

For Windows
| Shell | Command |
| ----------- | ----------- |
| cmd.exe | `venv\Scripts\activate.bat`|
| PowerShell | `venv\Scripts\Activate.ps1`|

On success the terminal path should includes env, signifying an activated virtual environment.

Finally run the following command to install all the project requirements onto the virtual environment

```
pip install -r requirements.txt
```

To deactivate the environment run

```
deactivate
```

## Running the Project

To run this project, run one of the following command after completing the installation sets above

If you do not want to use a gpu to run

```bash
python model_processing/main.py
```

If you do want to use a gpu to run

```bash
python model_processing/main_gpu.py
```

With each of these commands you can add the following flags to run specific functions, supports multiple flags if you want to regenerate the model, display it, and run all metrics

| Shorten | Full              | Function                               |
| ------- | ----------------- | -------------------------------------- |
| `-g`    | '`--generate`'    | regenerates the complete model         |
| `-d`    | '`--display`'     | displays the result after filtering    |
| `-a`    | '`--all`'         | runs all metrics                       |
| `-c`    | '`--controlled`'  | runs the controlled experiment metrics |
| `-f`    | '`--feature`'     | runs the feature compare metric        |
| `-p`    | '`--photometric`' | runs the photometric error metric      |

## Troubleshooting

If you have a M1 Mac book and getting the following error you must install libomp with homebrew

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Users/.../creating-a-mesh-from-plant-images/model_processing/venv/lib/python3.9/site-packages/open3d/__init__.py", line 93, in <module>
    from open3d.cpu.pybind import (core, camera, data, geometry, io, pipelines,
ImportError: dlopen(/Users/.../creating-a-mesh-from-plant-images/model_processing/venv/lib/python3.9/site-packages/open3d/cpu/pybind.cpython-39-darwin.so, 0x0002): Library not loaded: /opt/homebrew/opt/libomp/lib/libomp.dylib
  Referenced from: <6C0FB50D-E600-3D2F-AF11-C0935C1FBD7C> /Users/.../creating-a-mesh-from-plant-images/model_processing/venv/lib/python3.9/site-packages/open3d/cpu/pybind.cpython-39-darwin.so
  Reason: tried: '/opt/homebrew/opt/libomp/lib/libomp.dylib' (no such file), '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/opt/libomp/lib/libomp.dylib' (no such file), '/opt/homebrew/opt/libomp/lib/libomp.dylib' (no such file), '/usr/local/lib/libomp.dylib' (no such file), '/usr/lib/libomp.dylib' (no such file, not in dyld cache)
```

See here to install homebrew https://brew.sh/

Then run

```
brew install libomp
```
