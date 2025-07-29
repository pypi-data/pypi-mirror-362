import sys, os, time, signal, subprocess, logging, json, platform, socket, calendar
from logging.handlers import RotatingFileHandler
from urllib.parse import *
from datetime import datetime, timedelta
from threading import Thread
from pkg_resources import get_distribution

from mecord import store
from mecord import xy_pb
from mecord import utils
from mecord import taskUtils
from mecord import mecord_widget
from mecord import mecord_server_socket as TaskConnector

thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
pid_file = os.path.join(thisFileDir, "MecordService.pid")
stop_file = os.path.join(thisFileDir, "stop.now")
stop_thread_file = os.path.join(thisFileDir, "stop.thread")
all_thread_stoped = os.path.join(thisFileDir, "all_stoped.now")
waitlastTask = os.path.join(thisFileDir, f"waitlastTask")
remake_sg = os.path.join(thisFileDir, f"remake-sg")
remake_sgdc = os.path.join(thisFileDir, f"remake-sgdc")
remake_us = os.path.join(thisFileDir, f"remake-us")
remake_usdc = os.path.join(thisFileDir, f"remake-usdc")
remake_test = os.path.join(thisFileDir, f"remake-test")
logs_num = os.path.join(thisFileDir, "logs_num")
def notify_other_stoped():
    with open(all_thread_stoped, 'w') as f:
        f.write("")

class LogStdout(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        logFilePath = f"{os.path.dirname(os.path.abspath(__file__))}/log.log"
        if os.path.exists(logs_num):
            try:
                with open(logs_num) as f:
                    num = int(f.read().strip())
            except:
                num = 40
        else:
            num = 40
        file_handler = RotatingFileHandler(logFilePath, maxBytes=1024*1024*20, backupCount=num)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def write(self, message):
        if message != '\n':
            self.logger.info(message)
        self.stdout.write(message)

    def flush(self):
        self.stdout.flush()

    def __del__(self):
        self.close()

    def close(self):
        sys.stdout = self.stdout

class MecordService:
    def __init__(self):
        self.THEADING_LIST = []

    def signal_handler(self, signal_num, frame):
        print('接收到信号:', signal_num)

        print("prepare stop")
        with open(waitlastTask, 'w') as f:
            f.write("")
        with open(stop_thread_file, 'w') as f:
            f.write("")
        for t in self.THEADING_LIST:
            t.markStop()
        for t in self.THEADING_LIST:
            t.join()
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        # 4: clean
        if os.path.exists(stop_thread_file):
            os.remove(stop_thread_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        taskUtils.offlineNotify()
        TaskConnector._clearTask()
        taskUtils.recordTime('close')
        print("MecordService has ended!")
        sys.stdout.close()
        sys.exit()



    def start(self, env, threadNum=1, _threadNum=1,cooling=0):
        taskUtils.recordTime('start')
        high_threadNum = 1
        low_threadNum = 1
        if 'plus' in env:
            high_threadNum = threadNum
            low_threadNum = _threadNum

        if platform.system() == 'Windows':
            # 监听信号
            signal.signal(2, self.signal_handler)
            # signal.signal(signal.SIGINT, self.signal_handler)
        else:
            signal.signal(2, self.signal_handler)
            signal.signal(10, self.signal_handler)
            # signal.signal(signal.SIGUSR1, self.signal_handler)

        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    taskUtils.notifyWechatRobot("us", {
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        #1: service init
        sys.stdout = LogStdout()
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, self.stop)
        if 'plus' in env:
            store.save_multithread(high_threadNum+low_threadNum)
        else:
            store.save_multithread(threadNum)
        store.save_env(env)
        store.writeDeviceInfo(utils.deviceInfo())
        TaskConnector._clearTask()
        #2: service step
        if 'plus' in env:
            executor = TaskConnector.MecordTaskExecutorThread('plus', high_threadNum, low_threadNum)
        else:
            executor = TaskConnector.MecordTaskExecutorThread(cooling=cooling)
        self.THEADING_LIST.append(executor)
        use_env = []
        if "sg" in env:
            use_env.append("sg")
        elif "sgdc" in env:
            use_env.append("sgdc")
        elif "usdc" in env:
            use_env.append("usdc")
        elif "us" in env:
            # use_env.append("us")
            use_env.append("sg")
        elif "product" in env:
            # use_env.append("us")
            use_env.append("sg")
        elif "test" in env:
            use_env.append("test")
        else:
            # use_env.append("us")
            use_env.append("sg")
            use_env.append("test")

        # use_connnect = False if '-short' in env else TaskConnector.can_use_longconnect()
        use_connnect = False if '-short' in env else True
        if 'plus' in env:
            for e in use_env:
                if use_connnect == False:
                    self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(e, executor, '-h'))
                    self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(e, executor, '-l'))
                else:
                    self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(e, executor, '-h'))
                    self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(e, executor, '-l'))
        else:
            for e in use_env:
                if use_connnect == False:
                    self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(e, executor,cooling=cooling))
                else:
                    self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(e, executor))
        self.THEADING_LIST.append(MecordStateThread())
        self.THEADING_LIST.append(MecordPackageThread())
        now = datetime.now()
        next_day = now.replace(hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
        count = 0
        _count = 0
        flag = False

        os.remove(remake_sg) if os.path.exists(remake_sg) else None
        os.remove(remake_sgdc) if os.path.exists(remake_sgdc) else None
        os.remove(remake_us) if os.path.exists(remake_us) else None
        os.remove(remake_usdc) if os.path.exists(remake_usdc) else None
        os.remove(remake_test) if os.path.exists(remake_test) else None

        #3: service step
        while (os.path.exists(stop_file) == False):
            if os.path.exists(remake_sg):
                self.remakeThread(use_connnect, 'sg', 'sg', env, executor)
                os.remove(remake_sg)

            if os.path.exists(remake_us):
                _count = 0
                flag = not flag
                self.remakeThread(use_connnect, 'us', 'usdc', env, executor)
                os.remove(remake_us)

            if os.path.exists(remake_usdc):
                _count = 0
                flag = not flag
                self.remakeThread(use_connnect, 'usdc', 'us', env, executor)
                os.remove(remake_usdc)

            if os.path.exists(remake_test):
                self.remakeThread(use_connnect, 'test', 'test', env, executor)
                os.remove(remake_test)

            if (datetime.now() - next_day).total_seconds() > 0:
                taskUtils.notifyCounterIfNeed('test')
                next_day += timedelta(days=1)
                print(f'======= publish daily report =======')
            time.sleep(5)
            count += 1
            if (count % 720) == 0:
                taskUtils.notifyCounterIfNeed('test', is_end=True)
                count = 1
            if flag:
                _count += 1
            if flag and _count >= 360:
                with open(remake_us, 'w') as f:
                    f.write('')


        print("prepare stop")
        with open(stop_thread_file, 'w') as f:
            f.write("")
        for t in self.THEADING_LIST:
            t.markStop()
        for t in self.THEADING_LIST:
            t.join()
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        #4: clean
        if os.path.exists(stop_thread_file):
            os.remove(stop_thread_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        taskUtils.offlineNotify()
        TaskConnector._clearTask()
        taskUtils.recordTime('close')
        print("MecordService has ended!")
        utils.check_restart()
        sys.stdout.close()

    def remakeThread(self, use_connnect, country, server_country, env, executor):
        for t in self.THEADING_LIST[::-1]:
            if f'-{country}' in t.name:
                t.remake()
                i = 0
                while t.ws and i < 20:
                    i += 1
                    time.sleep(1)
                self.THEADING_LIST.remove(t)
        if 'plus' in env:
            if use_connnect == False:
                self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(server_country, executor, '-l'))
                self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(server_country, executor, '-h'))
            else:
                self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(server_country, executor, '-l'))
                self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(server_country, executor, '-h'))
        else:
            if use_connnect == False:
                self.THEADING_LIST.append(TaskConnector.MecordShortConnectThread(server_country, executor))
            else:
                self.THEADING_LIST.append(TaskConnector.MecordLongConnectThread(server_country, executor))


    def is_running(self):
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
        
    def stop(self, signum=None, frame=None):
        with open(waitlastTask, 'w') as f:
            f.write("")
        with open(stop_file, 'w') as f:
            f.write("")
        print("MecordService waiting stop...")
        taskUtils.restartNotify("手动")
        while os.path.exists(stop_file):
            time.sleep(1)
        print("MecordService has ended!")
        
    def restart(self):
        utils.begin_restart("手动重启", False, "https://pypi.python.org/simple/")
    
class MecordPackageThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"MecordPackageThread"
        if platform.system() == 'Windows':
            self.time_task_file = os.path.join(thisFileDir, "update_mecord.bat")
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.time_task_file = os.path.join(thisFileDir, "update_mecord.sh")
        if os.path.exists(self.time_task_file):
            os.remove(self.time_task_file)
        self.last_check_time = calendar.timegm(time.gmtime())
        self.is_running = True
        self.start()
    def getCommandResult(self, cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    def run(self):
        while (os.path.exists(stop_thread_file) == False):
            i = 0
            while self.is_running and 60 > i:
                time.sleep(1)
                i += 1
            if self.is_running is False:
                break
            if calendar.timegm(time.gmtime()) - self.last_check_time > 300:
                self.last_check_time = calendar.timegm(time.gmtime())
                try:
                    #update widget
                    mecord_widget.UpdateWidgetFromPypi()
                except Exception as ex:
                    print(f'update widget fail, {ex}')

                try:
                    #update cli
                    remote_config = json.loads(xy_pb.GetSystemConfig(xy_pb.supportCountrys()[0], "mecord_cli_version"))
                    remote_version = remote_config["ver"]
                    simple = "https://pypi.python.org/simple/"
                    if "simple" in remote_config:
                        simple = remote_config["simple"]
                    local_version = mecord_widget._local_package_version("mecord-cli")
                    if len(local_version) > 0 and len(remote_version) > 0 and mecord_widget.compare_versions(remote_version, local_version) > 0:
                        print("start update progress...")
                        utils.begin_restart("auto upgrade mecord-cli", True, simple)
                        device_id = utils.generate_unique_id()
                        machine_name = socket.gethostname()
                        ver = get_distribution("mecord-cli").version
                        taskUtils.notifyWechatRobot("us", {
                            "msgtype": "text",
                            "text": {
                                "content": f"机器<{machine_name}[{device_id}]>[{ver}] mecord-cli开始升级[{local_version}]->[{remote_version}]"
                            }
                        })
                        break
                except Exception as ex:
                    print(f'update mecord-cli fail, {ex}')
        print(f"   PackageChecker stop")
        notify_other_stoped() #because other thread is waiting some signal to close
    def markStop(self):
        print(f"   PackageChecker waiting stop")
        self.is_running = False

class MecordStateThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"MecordStateThread"
        self.daemon = True
        self.tik_time = 30.0
        self.is_running = True
        self.start()
    def run(self):
        taskUtils.onlineNotify()
        while (os.path.exists(stop_thread_file) == False):
            i = 0
            while self.is_running and self.tik_time > i:
                time.sleep(1)
                i += 1
            if self.is_running is False:
                break
            try:
                task_config = TaskConnector._getTaskConfig()
                if task_config["last_task_pts"] > 0:
                    cnt = (calendar.timegm(time.gmtime()) - task_config["last_task_pts"]) #second
                    if cnt >= (60*60) and cnt/(60*60)%1 <= self.tik_time/3600:
                        taskUtils.idlingNotify(cnt)
                        #clear trush
                        for root,dirs,files in os.walk(thisFileDir):
                            for file in files:
                                if file.find(".") <= 0:
                                    continue
                                ext = file[file.rindex("."):]
                                if ext in [ ".in", ".out" ]:
                                    os.remove(os.path.join(thisFileDir, file))
                            if root != files:
                                break
            except:
                i = 0
                while self.is_running and 60 > i:
                    time.sleep(1)
                    i += 1
        print(f"   StateChecker stop")
    def markStop(self):
        print(f"   StateChecker waiting stop")
        self.is_running = False
