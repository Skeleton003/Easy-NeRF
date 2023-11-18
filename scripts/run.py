import runpy
import sys
import os
from pynvml import *

nvmlInit()
deviceCount = nvmlDeviceGetCount()
if (deviceCount == 0):
    print("No device found")
    quit()

arch = 0
for i in range(deviceCount):
    handle = nvmlDeviceGetHandleByIndex(i)
    get_arch = nvmlDeviceGetArchitecture(handle)
    if get_arch in [4, 6, 7, 8]:
        arch = get_arch
        break
nvmlShutdown()

if arch == 0:
    print("No supported GPU found")
    quit()

data_dir = os.path.dirname(sys.argv[1])

sys.argv = [
    "scripts/colmap2nerf.py", "--video_in", sys.argv[1], "--video_fps", "2",
    "--run_colmap", "--aabb_scale", "32", "--overwrite"
]
if os.path.exists(os.path.join(data_dir, "transforms.json")) == False:
    runpy.run_path(path_name='scripts/colmap2nerf.py', run_name='__main__')

if (arch == 4):
    os.system(f"ngp_pascal {data_dir}")
elif (arch == 6):
    os.system(f"ngp_turing {data_dir}")
else:
    os.system(f"ngp_ampere.exe {data_dir}")
