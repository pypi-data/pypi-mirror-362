import os
import platform
import subprocess

sd_launch = os.environ.get('SD_LAUNCH')

if os.path.exists(sd_launch):
    if platform.system() == 'Windows':
        subprocess.call([sd_launch])
    else:
        subprocess.call(['sh', sd_launch])
else:
    print(f"Error: {sd_launch} not found.")


