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
| cmd.exe | `C:\> venv\Scripts\activate.bat`|
| PowerShell | `PS C:\> venv\Scripts\Activate.ps1`|

On success the terminal path should includes env, signifying an activated virtual environment.

Finally run the following command to install all the project requirements onto the virtual environment

```
pip install -r requirements.txt
```

To deactivate the environment run

```
deactivate
```

## Running the Projects
