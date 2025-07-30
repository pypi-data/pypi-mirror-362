import os, time, json, calendar
from urllib.parse import *
import threading
from datetime import datetime, timedelta
from threading import Thread, current_thread, Lock
import uuid
import queue
import subprocess, platform

from ryry import store, ryry_widget, ryry_webapi, task, constant, utils, taskUtils
from ryry.shared_memory import shared_memory_service

class RyryTaskExecutor(Thread):
    THEADING_LIST = []
    is_running = False
    task_queue = None
    ttt = 0
    
    def appendTask(self, data, callback):
        shared_memory_service.increment_cur_counter()
        self.task_queue.put([data, callback])
        try:
            taskUUID = data["taskUUID"]
            taskUtils.taskPrint(taskUUID, f"{current_thread().name} === addQueue task : {taskUUID}")
        except:
            pass
            
    def idlePower(self):
        return shared_memory_service.get_max_counter() - shared_memory_service.get_cur_counter()
    
    def widgetHasPower(self, cur_widget_id):
        widget_power = shared_memory_service.get_widget_power(cur_widget_id)
        if widget_power:
            return widget_power["cur"] < widget_power["max"]
        return True  # widget找不到的话就当作可以接
        
    def addWidgetPower(self, widget_id, max_task_number):
        # 检查widget是否已经初始化，如果没有则初始化最大任务数
        widget_power = shared_memory_service.get_widget_power(widget_id)
        if widget_power is None:
            # 首次初始化widget
            shared_memory_service.set_widget_power(widget_id, max_task_number, 0)
        
        # 增加当前任务数
        shared_memory_service.increment_widget_cur_power(widget_id)
        
    def delWidgetPower(self, widget_id):
        shared_memory_service.decrement_widget_cur_power(widget_id)
    
    def isWorking(self):
        return shared_memory_service.get_cur_counter() > 0
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = f"RyryTaskExecutor"
        self.task_queue = queue.Queue()
        # 启动共享内存服务并初始化数据
        self.max_counter = store.get_multithread()
        self.is_running = True
        self.THEADING_LIST = []
        self.start()

    def taskRunning(self):
        print(f"      - {current_thread().name} waiting")
        while self.is_running:
            try:
                data, callback = self.task_queue.get()
                if data is None: 
                    break
                try:
                    data_config = json.loads(data["config"])
                    widget_id = data_config["widget_id"]
                    max_task_number = data_config.get("max_task_number", 0)
                    if max_task_number <= 0:
                        max_task_number = task.maxTaskNumberWithWidget(widget_id)
                    timeout = data_config.get("timeout", 600)
                    if "timeout" in data:
                        timeout = data["timeout"]
                    
                    taskUUID = data["taskUUID"]
                    domain = ""
                    params_tmp = json.loads(data["data"])
                    if "domain" in params_tmp:
                        domain = params_tmp["domain"]
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === receive task : {taskUUID}")
                    _appendTask(taskUUID, domain)
                    self.addWidgetPower(widget_id, max_task_number)
                    is_ok, msg, result = task.runTask(data, timeout)
                    if is_ok == False:
                        taskUtils.notifyTaskFail(taskUUID, msg)
                    shared_memory_service.decrement_cur_counter()
                    callback(taskUUID, is_ok, msg, result)
                    _removeTask(taskUUID)
                    self.delWidgetPower(widget_id)
                except Exception as e:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === task exception : {e}")
                    taskUtils.notifyScriptError(taskUUID)
                finally:
                    taskUtils.taskPrint(taskUUID, None)
                self.task_queue.task_done()
            except Exception as ex:
                taskUtils.taskPrint(None, f"{current_thread().name} === exception : {ex}")
                pass
        print(f"   {current_thread().name} taskRunning stop")

    def run(self):
        shared_memory_service.start_service()
        shared_memory_service.set_max_counter(self.max_counter)
        shared_memory_service.set_cur_counter(0)
        for idx in range(0, self.max_counter):
            self.THEADING_LIST.append(Thread(name=f"exector-{idx}",target=self.taskRunning))
        for t in self.THEADING_LIST:
            t.start()
        while self.is_running:
            time.sleep(5)
        for t in self.THEADING_LIST:
            t.join()
        print(f"   {self.name} stop!")

    def markStop(self):
        self.is_running = False
        print(f"   {self.name} waiting stop")
        for _ in range(self.max_counter*2):
            self.task_queue.put([None, None])
        print(f"   {self.name} stop")
        shared_memory_service.stop_service()

lock = Lock()
task_config_file = os.path.join(constant.base_path, f"task_config.txt")    
def _readTaskConfig():
    if os.path.exists(task_config_file) == False:
        with open(task_config_file, 'w', encoding='utf-8') as f:
            json.dump({
                "last_task_pts": 0
            }, f)
    with open(task_config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
def _saveTaskConfig(data):
    with open(task_config_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
def _appendTask(taskUUID, subDomain):
    lock.acquire()
    task_config = _readTaskConfig()
    task_config[taskUUID] = {
        "pts": calendar.timegm(time.gmtime()),
        "domain": subDomain
    }
    task_config["last_task_pts"] = task_config[taskUUID]["pts"]
    _saveTaskConfig(task_config)
    lock.release() 
def _clearTask():
    lock.acquire()
    task_config = {
        "last_task_pts": 0
    }
    _saveTaskConfig(task_config)
    lock.release() 
def _removeTask(taskUUID):
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        del task_config[taskUUID]
    _saveTaskConfig(task_config)
    lock.release() 
def _taskCreateTime(taskUUID):
    pts = 0
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        pts = task_config[taskUUID]["pts"]
    lock.release()
    return pts 
def _getTaskConfig():
    lock.acquire()
    task_config = _readTaskConfig()
    lock.release() 
    return task_config

class RyryShortConnectThread(Thread):
    is_running = False
    executor: RyryTaskExecutor = None

    def __init__(self, executor):
        super().__init__()
        self.name = f"ShortConnect"
        self.is_running = True
        self.executor = executor
        self.last_check_time = calendar.timegm(time.gmtime())
        self.start()
    
    def taskCallback(self, taskUUID, is_ok, msg, result):
        ryry_webapi.TaskNotify(taskUUID, is_ok, msg, result)

    def checkWidgetVersion(self):
        if calendar.timegm(time.gmtime()) - self.last_check_time > 300:
            self.last_check_time = calendar.timegm(time.gmtime())
            try:
                #update widget
                ryry_widget.UpdateWidgetFromPypi()
            except Exception as ex:
                print(f'update widget fail, {ex}')

        # if platform.system() != 'Darwin':
        #     try:
        #         #update cli
        #         remote_version = ryry_widget._remote_package_version("ryry-cli")
        #         simple = "https://pypi.python.org/simple/"
        #         local_version, local_path = ryry_widget._local_package_info("ryry-cli")
        #         if ryry_widget.compare_versions(remote_version, local_version) > 0:
        #             print("start update progress...")
        #             utils.begin_restart("auto upgrade ryry-cli", True, simple)
        #             device_id = utils.generate_unique_id()
        #             machine_name = socket.gethostname()
        #             ver = get_distribution("ryry-cli").version
        #             taskUtils.notifyWechatRobot({
        #                 "msgtype": "text",
        #                 "text": {
        #                     "content": f"机器<{machine_name}[{device_id}]>[{ver}] ryry-cli开始升级[{local_version}]->[{remote_version}]"
        #                 }
        #             })
        #             break
        #     except Exception as ex:
        #         print(f'update ryry-cli fail, {ex}')

    def run(self):
        print(f"   {self.name} start")
        min_wait_time = 5
        max_wait_time = 60
        wait_time = min_wait_time
        consecutive_step = 10
        consecutive_failures = 0
        max_consecutive_failures = 10
        last_check_time = 0
        
        while (self.is_running):
            try:
                if self.executor.idlePower() == 0:
                    time.sleep(1)
                    continue
                
                widget_list = []
                map = store.widgetMap()
                for it in map:
                    if isinstance(map[it], (dict)):
                        if map[it]["isBlock"] == False and self.executor.widgetHasPower(it):
                            widget_list.append(it)
                    else:
                        if self.executor.widgetHasPower(it):
                            widget_list.append(it)
                datas = ryry_webapi.GetTask(widget_list)
                for it in datas:
                    self.executor.appendTask(it, self.taskCallback)
                    
                # if task empty -> full, set wait_time = max -> min
                if len(datas) > 0:
                    consecutive_failures = 0
                    wait_time = max(min_wait_time, wait_time - consecutive_step)
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        wait_time = min(max_wait_time, wait_time + consecutive_step)
                        consecutive_failures = 0
                        
                if calendar.timegm(time.gmtime()) - last_check_time > 600:
                    last_check_time = calendar.timegm(time.gmtime())
                    try:
                        min_wait_time, max_wait_time, consecutive_step = ryry_webapi.ServerTaskConfig()
                    except:
                        pass


            except Exception as ex:
                taskUtils.taskPrint(None, f"{self.name} === exception : {ex}")
            time.sleep(wait_time)
            if self.executor.isWorking() == False:
                #自动更新widget
                self.checkWidgetVersion()
            
        print(f"   {self.name} stop")

    def markStop(self):
        print(f"   {self.name} waiting stop")
        self.is_running = False