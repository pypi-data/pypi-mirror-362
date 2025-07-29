import uuid
import platform
import subprocess
import os
import sys
import requests
from io import BytesIO
import psutil
import pynvml
from datetime import datetime, timedelta
import http
import json
from pathlib import Path
import zipfile
import socket
from PIL import Image
from urllib.parse import urlparse, urlunparse
import time

def get_mac_from_nettools():
    try:
        cmd = "ifconfig"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode(encoding='UTF-8')
        mac = output_str[output_str.index('ether') + 6:output_str.index('ether') + 23].replace(':', '')
        return True, mac
    except Exception as e:
        return False, None
    
def get_mac_from_system():
    try:
        root_path = '/sys/class/net/'
        dbtype_list = os.listdir(root_path)
        for dbtype in dbtype_list:
            if os.path.isfile(os.path.join(root_path, dbtype)):
                dbtype_list.remove(dbtype)

        if len(dbtype_list) == 0:
            return False, None
        mac = ''
        for dbtype in dbtype_list:
          cmd = f"cat {root_path}{dbtype}/address"
          output = subprocess.check_output(cmd, shell=True)
          mac += output.decode(encoding='UTF-8')
        return True, mac
    except Exception as e:
        return False, None

mac_value = ""
def get_mac_address():
    global mac_value
    if mac_value and len(mac_value) > 0:
        return mac_value
    
    if platform.system() == 'Windows':
        cmd = "ipconfig /all"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.find('Physical Address')
        if pos == -1:
            pos = output_str.find('物理地址')
        mac_value = (output_str[pos:pos+100].split(':')[1]).strip().replace('-', '')
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        ok, mac_value = get_mac_from_nettools()
        if ok:
            return mac_value
        ok, mac_value = get_mac_from_system()
        if ok:
            return mac_value
        return None
    else:
        mac_value = None
    return mac_value

cpu_serial = ""
def get_cpu_serial():
    global cpu_serial
    if cpu_serial and len(cpu_serial) > 0:
        return cpu_serial
    
    if platform.system() == 'Windows':
        cmd = "wmic cpu get ProcessorId"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.index("\n")
        cpu_serial = output_str[pos:].strip()
    elif platform.system() == 'Linux':
        with open('/proc/cpuinfo') as f:
            
            for line in f:
                if line[0:6] == 'Serial':
                    return "1"
                if line.strip().startswith('serial'):
                    cpu_serial = line.split(":")[1].strip()
                    break
        if not cpu_serial:
            cpu_serial = None
    elif platform.system() == 'Darwin':
        cmd = "/usr/sbin/system_profiler SPHardwareDataType"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode(encoding='UTF-8')
        cpu_serial = output_str[output_str.index('Hardware UUID:') + 14:output_str.index('Hardware UUID:') + 51].replace('-', '')
    else:
        cpu_serial = None
    return cpu_serial

def get_hostname():
    return socket.gethostname()

def generate_unique_id(mtype=''):
    mac = get_mac_address()
    cpu_serial = get_cpu_serial()
    hostname = get_hostname()
    if mac and cpu_serial:
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac + cpu_serial + hostname + (mtype if mtype == '-h' else ''))
        return str(unique_id).replace('-', '')
    if mac :
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac + hostname + (mtype if mtype == '-h' else ''))
        return str(unique_id).replace('-', '')

def getOssImageSize(p):
    try:
        s = requests.session()
        s.keep_alive = False
        res = s.get(p, timeout=60)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0
    
def deviceInfo():
    mac = get_mac_address()
    mac = "" if mac == None else mac
    cpu_serial = get_cpu_serial()
    cpu_serial = "" if cpu_serial == None else cpu_serial
    hostname = get_hostname()
    M=1024*1024
    data = {
        "cpu": {
            "logical_count" : psutil.cpu_count(),
            "count" : psutil.cpu_count(logical=False),
            "max_freq" : f"{psutil.cpu_freq().max / 1000} GHz",
        },
        "memory": {
            "total" : f"{psutil.virtual_memory().total/M} M",
            "free" : f"{psutil.virtual_memory().free/M} M"
        },
        "gpu": {
            "count" : 0,
            "list" : [],
            "mem" : []
        },
        "device_id": generate_unique_id(),
        "host_name": hostname
    }
    try:
        pynvml.nvmlInit()
        gpuCount = pynvml.nvmlDeviceGetCount()
        data["gpu"]["count"] = gpuCount
        for i in range(gpuCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            data["gpu"]["list"].append(f"GPU{i}: {pynvml.nvmlDeviceGetName(handle)}")
            memInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            data["gpu"]["mem"].append(f"GPU{i}: total:{memInfo.total/M} M free:{memInfo.free/M} M")
            
        pynvml.nvmlShutdown()
    except Exception as e:
        data["gpu"]["count"] = 1
        data["gpu"]["list"].append(f"GPU0: Normal")
    return data

def reportLog():
    reason = ""
    if len(sys.argv) >= 2:
        reason = sys.argv[2].strip().replace("\n","").replace(",","").replace(" ","").replace(";","")
    d = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    uid = generate_unique_id()

    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    dist = os.path.join(thisFileDir, f"{uid}_{reason}_{d}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 

    for root,dirs,files in os.walk(thisFileDir):
        for file in files:
            if str(file).startswith("~$"):
                continue
            ext = file[file.rindex("."):]
            if ext == ".log" or ext == ".json" or ".log." in file:
                filepath = os.path.join(root, file)
                zip.write(filepath, file)
        if root != files:
            break
    zip.close()
    ossurl = uploadOSS(dist)
    os.remove(dist)
    return ossurl

def uploadOSS(file):
    conn = http.client.HTTPSConnection("api.mecordai.com")
    payload = json.dumps({
        "sign": "f0463f490eb84133c0aab3a8576ed2fc"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/proxymsg/get_oss_config", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    if data["code"] == 0:
        AccessKeyId = data["data"]["AccessKeyId"]
        AccessKeySecret = data["data"]["AccessKeySecret"]
        SecurityToken = data["data"]["SecurityToken"]
        BucketName = data["data"]["BucketName"]
        Expiration = data["data"]["Expiration"]
        Endpoint = data["data"]["Endpoint"]
        CallbackUrl = data["data"]["CallbackUrl"]
        cdn = data["data"]["cdn"]
        
        if len(AccessKeyId) > 0:  
            import oss2
            auth = oss2.StsAuth(AccessKeyId, AccessKeySecret, SecurityToken)
            bucket = oss2.Bucket(auth, Endpoint, BucketName, connect_timeout=600)
            with open(file, "rb") as f:
                byte_data = f.read()
            file_name = Path(file).name
            publish_name = f"mecord/report/{file_name}" 
            bucket.put_object(publish_name, byte_data)
            return f"{cdn}{publish_name}" 
    else:
        print(f"get_oss_config fail: response={data}")

def changeDomain(url=''):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc

    if netloc == 'm.mecordai.com':
        return url
    elif 'mecord' in netloc:
        mecord_netloc = 'm.mecordai.com'
        mecord_url = parsed_url._replace(netloc=mecord_netloc)
        return urlunparse(mecord_url)
    else:
        return url

def directDomain(url=''):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    if 'mecord' in netloc:
        mecord_netloc = 'mecord-web-sg.oss-ap-southeast-1.aliyuncs.com'
        mecord_url = parsed_url._replace(netloc=mecord_netloc)
        return urlunparse(mecord_url)
    else:
        return url

def process_is_alive(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        pstatus = process.status()
        if pstatus == psutil.STATUS_RUNNING or pstatus == psutil.STATUS_SLEEPING:
            return True
        else:
            return False
    except (FileNotFoundError, psutil.NoSuchProcess):
        return False
    except Exception as e:
        return False
    
def process_is_zombie_but_cannot_kill(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        pstatus = process.status()
        if pstatus == psutil.STATUS_DISK_SLEEP:
            return True
    except Exception as e:
        return False
    return False
    
def firstExitWithDir(root, suffix):
    for root,dirs,files in os.walk(root):
        for file in files:
            if file.find(".") <= 0:
                continue
            ext = file[file.rindex("."):]
            if ext == f".{suffix}":
                return os.path.join(root, file)
        if root != files:
            break
    return None

def begin_restart(reason, update_cli=False, simple="https://pypi.python.org/simple/"):
    thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
    restart_file = os.path.join(thisFileDir, "restart")
    auto_restart = os.path.join(thisFileDir, "auto_restart")
    if os.path.exists(restart_file):
        os.remove(restart_file)
    stop_file = os.path.join(thisFileDir, "stop.now")
    with open(stop_file, 'w') as f:
        f.write("")
    waitlastTask = os.path.join(thisFileDir, "waitlastTask")
    with open(waitlastTask, 'w') as f:
        f.write("")
    if reason == '手动重启' or os.path.exists(auto_restart):  # 如果是'手动重启',或者设置了auto_restart,则重启mecord
        with open(restart_file, 'w') as f:
            json.dump({
                "reason": reason,
                "update_cli": update_cli,
                "simple": simple
            },f)
    
def check_restart():
    thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
    restart_file = os.path.join(thisFileDir, "restart")
    if os.path.exists(restart_file) == False:
        return
    from mecord import taskUtils
    from mecord import store
    import time, calendar, platform, subprocess
    reason = "unknow"
    update_cli = False
    simple = "https://pypi.python.org/simple/"
    try:
        with open(restart_file, 'r') as f:
            config = json.load(f)
            reason = config["reason"]
            update_cli = config["update_cli"]
            simple = config["simple"]
    except:
        pass

    if platform.system() == 'Windows':
        time_task_file = os.path.join(thisFileDir, "update_mecord.bat")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        time_task_file = os.path.join(thisFileDir, "update_mecord.sh")
    else:
        time_task_file = os.path.join(thisFileDir, "update_mecord.txt")
    if os.path.exists(time_task_file):
        os.remove(time_task_file)

    def getCommandResult(cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    print(" restart_mecord_cli begin...")
    taskUtils.restartNotify(reason)
    restart_command = "mecord service start"
    threadNum = store.get_multithread()
    if threadNum > 1:
        restart_command = f"{restart_command} -thread {threadNum}"
    env = store.get_env()
    restart_command = f"{restart_command} {env}"
    auto_restart = os.path.join(thisFileDir, "auto_restart")
    if os.path.exists(auto_restart):
        restart_command += ' -auto'
    if platform.system() == 'Windows':
        new_time = datetime.now() + timedelta(minutes=1)
        win_time = new_time.strftime("%H:%M")
        with open(time_task_file, 'w') as f:
            if update_cli:
                f.write(f'''pip uninstall mecord-cli -y 
pip install -U mecord-cli -i {simple} --extra-index-url https://pypi.python.org/simple/
start /B {restart_command}''')
            else:
                f.write(f'''start {restart_command}''')
        result = subprocess.Popen(['schtasks', '/create', '/sc', 'ONCE', '/st', f'{win_time}', '/tn', f'MecordUpdate-{calendar.timegm(time.gmtime())}', '/tr', f"\"{time_task_file}\""], shell=True)
        print(f"{result.stdout}\n{result.stderr}")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        def run_subprocess(s):
            r = subprocess.run(s, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            print(f"{r.stdout}\n{r.stderr}")
        if len(getCommandResult("which at")) <= 0:
            run_subprocess(f"apt-get update")
            run_subprocess(f"apt-get install -y at libopencv-features2d-dev=4.5.4+dfsg-9ubuntu4 systemctl")
        run_subprocess(f"systemctl start atd")
        with open(time_task_file, 'w') as f:
            if update_cli:
                f.write(f'''#!/bin/bash
pip uninstall mecord-cli -y 
pip install -U mecord-cli -i {simple} --extra-index-url https://pypi.python.org/simple/
nohup {restart_command} &''')
            else:
                f.write(f'''#!/bin/bash
nohup {restart_command} &''')
        ot = os.path.join(thisFileDir, "update_mecord.out")
        result = subprocess.run(f"at now + 1 minutes -f {time_task_file} > {ot}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print(f"{result.stdout}\n{result.stderr}")
    os.remove(restart_file)
    print("one minute later must be start!")

def runMonitor():
    import threading
    import nvidia_smi, time, json
    from datetime import datetime, timedelta
    import os
    from mecord import utils

    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    pid_file = os.path.join(thisFileDir, "MecordMonitor.pid")
    log_dir = os.path.join(thisFileDir, "monitor_log")

    def runner():
        num = 0
        gpu_counter = 0
        data = []
        while True:
            for i in range(deviceCount):
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                usage = util.gpu/100.00
                gpu_counter += usage
            num += 1
            time.sleep(0.1)
            if num % 10 == 0:
                if gpu_counter > 0:
                    gpu_usage = f"{gpu_counter/10:3.2f}"
                else:
                    gpu_usage = '0.0'
                data.append(float(gpu_usage))

                print('GPU: ', gpu_usage)
                gpu_counter = 0

            if num == 600:
                now = datetime.now()
                key = now.strftime("%Y-%m-%d %H:%M")
                _file = os.path.join(log_dir, str(now.date()))
                _data = {key: data, 'total': round(sum(data)/60, 2)}
                with open(_file, 'a+') as f:
                    f.write(str(_data))
                    f.write('\n')
                num = 0
                print('save data:', _data)
                data = []

    def datapost():
        today = datetime.now().date()
        _today = str(today)
        nextday = datetime.now() + timedelta(days=1)
        _nextday = str(nextday.date())
        _file = os.path.join(log_dir, _nextday)
        while True:
            if os.path.exists(_file):
                with open(_file, 'r') as f:
                    data = f.read()

                _host_name = utils.get_hostname()
                host_name = f'{_host_name}_monitor'
                url = 'https://mecord-beta.2tianxin.com/proxymsg/interior_config'
                json_data = {
                    "key": host_name,
                    "value": json.dumps(data),
                }
                resp = requests.post(url, json=json_data)
                print(resp.text)
                if resp.json()['msg'] == 'success':
                    print('success')
                else:
                    print('fail')

                today = datetime.now().date()
                _today = str(today)
                nextday = datetime.now() + timedelta(days=1)
                _nextday = str(nextday.date())
                _file = os.path.join(log_dir, _nextday)

            else:
                time.sleep(600)


    if pid_file and os.path.exists(pid_file):
        with open(pid_file, 'r', encoding='UTF-8') as f:
            pid = int(f.read())
            try:
                if utils.process_is_alive(pid):
                    is_running = True
                else:
                    is_running = False
            except OSError:
                is_running = False
    else:
        is_running = False
    if is_running:
        print('Monitor is running!!!')
        return
    else:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


    nvidia_smi.nvmlInit()
    deviceCount = nvidia_smi.nvmlDeviceGetCount()


    thread_monitor = threading.Thread(target=runner)
    thread_post = threading.Thread(target=datapost)
    # monitor_run = True
    thread_post.start()
    thread_monitor.start()

def tellNextTask(text=''):
    port = os.environ.get('ZEROPORT', text)
    try:
        url = f'http://127.0.0.1:8088/nextTask/?ZEROPORT={port}'
        resp = requests.get(url, timeout=1)
        print(resp.text)
    except Exception as e:
        pass

def checkServiceActivate():
    # 检测秋文的zeroimage服务是否正常运行
    try:
        res = requests.post(f"http://127.0.0.1:6007", json={"method": "obj.activate", "params": [], "id": 0}, timeout=10)
        # logging.info(f"req:{res.request.url}")
        # logging.debug(f"res:{res.content}")
        assert res.status_code == 200 or res.status_code == 404
        return True
    except Exception as e:
        # logging.error(e)
        return False

def restart_zeroimage():
    zero_process = subprocess.Popen(['supervisorctl', 'restart', 'zeroimage:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = zero_process.communicate()
    print("stdout:\n", stdout)
    print("stderr:\n", stderr)
    start_time = time.time()
    check_flag = True
    server_flag = False
    test_path = "/root/autodl-fs/new_widgets/MecoImageCharacter/script"
    while check_flag:
        now_time = time.time()
        if now_time - start_time >= 2000:
            check_flag = False
            continue
        zeroport_flag = checkServiceActivate()
        if zeroport_flag:

            try:
                command = [sys.executable, f"{test_path}/main.py", "--run", f"{test_path}/test.json", "--out",
                           f"{test_path}/out.json"]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(timeout=60)
                if process.returncode == 0:
                    with open(f"{test_path}/out.json", 'r', encoding='UTF-8') as f:
                        res = json.load(f)
                        print(res)
                        if res and res.get("result", []) and res.get("result", [])[0] and res.get("result", [])[0].get(
                                "content", {}):
                            images = res.get("result", [])[0].get("content", {}).get("images", [])
                            image = images[0]
                            if "url" in image:
                                check_flag = False
                                server_flag = True
            except Exception as e:
                print(f"Run testcase error: {e}")
    if server_flag is False:
        stopdevice()

def stopdevice():
    # hostname = get_hostname()
    # param = {
    #         "msgtype": "text",
    #         "text": {
    #             "content": f"机器<{hostname}> 重新部署超时失败 "
    #         }
    #     }
    # robot_url = 'https://meet-api.mecord668.com/im/webhook/m1cgmm6mtb8ijpqndo7ct961ur'
    # headers = dict()
    # headers['Content-Type'] = "application/json"
    # co_res = requests.post(robot_url, json.dumps(param), headers=headers, verify=False, timeout=30)
    #
    # token = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjY4NzQ2LCJ1dWlkIjoiYjEwMDQ3NTUtNDVkMy00YjEyLThhODktNjY0NDM5NmE3NDNiIiwiaXNfYWRtaW4iOmZhbHNlLCJpc19zdXBlcl9hZG1pbiI6ZmFsc2UsInN1Yl9uYW1lIjoiIiwidGVuYW50IjoiYXV0b2RsIiwidXBrIjoiIn0.E0MGPAsfFq8eIKz4XoqUqkHe1K4iSTPqVcwjpPJ3oft1xoqVMlc9Y3RshS-pzUKkIhJ7xJrG03hABC3GEt95rw'
    # deviceId = hostname.split('-')[2]
    # headers = {"Authorization": token, "Content-Type": "application/json"}
    # backlist_url = "https://api.autodl.com/api/v1/dev/deployment/blacklist"
    # containerId = hostname.replace('autodl-container-', '')
    # body = {
    #     "deployment_container_uuid": containerId,
    #     "comment": "拉入黑名单"
    # }
    # print(body)
    # response = requests.post(backlist_url, json=body, headers=headers)
    # print(response.content.decode())
    # time.sleep(1)
    #
    #
    # stopdevice_url = "https://api.autodl.com/api/v1/dev/deployment/container/stop"
    # body = {"deployment_container_uuid": deviceId, "decrease_one_replica_num": False, "cmd_before_shutdown": "bash /autodl-fs/data/new_widgets/zz-deploy/imageDeployStop.sh"}
    # print(f"stop body:{body}")
    # response = requests.put(stopdevice_url, json=body, headers=headers)
    # res = response.content.decode()
    # print(f"response:{res}")
    pass

def interrupt_comfyui(taskUUID=""):
    try:
        url = "http://127.0.0.1:6006/interrupt"
        resp = requests.post(url, timeout=1)
        print(f"[{taskUUID}]  =>  interrupt_comfyui: {resp.status_code}")
    except Exception as e:
        print(e)


