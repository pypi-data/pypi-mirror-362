import os
import requests
import datetime
import json
import socket


from requests_toolbelt import MultipartEncoder
from urllib import parse
import base64
import hashlib
from mecord import utils
from pkg_resources import get_distribution
import time
thisFileDir = os.path.dirname(os.path.abspath(__file__))
gpu_flag = os.path.exists(os.path.join(thisFileDir, "gpu_flag"))
machine_name = str(socket.gethostname())
AutoID = os.environ.get('AutoDLDeploymentUUID', '') if machine_name.startswith('autodl') and len(machine_name.split('-')) >= 5 else ""   # AutoDL弹性ID
task_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"task_config.txt")
def taskCountryWithUUID(uuid):
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r') as f:
            data = json.load(f)
        if uuid in data:
            return data[uuid]["country"]
    return None

def taskInfoWithFirstTask():
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r') as f:
            data = json.load(f)
        for it in data:
            if it not in ["last_task_pts"]:
                return it, data[it]["country"]
    return None, None

# WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a771d063-45f9-4926-8543-538595833b74" #大群
WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=46692305-49b8-4428-b47a-b34342fafd7d" #mecord-cli小群
CO_URL = "https://meet-api.mecord668.com/im/webhook/mresrhm3zpb8dfjaehcjebhq5y"  #CO告警
# WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a24496ad-5af6-4c95-a7e4-39cc8e9bb243" #轰炸机
WECHAT_TEST_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dbe0737f-65fa-47ee-84a6-46b191405169" #测试环境
def uploadFile2Wechat(service_country, filepath):
    real_robot_url = WECHAT_URL
    # if service_country == "test":
    #     real_robot_url = WECHAT_TEST_URL
    #     return
    params = parse.parse_qs( parse.urlparse( real_robot_url ).query )
    webHookKey=params['key'][0]
    upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webHookKey}&type=file'
    headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
    filename = os.path.basename(filepath)
    try:
        multipart = MultipartEncoder(
            fields={'filename': filename, 'filelength': '', 'name': 'media', 'media': (filename, open(filepath, 'rb'), 'application/octet-stream')},
            boundary='-------------------------acebdf13572468')
        headers['Content-Type'] = multipart.content_type
        resp = requests.post(upload_url, headers=headers, data=multipart, timeout=300)
        json_res = resp.json()
        if json_res.get('media_id'):
            return json_res.get('media_id')
    except Exception as e:
        return ""
def uploadFile2CO(service_country, filepath,taskUUID):
    real_robot_url = WECHAT_URL
    # if service_country == "test":
    #     real_robot_url = WECHAT_TEST_URL
    #     return
    params = parse.parse_qs( parse.urlparse( real_robot_url ).query )
    webHookKey=params['key'][0]
    upload_url = 'https://meet-api.miyachat.com/general/UploadFile'
    with open(filepath,'rb') as file:
        file_content = file.read()
    base64_encode = base64.b64encode(file_content)
    md5_hash = hashlib.md5(file_content).hexdigest()
    data = {'base64':base64_encode.decode(),
            'md5':md5_hash,
            'robotSecret':'mresrhm3zpb8dfjaehcjebhq5y',
            'webhookToken':'',
            'fileName':taskUUID+".txt",
            }

    try:
        resp = requests.get(upload_url,json=data)
        json_res = resp.json()
        if json_res.get('defaultAccessUrl'):
            return "https://meet-api.miyachat.com"+json_res.get('defaultAccessUrl')
    except Exception as e:
        return ""

def notifyWechatRobot(service_country, param):
    real_robot_url = WECHAT_URL
    # if service_country == "test":
    #     real_robot_url = WECHAT_TEST_URL
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        # res = s.post(real_robot_url, json.dumps(param), headers=headers, verify=False, timeout=30)
        co_res = s.post(CO_URL, json.dumps(param), headers=headers, verify=False, timeout=30)
        s.close()
    except Exception as e:
        print(f"===== qyapi.weixin.qq.com fail ", True)




def MecordWechatRobot(txt, mentioned_list:list):
    device_id = utils.generate_unique_id()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8ecb0952-67fa-4726-a379-d6e6e2b5ab52'
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]{f'[弹性部署ID: {AutoID}]' if AutoID else ''}>\n{txt}"
        }
    }
    if len(mentioned_list) > 0:
        json_data['text']['mentioned_list'] = mentioned_list
    response = requests.post(url, headers=headers, json=json_data)

logs = {}
def taskPrint(taskUUID, msg):
    global logs
    if (taskUUID == None or len(taskUUID) == 0) and msg == None:
        return
    if taskUUID and msg == None:
        try:
            del logs[taskUUID]
        except:
            pass
        return
    if taskUUID and msg:
        if taskUUID not in logs:
            logs[taskUUID] = []
        logs[taskUUID].append(msg)
    if taskUUID == None and msg:
        for uuid in logs:
            logs[uuid].append(msg)
    print(msg)
def getTaskLog(taskUUID):
    if taskUUID in logs:
        return logs[taskUUID]
    return []

def _uploadLog(service_country, taskUUID):
    try:
        log_path = f"{os.path.dirname(os.path.abspath(__file__))}/log_{taskUUID}.log"
        with open(log_path, 'w') as f:
            f.write("\n".join(getTaskLog(taskUUID)))


        notifyWechatRobot(service_country,
                          {
            "msgtype": "markdown",
            "markdown": {
                "content": f"{service_country}任务: {taskUUID} [查看log]({uploadFile2CO(service_country, log_path,taskUUID)})"
            }}

        )
        if os.path.exists(log_path):
            os.remove(log_path)
    except:
        pass

def notifyTaskFail(taskUUID, service_country, reason):
    try:
        real_reason = ""
        if len(reason) > 610:
            real_reason = f"{reason[0:300]}\n...\n{reason[len(reason)-300:]}"
        else:
            real_reason = reason
        try:
            with open(task_config_file, 'r') as f:
                data = json.load(f)
                widget_name = data.get(taskUUID, '').get('name')
        except:
            widget_name = ""
        notifyWechatRobot(service_country, {
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器({machine_name}){f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n执行{service_country}任务{f'[{widget_name}]' if widget_name else ''}[{taskUUID}]失败\n\n{real_reason}"
            }
        })
        _uploadLog(service_country, taskUUID)
    except Exception as e:
        print(F"notifyTaskFail ERROR: {e}")

def notifyServerError(taskUUID, service_country, msg=''):
    try:
        notifyWechatRobot(service_country, {
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器({machine_name}){f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n 执行{service_country}任务[{taskUUID}]上报失败\n{msg}"
            }
        })
        pass
    except:
        pass

def notifyScriptError(taskUUID, service_country):
    try:
        with open(task_config_file, 'r') as f:
            data = json.load(f)
            widget_name = data.get(taskUUID, '').get('name')
    except:
        widget_name = ""
    try:
        notifyWechatRobot(service_country, {
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器({machine_name}){f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n 执行{service_country}{f'[{widget_name}]' if widget_name else ''}任务[{taskUUID}]异常"
            }
        })
        _uploadLog(service_country, taskUUID)
    except:
        pass

def idlingNotify(cnt):
    device_id = utils.generate_unique_id()
    hour = int(float(cnt)/(60.0*60.0))
    if hour<72:
        if hour not in [1, 2, 3, 10, 30, 50, 70]:
            return
    notifyWechatRobot("sg", {
        "msgtype": "text",
        "text": {
            "content": f"机器({machine_name}[{device_id}]){f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n 空转{hour}小时"
        }
    })

def onlineNotify(msg=''):
    device_id = utils.generate_unique_id()
    ver = get_distribution("mecord-cli").version
    notifyWechatRobot("sg", {
        "msgtype": "text",
        "text": {
            "content": f"机器({machine_name}[{device_id}])[{ver}] 上线{msg}{f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n"
        }
    })

def restartNotify(msg):
    device_id = utils.generate_unique_id()
    notifyWechatRobot("sg", {
        "msgtype": "text",
        "text": {
            "content": f"机器({machine_name}[{device_id}]) 即将下线，原因：{msg}{f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n"
        }
    })

def offlineNotify():
    device_id = utils.generate_unique_id()
    ver = get_distribution("mecord-cli").version
    notifyWechatRobot("sg", {
        "msgtype": "text",
        "text": {
            "content": f"机器({machine_name}[{device_id}]) 下线{f'[弹性部署ID: {AutoID}]' if AutoID else ''}\n"
        }
    })

#===================================================== counter ===============================================#
task_counter_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_counter.txt")
from threading import Lock
lock = Lock()
def notifyCounterIfNeed(service_country, is_end=False):
    lock.acquire()
    if gpu_flag:
        for i in range(6000, 6008):
            _task_counter_file = task_counter_file.replace('.txt', f"_{i}.txt")
            try:
                with open(_task_counter_file, 'r') as f:
                    datas = json.load(f)
                    postCounter(datas, extend=f"serverimage_{i}")
            except Exception as e:
                print(e)
    try:
        with open(task_counter_file, 'r') as f:
            datas = json.load(f)
    except:
        with open(task_counter_file, 'w') as f:
            json.dump({}, f)
        return
    finally:
        lock.release()
    try:
        postCounter(datas)
    except:
        pass
    if is_end:
        return
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    data = datas[yesterday]
    s_cnt = 0
    f_cnt = 0
    all_day_usage = 0
    t_l = []
    s_l = []
    f_l = []
    for i in range(0, 24):
        tips = ""
        if str(i) in data:
            s_cnt += data[str(i)]["success"]
            f_cnt += data[str(i)]["fail"]
            s_l.append(data[str(i)]["success"])
            f_l.append(data[str(i)]["fail"])
            if "usage" in data[str(i)]:
                all_day_usage += data[str(i)]["usage"]
                usage_percentage = int((float(data[str(i)]["usage"])/float(60*60))*100)
                tips = f"({usage_percentage}%)"
        else:
            s_cnt += 0
            f_cnt += 0
            s_l.append(0)
            f_l.append(0)
        t_l.append(f"{i}{tips}")
    usage_percentage = int((float(all_day_usage)/float(24*60*60))*100)
    notifyWechatRobot(service_country, {
        "msgtype": "markdown",
        "markdown": {
            "content": f"机器<<font color=\"warning\">{machine_name}</font>> {yesterday} 日报 \n\n\
                            >过去24小时执行任务<<font color=\"warning\">{s_cnt+f_cnt}</font>>个, 负载<<font color=\"warning\">{usage_percentage}%</font>> \n\
                            >成功<font color=\"warning\">{s_cnt}</font>个 \n\
                            >失败<font color=\"warning\">{f_cnt}</font>个"
        }
    })
    import subprocess, platform
    #darwin Command Line cannot create pyplot gui because not application with gui
    if platform.system() != 'Darwin':
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,3))
            plt.rcParams.update({
                'font.size': 7
            })
            plt.bar(t_l, s_l, color='g', label='success')
            plt.bar(t_l, f_l, bottom=s_l, color='r', label='fail')
            plt.title(f'[{machine_name}] [{yesterday}] success/fail={s_cnt}/{f_cnt}')
            plt.xlabel('time')
            plt.xticks(ticks=t_l,rotation=45)
            plt.ylabel('count')
            plt.subplots_adjust(bottom=0.25)
            plt.legend()
            fff = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plt.png")
            plt.savefig(fff)
            with open(fff, "rb") as f:
                encode_string = str(base64.b64encode(f.read()), encoding='utf-8')
            md5 = hashlib.md5()
            md5.update(base64.b64decode(encode_string))
            hash = md5.hexdigest()
            notifyWechatRobot(service_country, {
                "msgtype": "image",
                "image": {
                    "base64": encode_string,
                    "md5": hash
                }
            })
            os.remove(fff)
        except Exception as e:
            print(f"make daily image error: {e}")

def saveCounter(taskUUID, service_country, duration, isSuccess, ZEROPORT='6007'):
    if service_country == "test":
        return
    lock.acquire()
    try:
        if gpu_flag:
            _task_counter_file = task_counter_file.replace('.txt', f"_{ZEROPORT}.txt")
        else:
            _task_counter_file = task_counter_file
        try:
            with open(_task_counter_file, 'r') as f:
                data = json.load(f)
        except:
            data = {}
        #update
        today = datetime.datetime.now()
        now_hour = str(today.hour)
        date = str(today.date())
        if date in data:
            if now_hour in data[date]:
                if isSuccess:
                    data[date][now_hour]["success"] += 1
                else:
                    data[date][now_hour]["fail"] += 1
                if "usage" not in data[date][now_hour]:
                    data[date][now_hour]["usage"] = 0
                data[date][now_hour]["usage"] += duration
            else:
                data[date][now_hour] = {
                    "success" : 1 if isSuccess else 0,
                    "fail" : 0 if isSuccess else 1,
                    "usage" : 0
                }
        else:
            data[date] = {}
            data[date][now_hour] = {
                    "success" : 1 if isSuccess else 0,
                    "fail" : 0 if isSuccess else 1,
                    "usage" : 0
                }

        if len(data) > 14:
            recent_dates = [str((today - datetime.timedelta(days=i)).date()) for i in range(14)]
            _data = {}
            for date in recent_dates:
                if date in data:
                    _data[date] = data[date]
            data = _data
        #save
        with open(_task_counter_file, 'w') as f:
            json.dump(data, f)
    except:
        pass
    finally:
        lock.release()

def postCounter(data:dict, extend=''):
    _host_name = utils.get_hostname()
    host_name = f'{_host_name}_{extend}' if extend else _host_name  # widget_id：391生图扩容标记
    url = 'https://mecord-beta.2tianxin.com/proxymsg/interior_config'
    json_data = {
        "key": host_name,
        "value": json.dumps(data),
    }
    resp = requests.post(url, json=json_data)
    print(resp.text)
    if resp.json()['msg'] == 'success':
        return True
    else:
        return False

def getCounter(device_id=None):
    _device_id = device_id if device_id else utils.generate_unique_id()
    url = 'https://mecord-beta.2tianxin.com/proxymsg/interior_config'
    json_data = {
        "key": _device_id,
        "value": '',  # 空为查询，非空则update
    }
    resp = requests.post(url, json=json_data)
    print(resp.text)
    if resp.json()['msg'] == 'success':
        return json.loads(resp.json()['body']['value'])
    else:
        return False


def recordTime(msg="start", ZEROPORT='6007'):
    if gpu_flag:
        _task_counter_file = task_counter_file.replace('.txt', f"_{ZEROPORT}.txt")
    else:
        _task_counter_file = task_counter_file
    try:
        with open(_task_counter_file, 'r') as f:
            data = json.load(f)
    except:
        data = {}
        return
    now = datetime.datetime.now()
    data[msg] = str(now)
    with open(_task_counter_file, 'w') as f:
        json.dump(data, f)
