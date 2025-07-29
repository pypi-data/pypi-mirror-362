from mecord import store
import time, json
import threading
import calendar
from threading import Thread, current_thread
import websocket
import uuid
import queue
from mecord import xy_pb
from mecord import constant
from mecord import utils
from mecord import taskUtils
import mecord.pb.tarsproxy_pb2 as tarsproxy_pb2

class MecordAIGCTaskThread(Thread):
    params = False
    idx = 0
    call_back = None
    def __init__(self, idx, country, func, func_id, params, callback, user_id, parentTaskId=0, timeout=600, isCancelRetry=False):
        super().__init__()
        self.idx = idx
        self.country = country
        self.func = func
        self.widgetid = func_id
        self.params = params
        self.call_back = callback
        self.user_id = user_id
        self.parentTaskId = parentTaskId
        self.timeout = timeout if timeout > 3 else 6
        self.start_time = time.time()
        self.isCancelRetry = isCancelRetry    # 是否取消重试：true就不会重试,false会重试
        if self.call_back == None:
            raise Exception("need callback function")
        self.start()
    def run(self):
        self.checking = False
        self.result = False, "Unknow"
        if self.widgetid == None:
            self.widgetid = xy_pb.findWidget(self.country, self.func)
        if self.widgetid > 0:
            checkUUID = xy_pb.createTask(self.country, self.widgetid, self.params, self.user_id, self.parentTaskId)
            print(f"checkUUID: {checkUUID}")
            checking = True
            checkCount = 0
            while checking:
                now_time = time.time()
                if now_time - self.start_time >= self.timeout:
                    break
                finish, success, data = xy_pb.checkTask(self.country, checkUUID)
                if finish:
                    checking = False
                    if success:
                        self.call_back(self.idx, data)
                        return
                checkCount += 1
                time.sleep(0.1)
            if checking and self.isCancelRetry:
                print(f'Timeout checking: {checkUUID}')
                xy_pb.TaskNotify(self.country, checkUUID, False, '超时失败并取消重试', json.dumps({"parentTaskId": self.parentTaskId, "msg": "超时失败并取消重试"}), failSaveNotify=False, isCancelRetry=self.isCancelRetry)
        else:
            print(f"widget {self.func}-{self.widgetid} not found with {self.country}")
        self.call_back(self.idx, None)

class MecordAIGCTask:
    import urllib3
    thread_data = {}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def __init__(self, func: str, multi_params, fromUUID=None, func_id=None, _country='test', user_id=1, parentTaskId=0, timeout=600, isCancelRetry=False):
        realTaskUUID = fromUUID
        country = ""
        self.thread_data = {}
        if not _country.startswith('_'):
            if store.is_multithread() or realTaskUUID != None:
                country = taskUtils.taskCountryWithUUID(realTaskUUID)
            else:
                firstTaskUUID, country = taskUtils.taskInfoWithFirstTask()
                if realTaskUUID == None:
                    realTaskUUID = firstTaskUUID
            if country == None:
                country = _country
        else:
            country = _country[1:]

        def _callback(idx, data):
            self.thread_data[str(idx)]["result"] = data
        idx = 0
        for param in multi_params:
            param["fromUUID"] = realTaskUUID
            self.thread_data[str(idx)] = {
                "thread" :  MecordAIGCTaskThread(idx, country, func, func_id, param, _callback, user_id, parentTaskId, timeout, isCancelRetry),
                "result" : None
            }
            idx+=1
        
    def syncCall(self):
        for t in self.thread_data.keys():
            self.thread_data[t]["thread"].join()
        result = []
        for t in self.thread_data.keys():
            result.append(self.thread_data[t]["result"])
        return result
    
class TTSFunc(MecordAIGCTask):
    all_text = []
    def __init__(self, text: str = None, roles = [], fromUUID = None, multi_text = []):
        if text != None:
            self.all_text = [text] + multi_text
        else:
            self.all_text = multi_text
        params = []
        for t in self.all_text:
            params.append({
                "mode": 0,
                "param":{
                    "messages": [
                        {
                            "content": t,
                            "roles": roles,
                        }
                    ],
                    "task_types": [
                        "generate_tts"
                    ]
                }
            })
        super().__init__("TaskTTS", params, fromUUID)

    def syncCall(self):
        return self.singleSyncCall()
        
    def singleSyncCall(self):
        datas = super().syncCall()
        try:
            tts_url = datas[0][0]["content"]["tts_results"][0]["tts_mp3"]
            tts_duration = datas[0][0]["content"]["tts_results"][0]["duration"]
            return tts_duration, tts_url
        except:
            return 0, None
        
    def multiSyncCall(self):
        datas = super().syncCall()
        result = []
        try:
            idx = 0
            for t in self.all_text:
                if idx < len(datas):
                    tts_url = datas[idx][0]["content"]["tts_results"][0]["tts_mp3"]
                    tts_duration = datas[idx][0]["content"]["tts_results"][0]["duration"]
                    result.append({
                        "duration": tts_duration,
                        "url": tts_url,
                    })
                else:
                    result.append({
                        "duration": 0,
                        "url": "",
                    })
                idx += 1
        except:
            pass
        return result
       
class Txt2ImgFunc(MecordAIGCTask):
    all_text = []
    def __init__(self, text: str = None, roles = [], fromUUID = None, multi_text = []):
        if text != None:
            self.all_text = [text] + multi_text
        else:
            self.all_text = multi_text
        params = []
        for t in self.all_text:
            params.append({
                "mode": 0,
                "param":{
                    "messages": [
                        {
                            "content": t,
                            "content_summary": t,
                            "is_content_finish": True,
                            "message_type": "normal",
                            "roles": roles,
                        }
                    ],
                    "task_types": [
                        "generate_chapter_image"
                    ]
                }
            })
        super().__init__("TaskChapterImage", params, fromUUID)

    def syncCall(self):
        return self.singleSyncCall()
        
    def singleSyncCall(self):
        datas = super().syncCall()
        try:
            return datas[0][0]["content"]["chapter_image_urls"][0]
        except:
            return None
        
    def multiSyncCall(self):
        datas = super().syncCall()
        result = []
        try:
            idx = 0
            for t in self.all_text:
                if idx < len(datas):
                    result.append({
                        "url": datas[idx][0]["content"]["chapter_image_urls"][0],
                    })
                else:
                    result.append({
                        "url": "",
                    })
                idx += 1
        except:
            pass
        return result
     
class Audio2TextFunc(MecordAIGCTask):
    all_url = []
    def __init__(self, mp3Urls = [], fromUUID = None):
        self.all_url = mp3Urls
        params = []
        for t in self.all_url:
            params.append({
                "mode": 0,
                "param":{
                    "model":"large",
                    "audio": t
                }
            })
        super().__init__("SpeechToText", params, fromUUID)

    def syncCall(self):
        return self.singleSyncCall()
        
    def singleSyncCall(self):
        datas = super().syncCall()
        try:
            return datas[0][0]["content"]["chapter_image_urls"][0]
        except:
            return None
        
    def multiSyncCall(self):
        datas = super().syncCall()
        result = []
        try:
            idx = 0
            for t in self.all_url:
                if idx < len(datas):
                    result.append({
                        "text": datas[idx][0]["content"][0],
                        "lyric": datas[idx][0]["lyric"],
                        "language": datas[idx][0]["language"]
                    })
                else:
                    result.append({
                        "text": "",
                        "lyric": [],
                        "language": ""
                    })
                idx += 1
        except:
            pass
        return result
    
class MecordLongConnectServer(Thread):


    def get_url(self, country):
        return {
            "test": "wss://mecord-beta.2tianxin.com/proxymsg/ws",
            "us": "wss://api.mecordai.com/proxymsg/ws",
            "sg": "wss://api-inner.mecordai.com/proxymsg/ws" if 'autodl' in utils.get_hostname() else "wss://api-sg-gl.mecordai.com/proxymsg/ws",
        }[country]
    ws = None
    extend_config = {}
    token = ""
    device_id = ""
    service_country = "test"
    # THEADING_LIST = []
    THEADING_DICT = {}
    is_running = False
    last_get_task_begin = 0
    last_get_task_end = 0
    reconnect_cnt = 0


    def receive_unknow_func(self, body):
        pass
    def receive_GetTask(self, body, country):
        if len(body) == 0:
            return
        rsp = xy_pb.aigc_ext_pb2.GetTaskRes()
        rsp.ParseFromString(body)
        get_task_time = int(time.time()*1000)
        datas = []
        if len(rsp.list) > 0:
            self.last_get_task_end = calendar.timegm(time.gmtime())
            self.task_list = []
            for it in rsp.list:
                self.task_list.append(it.taskUUID)
                datas.append({
                    "taskUUID": it.taskUUID,
                    "pending_count": rsp.count - rsp.limit,
                    "config": it.config,
                    "data": it.data,
                })
            self.get_task_data_tem[country] = {'datas': datas, 'timeout': rsp.timeout, 'get_time': self.last_get_task_end, 'task_list': self.task_list}
            if self.get_task_data == {} and self.get_task_wait[country]:
                print(f'{self.name}-{country} === get {len(rsp.list)} task, tasklist: {self.task_list} -t {get_task_time}')
                self.get_task_data = {country: datas}
                self.get_task_timeout = {country: rsp.timeout}
                self.get_task_wait[country] = False
            else:
                print(f"{self.name}-{country} *** TaskReject: {str(self.task_list)}")


    def receive_TaskNotify(self, body, country):
        if len(body) == 0:
            self.notify_task = False
            self.notify_task_wait = False
            return
        rsp = xy_pb.aigc_ext_pb2.TaskNotifyRes()
        rsp.ParseFromString(body)

        print(f'{self.name} === task {rsp.task_uuid} notify={rsp.ok}')
        if self.notify_task_uuid == rsp.task_uuid:
            self.notify_task = rsp.ok
            self.notify_task_wait = False


    def receive_TaskInfo(self, body, country):
        if len(body) == 0:
            self.check_task = False
            self.check_task_wait = False
            return
        rsp = xy_pb.aigc_ext_pb2.TaskInfoRes()
        rsp.ParseFromString(body)

        if self.check_task_uuid == rsp.taskUUID:
            self.check_task = True
        else:
            self.check_task = False
        self.check_task_wait = False


    def on_message(self, ws, message):
        country = ws.header['country']
        try:
            msg = tarsproxy_pb2.Message()
            msg.ParseFromString(message)
            cases = {
                "mecord.aigc.AigcExtObj_GetTask": self.receive_GetTask,
                "mecord.aigc.AigcExtObj_TaskNotify": self.receive_TaskNotify,
                "mecord.aigc.AigcExtObj_TaskInfo": self.receive_TaskInfo,
            }
            return cases.get(f"{msg.obj}_{msg.func}", self.receive_unknow_func)(msg.body, country)
        except Exception as ex:
            # print(f'on_message() === error: {ex}')
            pass
    def on_error(self, ws, error):
        country = ws.header['country']
        print(f"{self.name}-{country} === Connection on_error (error: {error})")
        if 'Handshake status 400 Bad Request' in str(error) and self.reconnect_cnt >= 10:
            self.is_accelerate = False
        if "Connection to remote host was lost" in str(error):
            # print(f"close socket & sleep(2)")
            print(f"close socket.....")
        if self.is_reconnect is False:
            self.socket_close(country)

    def on_close(self, ws, status_code, close_msg):
        country = ws.header['country']
        if self.is_reconnect is False:
            self.socket_close(country)
        print(f"{self.name}-{country} === Connection closed (status code: {status_code}, message: {close_msg})")
        # if self.is_running:
        #     self.reconnect(country)
    def on_ping(self, ws, country, message):
        # print(f"MecordLongConnectServer-{ws.header['country']} === on_ping... {message}")
        try:
            if country == 'test':
                self.ws_test.send(message, websocket.ABNF.OPCODE_PING)
            if country == 'sg':
                self.ws_sg.send(message, websocket.ABNF.OPCODE_PING)
        except Exception as e:
            print(f'{self.name}-{country} on_ping Error: {e}')
            self.reconnect(country)


    def on_pong(self, ws, message):
        country = ws.header['country']
        print(f"MecordLongConnectServer-{country} === on_pong... {message}")
        if country == 'sg':
            self.reconnect_cnt_sg = 0
        else:
            self.reconnect_cnt_test = 0
        # pass


    def send_ping(self):
        self.ping_time = time.time()


    def on_open(self, ws):
        # self.GetTask()
        self.reconnect_cnt=0

    def __init__(self):
        threading.Thread.__init__(self)
        self.task_queue = queue.Queue()
        self.name = f"MecordLongConnectServer"
        extInfo = {}
        extInfo["version"] = constant.app_version
        # extInfo["device_id"] = utils.generate_unique_id()
        extInfo["device_id"] = ''.join(str(uuid.uuid4()).split('-'))
        extInfo["host_name"] = utils.get_hostname()
        self.extend_config = extInfo
        self.token = {'sg': xy_pb.real_token('sg'), 'test': xy_pb.real_token('test')}
        self.is_running = True
        self.is_reconnect = False
        # self.THEADING_DICT = {'test': '', 'sg': '', 'heartbeat': '',}
        self.THEADING_DICT = {}
        self.get_task_data_tem = {'test': {}, 'sg': ''}
        self.task_list = []
        self.last_get_task_begin = 0
        self.last_get_task_end = 0
        self.reconnect_cnt_sg = 0
        self.reconnect_cnt_test = 0
        self.latency = ''
        self.is_accelerate = True
        self.check_task = False
        self.check_task_wait = False
        self.check_task_uuid = 'uuid'
        self.get_task_wait = {'sg': False, 'test': False}
        self.get_task_data, self.get_task_timeout = {}, {}
        self.notify_task = False
        self.notify_task_uuid = 'uuid'
        self.notify_task_wait = False
        self.socket_init()
        self.start()

    def socket_init(self):
        self.ws_test = websocket.WebSocketApp(url=self.get_url('test'),
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_ping=self.on_ping,
                                    on_pong=self.on_pong,
                                    header={
                                        'deviceid':self.extend_config['device_id'],
                                        'country': 'test'
                                    })
        self.ws_sg = websocket.WebSocketApp(url=self.get_url('sg'),
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_ping=self.on_ping,
                                    on_pong=self.on_pong,
                                    header={
                                        'deviceid':self.extend_config['device_id'],
                                        'country': 'sg'
                                    })


    def reconnect(self, country):
        if country == 'sg':
            print(f'{self.name}-{country} === reconnect {self.reconnect_cnt_sg}/60...')
            self.reconnect_cnt_sg+=1
            self.ws_sg = websocket.WebSocketApp(url=self.get_url('sg'),
                            on_message=self.on_message,
                            on_error=self.on_error,
                            on_close=self.on_close,
                            on_ping=self.on_ping,
                            on_pong=self.on_pong,
                            header={
                                'deviceid':self.extend_config['device_id'],
                                'country': 'sg'
                            })

            self.THEADING_DICT['sg'] = threading.Thread(target=self.ws_sg.run_forever)
            self.THEADING_DICT['sg'].start()
            print(f'{self.name}-sg === restart...ok')

        if country == 'test':
            print(f'{self.name}-{country} === reconnect {self.reconnect_cnt_test}/60...')
            self.reconnect_cnt_test+=1
            self.ws_test = websocket.WebSocketApp(url=self.get_url('test'),
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_ping=self.on_ping,
                on_pong=self.on_pong,
                header={
                    'deviceid':self.extend_config['device_id'],
                    'country': 'test'
                })

            self.THEADING_DICT['test'] = threading.Thread(target=self.ws_test.run_forever)
            self.THEADING_DICT['test'].start()
            print(f'{self.name}-test === restart...ok')
        self.is_reconnect = False


    def send_byte(self, b, country):
        try:
            if country == 'sg':
                self.ws_sg.send_bytes(b)
            else:
                self.ws_test.send_bytes(b)
            return True
        except Exception as e:
            print(f'{self.name}-{country} === send_byte() error: {e}')
            return False


    def socket_close(self, country):
        self.is_reconnect = True
        if country == 'sg' and self.ws_sg:
            self.ws_sg.close()
            self.ws_sg = None
        if country == 'test' and self.ws_test:
            self.ws_test.close()
            self.ws_test = None

    def socket_bypass(self):
        time.sleep(2)
        while self.is_running:
            self.on_ping(self.ws_test, 'test', 'heartbeat')
            self.on_ping(self.ws_sg, 'sg', 'heartbeat')
            time.sleep(1)
        print(f"   {current_thread().name} heartbeat stop")

    def _pb_pack(self, func, req, country):
        opt = {
            "lang": "zh-Hans",
            "region": "CN",
            "appid": "80",
            "application": "mecord",
            "version": "1.0",
            "X-Token": self.token[country],
            "uid": "1",
        }
        input_req = xy_pb.rpcinput_pb2.RPCInput(obj="mecord.aigc.AigcExtObj", func=func, req=(req.SerializeToString() if req else None), opt=opt)
        return input_req.SerializeToString()


    def GetTask(self, country, widget_ids='', limit=1, keep_alive=False, reqid=None, timeout=3):
        if self.get_task_data:
            if country == list(self.get_task_data.keys())[0]:
                data, task_outime = self.get_task_data[country], self.get_task_timeout[country]
                self.get_task_data, self.get_task_timeout = {}, {}
                return data, task_outime
            else:
                return [], 10
        self.get_task_wait[country] = True
        req = xy_pb.aigc_ext_pb2.GetTaskReq()
        req.limit = limit
        req.version = xy_pb.constant.app_version
        req.DeviceKey = self.extend_config["device_id"]
        for widget in widget_ids:
            req.widgets.append(widget)
        req.token = xy_pb.real_token(country)
        self.extend_config["trace_id"] = reqid if reqid else ''.join(str(uuid.uuid4()).split('-'))
        req.extend = json.dumps(self.extend_config)
        req.apply = True
        self.last_get_task_begin = calendar.timegm(time.gmtime())
        send_byte_time = int(time.time()*1000)
        if keep_alive and self.get_task_data_tem[country] and ((self.last_get_task_begin - self.get_task_data_tem[country]['get_time']) < 5):
            data, task_outime, task_list = self.get_task_data_tem[country]['datas'], self.get_task_data_tem[country]['timeout'], self.get_task_data_tem[country]['task_list']
            self.get_task_data_tem[country] = {}
            self.TaskReply(country, task_list)
            print(f'{self.name}-{country} === get {len(task_list)} task, tasklist: {task_list} -t {send_byte_time}')
            return data, task_outime
        self.send_byte(self._pb_pack("GetTask", req, country), country)
        print(f'{self.name}-{country} === waiting {req.limit} task, widgets: {req.widgets} -t {send_byte_time} trace_id: {self.extend_config["trace_id"]}')
        num = 0
        while self.get_task_wait[country] and num < timeout:
            num += 0.01
            time.sleep(0.01)
        self.get_task_wait[country] = False
        self.GetNoneTask(country)
        try:
            data, task_outime = self.get_task_data[country], self.get_task_timeout[country]
            self.TaskReply(country, self.task_list)
            self.task_list = []
            self.get_task_data, self.get_task_timeout = {}, {}
        except:
            data, task_outime = [], 10
        return data, task_outime


    def GetNoneTask(self, country):
        req = xy_pb.aigc_ext_pb2.GetTaskReq()
        req.limit = 0
        req.version = xy_pb.constant.app_version
        req.DeviceKey = self.extend_config["device_id"]
        req.widgets.append('NoWidget')
        req.token = xy_pb.real_token(country)
        self.extend_config["trace_id"] = ''.join(str(uuid.uuid4()).split('-'))
        req.extend = json.dumps(self.extend_config)
        req.apply = True
        self.last_get_task_begin = calendar.timegm(time.gmtime())
        self.send_byte(self._pb_pack("GetTask", req, country), country)



    def TaskReply(self, country, tasklist):
        task_item = xy_pb.aigc_ext_pb2.TaskItem()
        req = xy_pb.aigc_ext_pb2.TaskReplyReq()
        for task in tasklist:
            task_item.taskUUID = task
            req.list.append(task_item)
        send_flag = self.send_byte(self._pb_pack("TaskReply", req, country), country)
        if send_flag is False:
            time.sleep(2)
            self.send_byte(self._pb_pack("TaskReply", req, country), country)

    def TaskInfo(self, country, taskUUID):
        req = xy_pb.aigc_ext_pb2.TaskInfoReq()
        req.taskUUID = taskUUID
        req.findTaskResult = False
        req.findWidgetData = False
        send_flag = self.send_byte(self._pb_pack("TaskInfo", req, country), country)
        if send_flag is False:
            time.sleep(2)
            self.send_byte(self._pb_pack("TaskInfo", req, country), country)

    def TaskNotify(self, country, taskUUID, status, msg, dataStr, failSaveNotify=True, keep_alive=False, timeout=3):
        self.notify_task_uuid = taskUUID
        req = xy_pb.aigc_ext_pb2.TaskNotifyReq()
        req.version = constant.app_version
        req.taskUUID = taskUUID
        if status:
            req.taskStatus = xy_pb.common_ext_pb2.TaskStatus.TS_Success
        else:
            req.taskStatus = xy_pb.common_ext_pb2.TaskStatus.TS_Failure
        req.failReason = msg
        req.data = dataStr
        self.extend_config["trace_id"] = ''.join(str(uuid.uuid4()).split('-'))
        req.extend = json.dumps(self.extend_config)
        # taskUtils.taskPrint(taskUUID, f"{self.name} === notify {country} task : {taskUUID}")
        print(f"{self.name} === notify {country} task : {taskUUID}")

        self.notify_task_wait = True
        send_flag = self.send_byte(self._pb_pack("TaskNotify", req, country), country)
        if send_flag is False:
            time.sleep(2)
            self.send_byte(self._pb_pack("TaskNotify", req, country), country)
        num = 0
        while self.notify_task_wait and num < timeout:
            num += 0.01
            time.sleep(0.01)
        if self.notify_task_wait:
            return False
        else:
            return self.notify_task


    def run(self):
        self.THEADING_DICT['sg'] = threading.Thread(target=self.ws_sg.run_forever)
        self.THEADING_DICT['test'] = threading.Thread(target=self.ws_test.run_forever)
        self.THEADING_DICT['hb'] = threading.Thread(target=self.socket_bypass)
        for t in self.THEADING_DICT:
            self.THEADING_DICT[t].start()
        while self.is_running:
            if self.ws_sg is None:
                self.THEADING_DICT['sg'].join()
                del self.THEADING_DICT['sg']
                self.reconnect('sg')
            if self.ws_test is None:
                self.THEADING_DICT['test'].join()
                del self.THEADING_DICT['test']
                self.reconnect('test')
            time.sleep(2)
        print(f"   {self.name} socket stop")

    def markStop(self):
        self.is_running = False
        print(f"   {self.name} waiting stop")
        for country in ['sg', 'test']:
            self.GetNoneTask(country)
        if self.ws_test:
            self.ws_test.close()
            self.ws_test = None
        if self.ws_sg:
            self.ws_sg.close()
            self.ws_sg = None
        for t in self.THEADING_DICT:
            self.THEADING_DICT[t].join()

        print(f"   {self.name} stop")


    def checkTaskCountry(self, country, taskUUID, timeout=3):
        self.check_task_uuid = taskUUID
        if taskUUID:
            self.check_task_wait = True
            self.TaskInfo(country, taskUUID)
            num = 0
            while self.check_task_wait and num < timeout:
                num += 0.01
                time.sleep(0.01)
            if self.check_task:
                return True, True, ''
            else:
                return False, False, ''
        else:
            return False, False, ''

