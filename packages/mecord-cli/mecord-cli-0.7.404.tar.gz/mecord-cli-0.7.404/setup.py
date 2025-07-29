import setuptools
import os
import subprocess
import datetime

mecord_version = "0.7.404"
mecord_build_number = int(mecord_version.replace(".",""))
cur_dir = os.path.dirname(os.path.abspath(__file__))
constanspy = os.path.join(cur_dir, "mecord", "constant.py")
try:
    result = subprocess.run("git config user.email", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    build_user = "Noh"
    if result.returncode == 0:
        build_user = result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
    build_pts = datetime.datetime.today()

    with open(constanspy, 'w') as f:
        f.write(f'''#!!!!! do not change this file !!!!!
app_version="{mecord_version}"
app_bulld_number={mecord_build_number}
app_bulld_anchor="{build_user}_{build_pts}"
app_name="mecord-cli"
''')
except:
    with open(constanspy, 'w') as f:
        f.write(f'''#!!!!! do not change this file !!!!!
app_version="0.0.1"
app_bulld_number=1
app_bulld_anchor=""
app_name="mecord-cli"
''')

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="mecord-cli",
    version=mecord_version,
    author="pengjun",
    author_email="mr_lonely@foxmail.com",
    description="mecord tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mecordofficial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['windows', 'public_tools'],
    # data_files=[
    #     ('widget_template', [
    #         'mecord/widget_template/config.json',
    #         'mecord/widget_template/icon.png',
    #         'mecord/widget_template/index.html'
    #         ]),
    #     ('script_template', [
    #         'mecord/scrip_template/main.py',
    #         'mecord/scrip_template/run.py'
    #         ])
    # ],
    install_requires=[
        'requests',
        'uuid',
        'Image',
        'pillow',
        'protobuf',
        'oss2',
        'psutil',
        'pynvml',
        'requests_toolbelt',
        'matplotlib',
        'ping3',
        'piexif',
        'gputil',
        'urlparser',
        'setuptools',
        'twine',
        'uvicorn>=0.21.1',
        'fastapi>=0.94.0',
        'python-crontab',
        'websocket-client>=1.7.0'
    ],
    dependency_links=[],
    entry_points={
        'console_scripts':[
            'mecord = mecord.main:main'
        ]
    },
    # scripts=[
    #     'mecord/upload.py'
    # ],
    python_requires='>=3.4',
)
