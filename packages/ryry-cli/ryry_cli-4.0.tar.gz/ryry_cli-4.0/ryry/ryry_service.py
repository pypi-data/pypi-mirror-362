import sys, os, time, signal, subprocess, logging, json, platform, socket, calendar
from logging.handlers import RotatingFileHandler
from urllib.parse import *
from threading import Thread

from ryry.daemon_manager import daemon_manager
from ryry import store, ryry_webapi, utils, taskUtils, ryry_widget, constant
from ryry import ryry_server_socket as TaskConnector

pid_file = os.path.join(constant.base_path, "ryryService.pid")
stop_file = os.path.join(constant.base_path, "stop.now")
stop_thread_file = os.path.join(constant.base_path, "stop.thread")
all_thread_stoped = os.path.join(constant.base_path, "all_stoped.now")
def notify_other_stoped():
    with open(all_thread_stoped, 'w', encoding='utf-8') as f:
        f.write("")

class LogStdout(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        logFilePath = f"{constant.base_path}/log.log"
        file_handler = RotatingFileHandler(logFilePath, maxBytes=1024*1024*20, backupCount=30, encoding="utf-8")
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

class ryryService:
    def __init__(self):
        self.THEADING_LIST = []

    def start(self, threadNum=1):
        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r', encoding='utf-8') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    taskUtils.notifyWechatRobot({
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        #1: service init 
        sys.stdout = LogStdout()
        with open(pid_file, 'w', encoding='utf-8') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, self.stop)
        store.save_multithread(threadNum)
        store.writeDeviceInfo(utils.deviceInfo())
        TaskConnector._clearTask()
        
        #2: service step
        executor = TaskConnector.RyryTaskExecutor()
        self.THEADING_LIST.append(executor)
        self.THEADING_LIST.append(TaskConnector.RyryShortConnectThread(executor))
        self.THEADING_LIST.append(ryryDaemonThread())
        self.THEADING_LIST.append(ryryStateThread())
        
        #3: service step
        while (os.path.exists(stop_file) == False):
            time.sleep(5)
        print("Prepare stop")
        
        with open(stop_thread_file, 'w', encoding='utf-8') as f:
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
        print("Service has ended!")
        utils.check_restart()
        sys.stdout.close()

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
        with open(stop_file, 'w', encoding='utf-8') as f:
            f.write("")
        print("ryryService waiting stop...")
        taskUtils.restartNotify("手动")
        while os.path.exists(stop_file):
            time.sleep(1)
        print("ryryService has ended!")
    
class ryryDaemonThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"ryryDaemonThread"
        self.tik_time = 30.0
        self.start()    
    
    def run(self):
        print(f"   {self.name} start")
        daemon_manager.start_all_daemons()
        
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(self.tik_time)
            try:
                daemon_manager.sync_daemons_with_widget_map()
            except:
                time.sleep(60)
                
        try:
            print("Stopping daemon processes...")
            if daemon_manager.stop_all_daemons():
                print("All daemon processes stopped")
            else:
                print("Some daemon processes failed to stop gracefully")
        except Exception as e:
            print(f"Failed to stop daemon processes: {e}")
        
        print(f"   DaemonThread stop")
        notify_other_stoped() #because other thread is waiting some signal to close
    def markStop(self):
        print(f"   DaemonThread waiting stop")
        
class ryryStateThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"ryryStateThread"
        self.daemon = True
        self.tik_time = 30.0
        self.start()
    
    def run(self):
        print(f"   {self.name} start")
        taskUtils.onlineNotify()
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(self.tik_time)
            try:
                task_config = TaskConnector._getTaskConfig()
                if task_config["last_task_pts"] > 0:
                    cnt = (calendar.timegm(time.gmtime()) - task_config["last_task_pts"]) #second
                    if cnt >= (60*60) and cnt/(60*60)%1 <= self.tik_time/3600:
                        taskUtils.idlingNotify(cnt)
                        #clear trush
                        now = time.time()
                        threshold = 24 * 3600 
                        for root, dirs, files in os.walk(constant.base_path):
                            for file in files:
                                full_path = os.path.join(root, file)
                                if (
                                    file.endswith(".in") or
                                    file.endswith(".out") or
                                    file.startswith("local_")
                                ):
                                    # 检查文件是否超过 24 小时
                                    mtime = os.path.getmtime(full_path)
                                    if now - mtime > threshold:
                                        try:
                                            os.remove(full_path)
                                        except Exception as e:
                                            pass
                            break  # 只处理当前目录，不递归子目录
                #更新机器性能
                store.writeDeviceInfo(utils.deviceInfo())
            except:
                time.sleep(60)
        print(f"   StateChecker stop")
        notify_other_stoped() #because other thread is waiting some signal to close
    def markStop(self):
        print(f"   StateChecker waiting stop")
        