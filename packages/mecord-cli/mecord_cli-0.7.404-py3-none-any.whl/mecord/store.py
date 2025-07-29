import os
import json
from threading import Lock
lock = Lock()

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

def updateIfNeed():
    thisDir = os.path.dirname(os.path.abspath(__file__))
    for root,dirs,files in os.walk(thisDir):
        for file in files:
            if "_test.json" in file:
                pname = file.replace("_test", "")
                if os.path.exists(os.path.join(root, pname)):
                    os.remove(os.path.join(root, pname))
                os.rename(os.path.join(root, file), os.path.join(root, pname))
            if os.path.exists(os.path.join(root, "env.txt")):
                os.remove(os.path.join(root, "env.txt"))
        if root != files:
            break

@singleton
class Store(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data.json")
        # update with pengjun
        # remove env , all product env -> test env
        updateIfNeed()
        
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)
                
    def read(self):
        lock.acquire()
        data = {}
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            lock.release()
        except Exception as e:
            lock.release()
            print(f'data.json error:{e}\ntry to init....')
        if len(data) == 0:
            from mecord import utils
            data = {"deviceInfo": utils.deviceInfo()}
            self.write(data)
        return data
    
    def write(self, data):
        lock.acquire()
        with open(self.path, 'w') as f:
            json.dump(data, f)
        lock.release()

def groupUUID():
    sp = Store()
    read_data = sp.read()
    if "groupUUID" in read_data:
        return read_data["groupUUID"]
    else:
        return ""
    
def token():
    sp = Store()
    read_data = sp.read()
    if "token" in read_data:
        return read_data["token"]
    else:
        return ""
    
#============================== widget ================================
def isCreateWidget():
    sp = Store()
    read_data = sp.read()
    if "isCreateWidget" in read_data:
        return read_data["isCreateWidget"]
    else:
        return False
    
def finishCreateWidget():
    sp = Store()
    read_data = sp.read()
    read_data["isCreateWidget"] = False
    sp.write(read_data)

def widgetMap():
    sp = Store()
    read_data = sp.read()
    if "widgets" in read_data:
        return read_data["widgets"]
    else:
        return {}
    
def insertWidget(widget_id, path):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        widgetsMap[widget_id]["path"] = path
    else:
        widgetsMap[widget_id] = {
            "isBlock": False,
            "path" : path
        }
    for k in list(widgetsMap.keys()):
        if isinstance(widgetsMap[k], (dict)):
            if os.path.exists(widgetsMap[k]["path"]) == False:
                del widgetsMap[k]
        else:
            if os.path.exists(widgetsMap[k]) == False:
                del widgetsMap[k]
    sp.write(read_data)

def removeWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        del widgetsMap[widget_id]
    sp.write(read_data)
    
def disableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = True
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": True,
                "path" : path
            }
    sp.write(read_data)

def disableWidgetall():
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    for widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = True
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": True,
                "path" : path
            }
    sp.write(read_data)

def enableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = False
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": False,
                "path" : path
            }
    sp.write(read_data)

def enableWidgetall():
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    for widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = False
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": False,
                "path" : path
            }
    sp.write(read_data)

def markWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isGPU"] = True
        # else:
        #     path = widgetsMap[widget_id]
        #     widgetsMap[widget_id] = {
        #         "isBlock": False,
        #         "path": path,
        #         "isGPU": True
        #     }
    sp.write(read_data)

def unmarkWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isGPU"] = False
        # else:
        #     path = widgetsMap[widget_id]
        #     widgetsMap[widget_id] = {
        #         "isBlock": False,
        #         "path": path,
        #         "isGPU": False
        #     }
    sp.write(read_data)
    
#============================== device id ================================

def writeDeviceInfo(data):
    sp = Store()
    read_data = sp.read()
    read_data["deviceInfo"] = data
    sp.write(read_data)
    
def readDeviceInfo():
    sp = Store()
    read_data = sp.read()
    if "deviceInfo" in read_data:
        return read_data["deviceInfo"]
    else:
        return {}

def is_multithread():
    return get_multithread() > 1

def get_multithread():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multi_thread.config")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            n = int(f.read())
            return n
    except:
        return 1

def save_multithread(n):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multi_thread.config")
    try:
        with open(file, 'w') as f:
            f.write(str(n))
    except:
        pass
    
def get_env():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "env.config")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            return f.read()
    except:
        return ""
    
def save_env(env):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "env.config")
    try:
        with open(file, 'w') as f:
            f.write(str(env))
    except:
        return

def get_request_limit():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "request_limit")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            n = int(f.read())
            return n
    except:
        return get_multithread()

def save_request_limit(n):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "request_limit")
    try:
        with open(file, 'w') as f:
            f.write(str(n))
    except:
        pass
