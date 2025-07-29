import os
import json
import sys
import shutil
import zipfile
import pkg_resources
import threading
import time
import requests
import random
import subprocess
import platform
import re
from pkg_resources import get_distribution
import socket

from pathlib import Path
from mecord import store
from mecord import xy_pb
from mecord import upload
from mecord import taskUtils
from mecord import utils
thisFileDir = os.path.dirname(os.path.abspath(__file__))
meco = os.path.exists(os.path.join(thisFileDir, "meco"))
def is_running():

    pid_file = os.path.join(thisFileDir, "MecordService.pid")
    if pid_file and os.path.exists(pid_file):
        with open(pid_file, 'r', encoding='UTF-8') as f:
            pid = int(f.read())
            try:
                if utils.process_is_alive(pid):
                    return True
                else:
                    return False
            except OSError:
                return False
    else:
        return False
def _pipServerUrl():
    if meco:
        return "https://meco-mvn.2tianxin.com/repository/mecord/simple"
    else:
        return "https://mvn.miyachat.com/nexus/repository/mecord/simple"

def _pipUploadServerUrl():
    if meco:
        return "https://meco-mvn.2tianxin.com/repository/mecord/"
    else:
        return "https://mvn.miyachat.com/nexus/repository/mecord/"

def compare_versions(version1, version2):
    if len(version1) <= 0:
        version1 = "0"
    if len(version2) <= 0:
        version2 = "0"
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))
    while len(v1) < len(v2):
        v1.append(0)
    while len(v2) < len(v1):
        v2.append(0)
    for i in range(len(v1)):
        if v1[i] < v2[i]:
            return -1
        elif v1[i] > v2[i]:
            return 1
    return 0

def _remote_package_version(py_package):
    remote_version = ""
    result = subprocess.run(f"pip index versions {py_package} -i {_pipServerUrl()}", 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ss = result.stdout.decode(encoding="utf8", errors="ignore").split("\n")
    for s in ss:
        if "LATEST:" in s.strip():
            remote_version = s.replace("LATEST:", "").strip()
    return remote_version

#real time version get
def _local_package_version(py_package):
    find_str = "grep"
    if platform.system() == 'Windows':
        find_str = "findstr"
    local_version = ""
    result = subprocess.run(f"pip list | {find_str} {py_package}", 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ss = result.stdout.decode(encoding="utf8", errors="ignore").split("\n")
    for s in ss:
        s = re.sub(r'\s+', ' ', s)
        sl = s.strip().split(" ")
        if len(sl) == 2:
            if py_package.strip() == sl[0].strip():
                local_version = sl[1].strip()
    return local_version

def _pypi_folder_name(name):
    import re
    return re.sub(r"[/,\-\s]", "", name)

h5_name = "h5"
script_name = "script"
def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
    if os.path.exists(os.path.join(path, h5_name)):
        for filename in os.listdir(os.path.join(path, h5_name)):
            pathname = os.path.join(path, h5_name, filename) 
            if (os.path.isfile(pathname)) and filename in ["config.json", "config.json.py"]:
                with open(pathname, 'r', encoding='UTF-8') as f:
                    return json.load(f)
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename in ["config.json", "config.json.py"]:
            with open(pathname, 'r', encoding='UTF-8') as f:
                return json.load(f)
    return {}

def folderIsH5(path):
    configFileExist = False
    iconFileExist = False
    htmlFileExist = False
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            configFileExist = True
        if (os.path.isfile(pathname)) and filename == "icon.png":
            iconFileExist = True
        if (os.path.isfile(pathname)) and filename == "index.html":
            htmlFileExist = True
    return configFileExist and iconFileExist and htmlFileExist

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def checkImportMecordJs(h5Root):
    jsPath = os.path.join(h5Root, "MekongJS.js")
    jsPathTmp = os.path.join(h5Root, "MekongJS.js.py")
    s = requests.session()
    s.keep_alive = False
    js_res = s.get(f"https://www.mecordai.com/prod/mecord/commonality/MecordJS/MecordJS.min.js?t={random.randint(100,99999999)}")
    with open(jsPathTmp, "wb") as c:
        c.write(js_res.content)
    if os.path.exists(jsPathTmp):
        if os.path.exists(jsPath):
            os.remove(jsPath)
        os.rename(jsPathTmp, jsPath)
    s.close()

def replaceIfNeed(dstDir, name, subfix):
    newsubfix = subfix + ".py"
    if name.find(newsubfix) != -1:
        os.rename(os.path.join(dstDir, name), os.path.join(dstDir, name.replace(newsubfix, subfix)))

def copyWidgetTemplate(root, name, dirname):
    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)#sys.prefix
    dstDir = os.path.join(root, dirname)
    shutil.copytree(templateDir, dstDir)
    shutil.rmtree(os.path.join(dstDir, "__pycache__"))
    os.remove(os.path.join(dstDir, "__init__.py"))
    for filename in os.listdir(dstDir):
        replaceIfNeed(dstDir, filename, ".json")
        replaceIfNeed(dstDir, filename, ".js")
        replaceIfNeed(dstDir, filename, ".png")
        replaceIfNeed(dstDir, filename, ".html")

default_max_task_number = 10
def setWidgetData(root, widgetid):
    #h5
    data = GetWidgetConfig(root)
    data["name"] = os.path.basename(root)
    data["parent_widget_id"] = ""
    data["widget_id"] = widgetid
    data["group_id"] = '58b32fde-a39d-58b3-b98e-30f48fd225b5'
    data["device_keys"] = [
        utils.generate_unique_id()
    ]
    data["cmd"] = os.path.join(root, script_name, "main.py")
    data["max_task_number"] = default_max_task_number
    with open(os.path.join(root, h5_name, "config.json"), 'w') as f:
        json.dump(data, f)
    checkImportMecordJs(os.path.join(root, h5_name))
    #script
    with open(os.path.join(root, script_name, "config.json"), 'w') as f:
        json.dump({"widget_id": widgetid}, f)

def createWidget(root):
    if PathIsEmpty(root) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = xy_pb.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create widget fail! mecord server is not avalid")
        return
    
    copyWidgetTemplate(root, "widget_template", h5_name)
    copyWidgetTemplate(root, "script_template", script_name)
    setWidgetData(root, widgetid)
    addWidgetToEnv(os.path.join(root, script_name))
    print("create widget success")

def CheckWidgetDataInPath(path):
    data = GetWidgetConfig(path)
    if "widget_id" not in data:
        print("folder is not widget")
        return False

    if "widget_id" in data:
        widget_id = data["widget_id"]
        if len(widget_id) == 0:
            print("widget_id is empty!")
            return False
        
    return True

def addWidgetToEnv(root):
    refreshMessage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refreshMessage")
    if is_running():
        with open(refreshMessage, 'w') as f:
            f.write("")
    else:
        if os.path.exists(refreshMessage):
            os.remove(refreshMessage)

    #maybe pip package
    try:
        package = pkg_resources.get_distribution(root)
        local_version = package.version
        name = package.project_name
        version = package.version
        root = os.path.join(package.location, _pypi_folder_name(name))
    except:
        pass

    if CheckWidgetDataInPath(root) == False:
        return
    data = GetWidgetConfig(root)
    widget_id = data["widget_id"]
    mainPythonPath = os.path.join(root, "main.py")
    if os.path.exists(os.path.join(root, script_name)):
        mainPythonPath = os.path.join(root, script_name, "main.py")
    store.insertWidget(widget_id, mainPythonPath)
    print(f"add {widget_id.ljust(len(widget_id)+4)} {mainPythonPath}")

def remove(args):
    refreshMessage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refreshMessage")
    if is_running():
        with open(refreshMessage, 'w') as f:
            f.write("")
    else:
        if os.path.exists(refreshMessage):
            os.remove(refreshMessage)
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    # if xy_pb.DeleteWidget(widget_id):
    store.removeWidget(widget_id)
    print(f"widget:{widget_id} is removed with local")
        
def enable(args):
    refreshMessage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refreshMessage")
    if is_running():
        with open(refreshMessage, 'w') as f:
            f.write("")
    else:
        if os.path.exists(refreshMessage):
            os.remove(refreshMessage)
    if args == 'all':
        store.enableWidgetall()
        print(f"All widgets are enabled")
    else:
        widget_id = args
        if os.path.exists(args):
            #find widgetid in args path
            data = GetWidgetConfig(args)
            if "widget_id" not in data:
                print(f"path {args} is not widget folder!")
                return
            widget_id = data["widget_id"]
        store.enableWidget(widget_id)
        print(f"widget:{widget_id} updated")
        
def disable(args):
    refreshMessage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refreshMessage")
    if is_running():
        with open(refreshMessage, 'w') as f:
            f.write("")
    else:
        if os.path.exists(refreshMessage):
            os.remove(refreshMessage)
    if args == 'all':
        store.disableWidgetall()
        print(f"All widgets are disabled")
    else:
        widget_id = args
        if os.path.exists(args):
            #find widgetid in args path
            data = GetWidgetConfig(args)
            if "widget_id" not in data:
                print(f"path {args} is not widget folder!")
                return
            widget_id = data["widget_id"]
        store.disableWidget(widget_id)
        print(f"widget:{widget_id} updated")

def mark(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    # if xy_pb.DeleteWidget(widget_id):
    store.markWidget(widget_id)
    print(f"widget:{widget_id} mark")

def unmark(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    # if xy_pb.DeleteWidget(widget_id):
    store.unmarkWidget(widget_id)
    print(f"widget:{widget_id} unmark")
        
def getTaskCount(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    datas = xy_pb.GetTaskCount(widget_id)
    for it in datas:
        if it["widgetUUID"] == widget_id:
            return it["taskCount"]
    return -1

def publishWidget(root):
    if CheckWidgetDataInPath(root) == False:
        return
    #h5 folder
    package_folder = ""
    script_folder = ""
    if folderIsH5(root):
        package_folder = root
    elif folderIsH5(os.path.join(root, h5_name)):
        script_folder = os.path.join(root, script_name)
        package_folder = os.path.join(root, h5_name) 
        
    data = GetWidgetConfig(package_folder)
    widget_id = data["widget_id"]
    name = data["name"]
    local_version = data["version"]
    group_id = data["group_id"]
    user_id = utils.generate_unique_id()

    #override setting
    remote_version = _remote_package_version(name)
    if compare_versions(remote_version, local_version) >= 0:
        print(f"version {local_version} must be larger than {remote_version}, publish abandon")
        return
        
    #if in h5&script parent folder, add env path
    if len(script_folder) > 0:
        addWidgetToEnv(script_folder)
        
    #package python to private pip server
    requirements_txts = [
        os.path.join(script_folder, "requirements.txt"),
        os.path.join(os.path.dirname(package_folder), "requirements.txt")
    ]
    requirements = ""
    for requirements_txt in requirements_txts:
        if os.path.exists(requirements_txt):
            with open(requirements_txt, "r", encoding="UTF-8") as f:
                ss = f.readlines()
                for s in ss:
                    reals = s.replace("\n","").replace(" ","")
                    if ";" in reals:
                        requirements += f"'{reals[:reals.index(';')]}',"  
                    elif "#" not in reals:
                        requirements += f"'{reals}',"
    pip_dir = os.path.join(os.path.dirname(package_folder), "tmp")
    if os.path.exists(pip_dir):
        shutil.rmtree(pip_dir)
    os.makedirs(pip_dir)
    source_folder_name = _pypi_folder_name(name)
    pip_source_dir = os.path.join(pip_dir, source_folder_name)
    shutil.copytree(script_folder, pip_source_dir)
    config_json_file = os.path.join(pip_source_dir, "config.json") 
    if os.path.exists(config_json_file):
        with open(config_json_file, 'r') as f:
            cc = json.load(f)
        cc["py_package"] = name
    else:
        shutil.copy(os.path.join(package_folder, "config.json"), config_json_file)
        with open(config_json_file, 'r') as f:
            cc = json.load(f)
        cc["py_package"] = name
    if os.path.exists(os.path.join(pip_source_dir, "__init__.py")) == False:
        with open(os.path.join(pip_source_dir, "__init__.py"), 'w') as f:
            f.write("")
    #get datafile
    data_file_config = {}
    for root,dirs,files in os.walk(pip_source_dir):
        for file in files:
            if file.find(".") > 0 and file[file.rindex("."):] == ".py":
                continue
            if root.startswith("."):#hidding files
                continue
            dir_path = os.path.relpath(root, pip_source_dir)
            file_path = os.path.join(dir_path, file)
            file_path = os.path.normpath(file_path).replace("\\", "/")
            k = dir_path.replace("\\", "/")
            if k in data_file_config:
                data_file_config[k].append(file_path)
            else:
                data_file_config[k] = [file_path]
    package_data_str = ""
    for k in data_file_config:
        for p in data_file_config[k]:
            package_data_str += f"'{p}',"
    setup_py = os.path.join(pip_dir, "setup.py")
    with open(setup_py, 'w') as f:
        f.write(f'''import setuptools, os, sys, subprocess, datetime
    
setuptools.setup(
    name="{name}",
    version="{local_version}",
    author="{user_id}",
    author_email="{user_id}@xinyu668.com",
    description="mecord widget",
    long_description="privide by mecord-cli",
    long_description_content_type="text/markdown",
    url="https://mecordai.com/#/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[],
    install_requires=[
        {requirements}
    ],
    package_data={{
        '{source_folder_name}':[{package_data_str}]
    }},
    entry_points={{
        'console_scripts':[
            '{name} = {source_folder_name}.main:main'
        ]
    }},
    python_requires='>=3.4',
)
''')
    try:
        #build
        subprocess.run(f"python {setup_py} sdist bdist_wheel", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=pip_dir, encoding="utf-8")
        #uninstall
        subprocess.run(f"pip uninstall {name} -y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
        #install
        whl = utils.firstExitWithDir(os.path.join(pip_dir, "dist"), "whl")
        subprocess.run(f"pip install {whl} --extra-index-url https://pypi.python.org/simple/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
        #upload
        subprocess.run(["twine",
                        "upload",
                        "-u","admin" if meco else "mecord-adm",
                        "-p","%dSPB60rgY#oeSFH",
                        "--repository-url", _pipUploadServerUrl(),
                        f"{pip_dir}/dist/*"])
        print(f"发布 {name}_{local_version} -> pypi成功")
    except Exception as ex:
        print(ex)
    finally:
        shutil.rmtree(pip_dir)
        pass
        
    #package h5 & script code to mecord server
    distname = utils.generate_unique_id() + "_" + widget_id
    dist = os.path.join(os.path.dirname(package_folder), distname + ".zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    checkImportMecordJs(package_folder)
    for rt,dirs,files in os.walk(package_folder):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, package_folder)
            zip.write(filepath, writepath)
    zip.close()
    (ossurl, checkid) = upload.uploadWidget(dist, widget_id)
    if checkid > 0:
        checkUploadComplete(checkid, dist)
    else:
        os.remove(dist)

def checkUploadComplete(checkid, dist):
    rst = xy_pb.UploadWidgetCheck(checkid)
    if rst == 1: #success
        print("publish widget success")
        # xy_pb.UploadWidget(widget_id, ossurl)  #暂时不用
        os.remove(dist)
        store.finishCreateWidget()
    elif rst == -1:
        threading.Timer(1, checkUploadComplete, (checkid, dist, )).start()
    else: #fail
        print("publish fail")
        return

def widgetUpdateNotify(widgetName, oldver, newver):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("mecord-cli").version
    taskUtils.notifyWechatRobot("us", {
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]>[{ver}] widget:[{widgetName}]升级版本[{oldver}]->[{newver}]"
        }
    })

def UpdateWidgetFromPypi():
    map = store.widgetMap()
    for it in map:
        is_block = False
        if isinstance(map[it], (dict)):
            is_block = map[it]["isBlock"]
            path = map[it]["path"]
        else:
            path = map[it]
        path = os.path.dirname(path)
        if is_block == False and os.path.exists(path):
            data = GetWidgetConfig(path)
            if "py_package" in data and len(data["py_package"]) > 0:
                try:
                    py_package = data["py_package"]
                    remote_version = _remote_package_version(py_package)
                    local_version = _local_package_version(py_package)
                    if compare_versions(remote_version, local_version) > 0:
                        #update
                        subprocess.run(f"pip uninstall {py_package}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, timeout=15)
                        subprocess.run(f"pip install -U {py_package} -i {_pipServerUrl()} --extra-index-url https://pypi.python.org/simple/", 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, timeout=15)
                        widgetUpdateNotify(py_package, local_version, remote_version)
                except Exception as ex:
                    print(ex)
                    continue

def installWidget(args):

    def find_widget(path):
        for _root, dirs, files in os.walk(path):
            if '__init__.py' in files:
                return os.path.abspath(_root)

    root = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) == 5:
        path = sys.argv[4] + r'/widgets'
    else:
        path = root + r'/widgets'

    widgetName = args
    widget_dir = path + f'/{widgetName}'
    downloadpath = path + f'/download'
    if os.path.exists(downloadpath):
        shutil.rmtree(downloadpath, ignore_errors=True)
    os.makedirs(downloadpath)
    widget_template = os.path.join(os.path.dirname(os.path.abspath(__file__))) + f'/widget_template'


    h5_path = widget_dir + r'/h5'
    scr_path = widget_dir + r'/script'


    ver_cmd = f'pip index versions {widgetName} -i {_pipServerUrl()}'
    result = subprocess.run(ver_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ss = result.stdout.decode(encoding="utf8", errors="ignore").split("\n")
    version = re.search('\((.*?)\)', ss[0]).groups()[0]
    cmd_str = f'pip install {widgetName}=={version} --no-deps --no-cache-dir -i {_pipServerUrl()} -t {downloadpath}'
    subprocess.run(cmd_str.split(' '))

    if os.path.exists(widget_dir):
        shutil.rmtree(widget_dir)
    os.makedirs(widget_dir)

    widget_base = find_widget(downloadpath)
    shutil.copytree(widget_base, scr_path)
    os.remove(os.path.join(scr_path, "__init__.py"))

    shutil.copytree(widget_template, h5_path)
    os.remove(os.path.join(h5_path, "__init__.py"))


    for _root, dirs, files in os.walk(h5_path):
        for file in files:
            os.rename(_root+'/'+file, _root+'/'+file.replace('.py', ''))

    data = GetWidgetConfig(widget_base)
    widgetid = data.get("widget_id", '')
    data["version"] = version
    data["parent_widget_id"] = ""
    data["widget_id"] = widgetid
    data["group_id"] = '58b32fde-a39d-58b3-b98e-30f48fd225b5'
    data["device_keys"] = [
        utils.generate_unique_id()
    ]
    data["cmd"] = os.path.join(scr_path, "main.py")
    data["max_task_number"] = default_max_task_number
    with open(os.path.join(h5_path, "config.json"), 'w') as f:
        json.dump(data, f)
    checkImportMecordJs(h5_path)
    #script
    with open(os.path.join(scr_path, "config.json"), 'w') as f:
        json.dump({"widget_id": widgetid}, f)
    addWidgetToEnv(os.path.join(widget_dir))
    install_requirements(scr_path)

    if os.path.exists(downloadpath):
        shutil.rmtree(downloadpath)

def install_requirements(scr_path):
    # 检查可能的文件名
    requirements_files = [
        os.path.join(scr_path, 'requirements.txt'),
        os.path.join(scr_path, 'requirements')
    ]

    found = False

    for file_path in requirements_files:
        if os.path.isfile(file_path):
            print(f"找到依赖文件: {file_path}")
            try:
                # 使用当前Python环境的pip安装依赖
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-r', file_path],
                    check=True
                )
                print("依赖安装成功。")
                found = True
                break
            except subprocess.CalledProcessError as e:
                print(f"安装依赖失败，错误信息: {e}")
                found = True  # 文件存在但安装失败
                break
            except Exception as e:
                print(f"发生未知错误: {e}")
                found = True
                break

    if not found:
        print(f"目录 {scr_path} 中未找到requirements.txt或requirements文件。")
