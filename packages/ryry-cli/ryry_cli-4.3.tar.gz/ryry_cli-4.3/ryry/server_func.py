import time, urllib3, sys, os, uuid, json
from threading import Thread, Lock

from ryry import ryry_webapi, upload, taskUtils, task, constant

lock = Lock()
def print_progress_bar(iteration, total, name, idx, total_bars):
    length=50
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    with lock:        
        sys.stdout.write(f'\0337')  # Save cursor position
        sys.stdout.write(f'\033[{total_bars-idx+1}A')  # Move cursor up to the specific progress bar line
        sys.stdout.write(f'\r{name}: |{bar}| {percent}% Complete')
        sys.stdout.write(f'\0338')  # Restore cursor position
        sys.stdout.flush()
    
class TaskThread(Thread):
    params = False
    idx = 0
    call_back = None
    def __init__(self, idx, total, func, params, callback, timeout=3600):
        super().__init__()
        self.idx = idx
        self.total = total
        self.func = func
        self.checkUUID = None
        self.checking = False
        self.checkCount = 0
        self.params = params
        self.timeout = timeout
        self.call_back = callback
        if self.call_back == None:
            raise Exception("need callback function")
        self.start()
    
    def run(self):
        self.checking = False
        self.result = False, "Unknow"
        if len(self.func) > 0:
            self.checking = True
            self.checkCount = 0
            wait_time_step = 5
            cmd = task.cmdWithWidgetName(self.func)
            if cmd:
                self.checkUUID = ryry_webapi.createLocalTask(self.func, self.params, self.timeout)
            else:
                self.checkUUID = ryry_webapi.createTask(self.func, self.params)
            time.sleep(wait_time_step)
            while self.checking and self.checkCount < self.timeout / wait_time_step:
                finish, success, data, progress = ryry_webapi.checkTask(self.checkUUID)
                print_progress_bar(progress, 100, f"Task{self.idx} {self.func}", self.idx+1, self.total)
                if finish:
                    self.checking = False
                    if success:
                        self.call_back(self.idx, data)
                        return
                self.checkCount += 1
                time.sleep(wait_time_step)
        else:
            print(f"widget {self.func} not found")
        self.call_back(self.idx, None)
        
    def __del__(self):
        if self.checking and self.checkUUID:
            ryry_webapi.TaskCancel(self.checkUUID)
        ryry_webapi.removeLocalTask(self.checkUUID)
        
class Task:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    thread_data = {}
    
    def __init__(self, func: str, multi_params: list[dict], fromUUID="", timeout=3600):
        self.thread_data = {}
        
        realTaskUUID = fromUUID
        if realTaskUUID == None or len(realTaskUUID) <= 0:
            realTaskUUID = taskUtils.taskInfoWithFirstTask()
            
        mayby_domain = ""
        if "domain" not in multi_params[0]:
            support_subdomain = upload.getFirstSupportSubdomain()
            if support_subdomain:
                mayby_domain = support_subdomain["domain"]
            
        def _callback(idx, data):
            self.thread_data[str(idx)]["result"] = data
        idx = 0
        for param in multi_params:
            param["fromUUID"] = realTaskUUID
            if "domain" not in param:
                param["domain"] = mayby_domain
            self.thread_data[str(idx)] = {
                "thread" :  TaskThread(idx, len(multi_params), func, param, _callback, timeout),
                "result" : None
            }
            idx+=1
            time.sleep(1)
        
    def call(self):
        for t in self.thread_data.keys():
            self.thread_data[t]["thread"].join()
        result = []
        for t in self.thread_data.keys():
            result.append(self.thread_data[t]["result"])
        return result
       
class AsyncTask:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def __init__(self, func: str, params: dict, fromUUID=""):
        self.params = params
        self.func = func
        
        realTaskUUID = fromUUID
        if realTaskUUID == None or len(realTaskUUID) <= 0:
            realTaskUUID = taskUtils.taskInfoWithFirstTask()
            
        self.params["fromUUID"] = realTaskUUID
        if "domain" not in self.params:
            support_subdomain = upload.getFirstSupportSubdomain()
            if support_subdomain:
                self.params["domain"] = support_subdomain["domain"]
        
    def call(self):
        cmd = task.cmdWithWidgetName(self.func)
        if cmd:
            raise Exception("local widget not support AsyncTask, please use Task")
        else:
            self.checkUUID = ryry_webapi.createTask(self.func, self.params)
            return self.checkUUID
            
    def cancel(self, taskUUID=None):
        ryry_webapi.TaskCancel(taskUUID if taskUUID else self.checkUUID)
        return True
    
    def multiCancel(self, taskUUIDs):
        ryry_webapi.multiTaskCancel(taskUUIDs)
        return True
    
    def check(self, taskUUID=None):
        finish, success, data, progress = ryry_webapi.checkTask(taskUUID if taskUUID else self.checkUUID)
        return {
            "finish": finish,
            "success": success,
            "data": data,
            "progress": progress
        }
        
    def multiCheck(self, taskUUIDs):
        results = ryry_webapi.multiCheckTask(taskUUIDs)
        json_results = {}
        for [taskUUID, finish, success, data, progress] in results:
            json_results[taskUUID] = {
                "finish": finish,
                "success": success,
                "data": data,
                "progress": progress
            }
        return json_results