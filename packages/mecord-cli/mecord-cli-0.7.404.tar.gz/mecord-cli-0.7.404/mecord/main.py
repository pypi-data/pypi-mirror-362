import sys, os, urllib3, time, platform, json, ast

from mecord import utils
from mecord import mecord_service
from mecord import mecord_widget
from mecord import store
from mecord import utils
from mecord import taskUtils
import psutil

ll = 42
monitor_run = True
mdict = {}
cpu_count = psutil.cpu_count()
thisFileDir = os.path.dirname(os.path.abspath(__file__))
auto_restart = os.path.join(thisFileDir, "auto_restart")
short_flag = os.path.join(thisFileDir, "short_flag")
ex_flag = os.path.join(thisFileDir, "ex_flag")
gpu_flag = os.path.join(thisFileDir, "gpu_flag")
process_timeout = os.path.join(thisFileDir, "process_timeout")
logs_num = os.path.join(thisFileDir, "logs_num")
comfyui_flog = os.path.join(thisFileDir, "comfyui_flog")
proxy_autodl = os.path.join(thisFileDir, "proxy_autodl")
request_limit = os.path.join(thisFileDir, "request_limit")
meco = os.path.join(thisFileDir, "meco")
def scr_str(s):
    return "| " + s + " |"
def scr_str1(s):
    return "| " + s
def scr_line(s):
    return "|" + s + "|"

def service_status(stdscr, idx, flag):
    gpu_flag = os.path.exists(os.path.join(thisFileDir, "gpu_flag"))
    def real_stdsrc(*args):
        if flag:
            print(args[2])
        else:
            stdscr.addstr(*args)
    def running_task_uuids():
        test_lst = []
        us_lst = []
        sg_lst = []
        if flag:
            if os.path.exists(taskUtils.task_config_file):
                with open(taskUtils.task_config_file, 'r') as f:
                    data = json.load(f)
                for it in data:
                    if it not in ["last_task_pts"]:
                        c = data[it]["country"].lower()
                        name = data[it]["name"]
                        if c == "test":
                            test_lst.append(f"{it}[{name}]")
                        elif c == "us":
                            us_lst.append(f"{it}[{name}]")
                        elif c == "sg":
                            sg_lst.append(f"{it}[{name}]")
        else:
            for it in mdict:
                if it != 'main':
                    taskid = mdict[it]["taskid"]
                    c = mdict[it]["country"]
                    name = mdict[it]["name"]
                    more_status = f"{it} {mdict[it]['ZEROPORT']if gpu_flag else mdict[it]['cpu']} {mdict[it]['memory']} {mdict[it]['read']} {mdict[it]['write']}  " if "cpu" in mdict[it] else ""
                    if c == "test":
                        test_lst.append(f"{taskid}[{name}] {more_status}")
                    elif c == "us":
                        us_lst.append(f"{taskid}[{name}] {more_status}")
                    elif c == "sg":
                        sg_lst.append(f"{taskid}[{name}] {more_status}")

        return test_lst, us_lst, sg_lst
    test_lst, us_lst, sg_lst = running_task_uuids()
    d = 0
    # for d in range(0, max([len(test_lst),len(us_lst),len(sg_lst)])):
    def widget_stdscr(this_d, this_task, row_idx, col_idx, append_str):
        if this_d < len(this_task):
            real_s = this_task
            if len(append_str) > 0:
                real_s = f" [{append_str}]" + real_s
            real_stdsrc(row_idx, col_idx, scr_str(real_s.ljust(ll-1)))

    for _lst in test_lst:
        widget_stdscr(d, _lst, idx, 0, "test" if platform.system() == 'Windows' else "")
        idx += 1
    for _lst in sg_lst:
        widget_stdscr(d, _lst, idx, 0, " sg " if platform.system() == 'Windows' else "")
        idx += 1
    return idx

def device_status(stdscr, idx, flag):
    def real_stdsrc(*args):
        if flag:
            print(args[2])
        else:
            stdscr.addstr(*args)
    if flag:
        import psutil
        import GPUtil
        import ping3
        net = psutil.net_io_counters()
        net_up, net_down = net.bytes_sent, net.bytes_recv
        cpu_load = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_load = mem.percent
        _net_up, _net_down = net.bytes_sent, net.bytes_recv
        up_load = (_net_up - net_up) / 1024
        down_load = (_net_down - net_down) / 1024
        try:
            gpu_list = GPUtil.getGPUs()
            if len(gpu_list) > 0:
                gpu_load = gpu_list[0].load * 100  # 只考虑第一块显卡
            else:
                gpu_load = 0
            real_stdsrc(idx, 0, scr_str(f"Device Usage    CPU : {cpu_load}%    Memory : {mem_load}%    GPU : {gpu_load}%    ↑ {up_load}KB/s    ↓ {down_load}KB/s ".ljust(ll*3-4)))
        except:
            real_stdsrc(idx, 0, scr_str(f"Device Usage    CPU : {cpu_load}%    Memory : {mem_load}%    GPU : 获取失败"))
    else:
        try:
            real_stdsrc(idx, 0, scr_str(f"Device Usage    CPU : {mdict['main']['cpu']}%    Memory : {mdict['main']['mem']}%    GPU : {mdict['main']['gpu']}%    ↑ {mdict['main']['up']}    ↓ {mdict['main']['down']}".ljust(ll*3-4)))
        except:
            real_stdsrc(idx, 0, scr_str(f"Device Usage                  CPU : ----                  Memory : ----                  GPU : ----"))
    idx+=1
    return idx

def widget_status(stdscr, idx, flag):
    def real_stdsrc(*args):
        if flag:
            print(args[2])
        else:
            try:
                stdscr.addstr(*args)
            except:
                pass
    real_stdsrc(idx, 0, scr_str("Widget List".ljust(ll*3-2)))
    idx+=1
    widget_map = store.widgetMap()
    if len(widget_map) == 0:
        real_stdsrc(idx, 0, scr_str("empty"))
        idx+=1
        return idx
    maxJust = 10
    for it in widget_map:
        if len(it) > maxJust:
            maxJust = len(it)
    maxJust += 5
    for it in widget_map:
        path = ""
        is_block = False
        isGPU = False
        if isinstance(widget_map[it], (dict)):
            path = widget_map[it]["path"]
            is_block = widget_map[it]["isBlock"]
            isGPU = widget_map[it].get('isGPU', False)
        else:
            path = map[it]
        end_args = ""
        if is_block:
            end_args = " [X]"
        if isGPU:
            end_args += "[H]"
        real_stdsrc(idx, 0, scr_str(f'{f"{it}{end_args}".ljust(maxJust)} {path}'.ljust(ll*3-2)))
        idx+=1
    return idx

def gettitle():
    cooling = False
    cooling_text = ""
    try:
        env_service = ast.literal_eval(store.get_env())
        _env = []
        if '-short' in env_service:
            env_service.remove('-short')
        if '-cooling' in env_service:
            index = env_service.index('-cooling')
            cooling = env_service[index+1]
            cooling_text = f"[线程冷却{cooling}秒]"
            del env_service[index+1]
            del env_service[index]

        else:
            cooling = None
        if 'plus' in env_service:
            env_service.remove('plus')
        if len(env_service) == 0:
            _env = ['sg', 'test']
        else:
            _env = env_service
        env_text = '[{}]'.format(','.join(_env))
    except:
        env_text = ''
    server = "Meco" if os.path.exists(meco) else "Mecord"
    text = f"{server}{'[auto]' if os.path.exists(auto_restart) else ''}{'[short]' if os.path.exists(short_flag) else ''}{cooling_text if cooling else ''}{env_text}".ljust(ll*3-2)
    return text

def status(flag=False):
    from pkg_resources import parse_version, get_distribution
    ver = get_distribution("mecord-cli").version
    deviceid = utils.generate_unique_id()
    import socket
    machine_name = socket.gethostname()
    service = mecord_service.MecordService()
    thread_num = store.get_multithread()
    header_text = gettitle()

    def get_shared_memory_max_counter():
        # 获取系统推荐的共享目录
        system = platform.system()
        if system == 'Windows':
            temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or os.path.expanduser('~\\AppData\\Local\\Temp')
            data_dir = os.path.join(temp_dir, 'widget_shared_memory')
        elif system == 'Darwin':
            cache_dir = os.path.expanduser('~/Library/Caches')
            data_dir = os.path.join(cache_dir, 'widget_shared_memory')
        else:
            data_dir = '/tmp/widget_shared_memory'
        data_file = os.path.join(data_dir, 'widget_power.json')
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('max_counter', None)
        except Exception:
            return None
    shared_max_counter = get_shared_memory_max_counter()
    shared_max_counter_str = ""
    if shared_max_counter and shared_max_counter != thread_num:
        shared_max_counter_str = f"({shared_max_counter} 共享限制)"

    if flag:
        service_is_running = service.is_running()
        print(scr_line("-" * ll*3))
        print(scr_str(header_text))
        print(scr_str(f"版本: {ver}".ljust(ll*3-4)))
        print(scr_str(f"设备号: {deviceid}".ljust(ll*3-5)))
        print(scr_str(f"容器HostName: {machine_name}".ljust(ll*3-4)))
        print(scr_line("-" * ll*3))
        if service_is_running:
            print(scr_str1(f"运行中 ({thread_num} 线程)".ljust(ll*3-2)))
        else:
            print(scr_str1("未运行".ljust(ll*3-2)))
        print(scr_line("-" * ll*3))
        service_status(None, 0, flag)
        print(scr_line("-" * ll*3))
        device_status(None, 0, flag)
        print(scr_line("-" * ll*3))
        widget_status(None, 0, flag)
        print(scr_line("-" * ll*3))
    else:
        import threading
        import curses
        import signal

        def signal_handler(signal_num, frame):
            global monitor_run
            monitor_run = False

        def task_status():
            global monitor_run
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            stdscr.keypad(True)

            tiktak = 0
            while monitor_run:
                try:
                    header_text = gettitle()
                    stdscr.clear()
                    height, width = stdscr.getmaxyx()
                    service_is_running = service.is_running()
                    idx = 0
                    stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    idx += 1
                    stdscr.addstr(idx, 0, scr_str(header_text), )
                    idx += 1
                    stdscr.addstr(idx, 0, scr_str(f"版本: {ver}".ljust(ll * 3 - 4)))
                    idx += 1
                    stdscr.addstr(idx, 0, scr_str(f"设备号: {deviceid}".ljust(ll * 3 - 5)))
                    idx += 1
                    stdscr.addstr(idx, 0, scr_str(f"容器HostName: {machine_name}".ljust(ll * 3 - 4)))
                    idx += 1
                    stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    idx += 1
                    if service_is_running:
                        if tiktak > 3:
                            tiktak = 0
                        stdscr.addstr(idx, 0,
                                      scr_str1("运行中" + "." * tiktak + f" ({thread_num} 线程) {shared_max_counter_str}".ljust(ll * 3 - 2)),
                                      curses.color_pair(1))
                        tiktak += 1
                    else:
                        stdscr.addstr(idx, 0, scr_str1("未运行".ljust(ll * 3 - 2)), curses.color_pair(2))
                    idx += 1
                    stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    idx += 1
                    idx = service_status(stdscr, idx, flag)
                    try:
                        stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    except:
                        pass
                    idx += 1
                    idx = device_status(stdscr, idx, flag)
                    try:
                        stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    except:
                        pass
                    idx += 1
                    idx = widget_status(stdscr, idx, flag)
                    try:
                        stdscr.addstr(idx, 0, scr_line("-" * ll * 3))
                    except:
                        pass
                    stdscr.refresh()
                    time.sleep(1)
                except:
                    # stdscr.addstr(idx, 0, scr_line("-" * ll * 3)) 高度超出会报异常
                    time.sleep(1)
                    pass
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

        def task_monitor():
            import asyncio, GPUtil, ping3
            async def get_usage(pid):
                try:
                    if pid == 'main':
                        network = psutil.net_io_counters()
                        net_up, net_down = network.bytes_sent, network.bytes_recv
                        cpu_usage = f"{psutil.cpu_percent(interval=1):.1f}"
                        mem = psutil.virtual_memory()
                        mem_load = f"{mem.percent:.1f}"
                        network = psutil.net_io_counters()
                        _net_up, _net_down = network.bytes_sent, network.bytes_recv
                        up_num = _net_up - net_up
                        dowm_num = _net_down - net_down
                        up_load = f"{up_num / 1024:.2f}KB/s" if up_num < 1000000 else f"{up_num / 1024 / 1024:.2f}MB/s"
                        down_load = f"{dowm_num / 1024:.2f}KB/s" if dowm_num < 1000000 else f"{dowm_num / 1024 / 1024:.2f}MB/s"
                        try:
                            gpu_list = GPUtil.getGPUs()
                            if len(gpu_list) > 0:
                                gpu_load = f"{gpu_list[0].load * 100:.1f}"  # 只考虑第一块显卡
                            else:
                                gpu_load = 0
                        except:
                            gpu_load = '获取失败'

                        mdict[pid] = {
                            "cpu": cpu_usage,
                            "mem": mem_load,
                            "gpu": gpu_load,
                            'up': up_load,
                            'down': down_load,
                        }
                    else:
                        process = psutil.Process(int(pid))
                        io_counters = process.io_counters()
                        read, write = io_counters.read_bytes, io_counters.write_bytes
                        cpu_usage = f"{process.cpu_percent(interval=1) / cpu_count:.1f}%"
                        memory_info = process.memory_info()
                        memory_usage = f"{memory_info.rss / (1024 ** 2):.2f}MB"
                        io_counters = process.io_counters()
                        read_num = io_counters.read_bytes - read
                        write_num = io_counters.write_bytes - write
                        disk_read = f"{read_num / 1024:.2f}KB/s" if read_num < 1000000 else f"{read_num / 1024 / 1024:.2f}MB/s"
                        disk_write = f"{write_num / 1024:.2f}KB/s" if write_num < 1000000 else f"{write_num / 1024 / 1024:.2f}MB/s"
                        mdict[pid].update({
                            "cpu": cpu_usage,
                            "read": disk_read,
                            "write": disk_write,
                            "memory": memory_usage,
                        })
                except psutil.NoSuchProcess as error:
                    del mdict[pid]
                    # print(error)
                except Exception as e:
                    del mdict[pid]
                    # print(e)

            async def minitor_main():
                global monitor_run
                while monitor_run:
                    if 'main' not in mdict:
                        mdict['main'] = {}
                    if os.path.exists(taskUtils.task_config_file):
                        try:
                            with open(taskUtils.task_config_file, 'r') as f:
                                data = json.load(f)
                        except Exception as e:
                            time.sleep(0.5)
                            continue
                        for it in data:
                            if it not in ["last_task_pts"]:
                                pid = data[it]["pid"]
                                if str(pid) not in mdict:
                                    mdict[str(pid)] = {
                                        'name': data[it]["name"],
                                        'country': data[it]["country"].lower(),
                                        'ZEROPORT': data[it]["ZEROPORT"],
                                        'taskid': it
                                    }
                    tasks = [get_usage(pid) for pid in mdict]
                    await asyncio.gather(*tasks)

            asyncio.run(minitor_main())
        if platform.system() == 'Windows':
            signal.signal(2, signal_handler)
        else:
            signal.signal(2, signal_handler)
            signal.signal(10, signal_handler)

        thread_monitor = threading.Thread(target=task_monitor)
        thread_status = threading.Thread(target=task_status)
        # monitor_run = True
        thread_status.start()
        thread_monitor.start()
        global monitor_run
        try:
            while monitor_run:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor_run = False

        thread_status.join()
        thread_monitor.join()


def service():
    if len(sys.argv) <= 2:
        print('please set command!')
        return

    command = sys.argv[2]
    service = mecord_service.MecordService()
    if command == 'start':
        if os.path.exists(auto_restart):
            os.remove(auto_restart)
        if os.path.exists(ex_flag):
            os.remove(ex_flag)
        if os.path.exists(short_flag):
            os.remove(short_flag)
        if os.path.exists(gpu_flag):
            os.remove(gpu_flag)
        if os.path.exists(process_timeout):
            os.remove(process_timeout)
        if os.path.exists(logs_num):
            os.remove(logs_num)
        if os.path.exists(comfyui_flog):
            os.remove(comfyui_flog)
        if os.path.exists(proxy_autodl):
            os.remove(proxy_autodl)
        if os.path.exists(request_limit):
            os.remove(request_limit)

        if service.is_running():
            print('Service is already running.')
        else:
            print(f'Starting service...[args = {" ".join(sys.argv)}]')
            threadNum = 1
            _threadNum = 1
            cooling = 0
            idx = 2      
            env = []
            while idx < len(sys.argv):
                if sys.argv[idx] == "-thread":
                    threadNum = int(sys.argv[idx+1])
                    if threadNum < 1 or threadNum > 500:
                        print('multi thread number must be 1~500')
                        return
                if sys.argv[idx] in ["product", "us", "usdc", "sg",  "sgdc", "test", "plus", '-short']:
                    env.append(sys.argv[idx])
                if sys.argv[idx] == '-auto':
                    with open(auto_restart, 'w') as f:
                        f.write("")
                if sys.argv[idx] == '-ex':
                    with open(ex_flag, 'w') as f:
                        f.write("")
                if sys.argv[idx] == '-short':
                    with open(short_flag, 'w') as f:
                        f.write("")
                if sys.argv[idx] == '-gpus':
                    with open(gpu_flag, 'w') as f:
                        f.write("")
                if sys.argv[idx] == '-timeout':
                    with open(process_timeout, 'w') as f:
                        f.write(str(sys.argv[idx+1]))
                if sys.argv[idx] == '-logs':
                    with open(logs_num, 'w') as f:
                        f.write(str(sys.argv[idx+1]))
                if sys.argv[idx] == '-comfyui':
                    with open(comfyui_flog, 'w') as f:
                        f.write("")
                if sys.argv[idx] == '-autodl':
                    with open(proxy_autodl, 'w') as f:
                        f.write("")
                if '-h' in sys.argv[idx]:
                    threadNum = int(sys.argv[idx+1])
                if '-l' in sys.argv[idx]:
                    _threadNum = int(sys.argv[idx+1])
                if '-cooling' in sys.argv[idx]:
                    cooling = int(sys.argv[idx+1])
                    env.append(sys.argv[idx])
                    env.append(sys.argv[idx+1])
                if sys.argv[idx] == '-limit':
                    store.save_request_limit(sys.argv[idx+1])
                idx += 1
            service.start(env, threadNum, _threadNum,cooling)
    elif command == 'stop':
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.stop()
    elif command == 'status': 
        status(True)
    elif command == 'restart': 
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.restart()
    else:
        print("Unknown command:", command)

def widget():
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord widget [init|publish]')
        return

    command = sys.argv[2]
    work_path = os.getcwd()
    if len(sys.argv) > 3:
        work_path = sys.argv[3]
    if command == 'init':
        mecord_widget.createWidget(work_path)
    elif command == 'publish':
        mecord_widget.publishWidget(work_path)
    elif command == 'list':
        map = store.widgetMap()
        if len(map) == 0:
            print("local widget is empty")
        maxJust = 20
        for it in map:
            if len(it) > maxJust:
                maxJust = len(it)
        maxJust += 10
        showStatus = ""
        if len(sys.argv) > 3:
            showStatus = sys.argv[3]
        for it in map:
            path = ""
            is_block = False
            if isinstance(map[it], (dict)):
                path = map[it]["path"]
                is_block = map[it]["isBlock"]
            else:
                path = map[it]
            end_args = ""
            if is_block:
                end_args = " [X]"
            ss = f"{it}{end_args}"
            if showStatus in ["disable", "enable"]:
                if is_block and showStatus == "disable":
                    print(f'{ss.ljust(maxJust + 4)} {path}')
                elif is_block == False and showStatus == "enable":
                    print(f'{ss.ljust(maxJust + 4)} {path}')
            else:
                print(f'{ss.ljust(maxJust + 4)} {path}')
    elif command == 'add':
        mecord_widget.addWidgetToEnv(work_path)
    elif command == 'remove':
        mecord_widget.remove(work_path)
    elif command == 'enable':
        mecord_widget.enable(work_path)
    elif command == 'disable':
        mecord_widget.disable(work_path)
    elif command == 'mark':
        mecord_widget.mark(work_path)
    elif command == 'unmark':
        mecord_widget.unmark(work_path)
    elif command == 'pending_task':
        mecord_widget.getTaskCount(work_path)
    elif command == 'install':
        mecord_widget.installWidget(work_path)
    else:
        print("Unknown command:", command)

def monitor():
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord widget [init|publish]')
        return

    command = sys.argv[2]
    if command == 'start':
        utils.runMonitor()
    elif command == 'stop':
        with open('MecordMonitor.pid', 'r') as f:
            pid = f.read()
            os.system("kill -9 " + pid)

def init():
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'meco':
            with open(meco, 'w') as f:
                f.write('')
            print("Init Meco server")
        else: 
            print("Init Mecord server")
            if os.path.exists(meco):
                os.remove(meco)
    else:
        print("Init Mecord server")
        if os.path.exists(meco):
            os.remove(meco)


def main():
    urllib3.disable_warnings()
    if len(sys.argv) >= 2:
        module = sys.argv[1]
        if module == "widget":
            widget()
        elif module == "service":
            service()
        elif module == "status":
            status(True)
        elif module == "report":
            utils.reportLog()
            print(f"report success")
        elif module == "postdata":
            taskUtils.notifyCounterIfNeed('test', is_end=True)
            print(f"postdata success")
        elif module == "monitor":
            monitor()
        elif module == "init":
            init()
        else:
            print(f"Unknown command:{module}")
            sys.exit(0)
    else:
        status(False)

if __name__ == '__main__':
    main()
