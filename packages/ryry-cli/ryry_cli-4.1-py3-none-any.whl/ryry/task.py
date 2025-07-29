import os, time, calendar
import json
from urllib.parse import *
import sys
import signal
import subprocess, multiprocessing
from threading import Thread, current_thread, Lock
import xmlrpc.client

from ryry import ryry_webapi,store,taskUtils,utils,constant
from pathlib import Path

# 延迟导入daemon_manager，避免循环依赖
daemon_manager = None

def runTask(it, timeout):
    start_time = calendar.timegm(time.gmtime())
    taskUUID = it["taskUUID"]
    config = json.loads(it["config"])
    params = json.loads(it["data"])
    widget_id = config["widget_id"]
    
    # 检查是否启用常驻进程
    if should_use_daemon(widget_id):
        # 使用常驻进程执行任务
        return execute_with_daemon(taskUUID, widget_id, params, timeout, start_time)
    else:
        # 使用传统方式执行任务
        return execute_with_subprocess(taskUUID, widget_id, params, timeout, start_time)


def should_use_daemon(widget_id: str) -> bool:
    """检查是否应该使用常驻进程执行任务"""
    global daemon_manager
    
    if daemon_manager is None:
        from ryry.daemon_manager import daemon_manager
    
    try:
        # 检查daemon是否正在运行且接受任务
        status = daemon_manager.get_daemon_status(widget_id)
        return status.get("running", False) and status.get("accept_tasks", False)
    except Exception:
        return False


def get_widget_config(widget_id: str) -> dict:
    """获取widget配置"""
    widget_map = store.widgetMap()
    if widget_id not in widget_map:
        return None
    
    widget_info = widget_map[widget_id]
    if isinstance(widget_info, dict):
        path = widget_info["path"]
    else:
        path = widget_info
    
    # 读取widget配置
    config_path = os.path.join(os.path.dirname(path), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None


def execute_with_daemon(taskUUID: str, widget_id: str, params: dict, timeout: int, start_time: float):
    """使用常驻进程执行任务"""
    global daemon_manager
    
    if daemon_manager is None:
        from ryry.daemon_manager import daemon_manager
    
    try:
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== start execute task with daemon: {taskUUID}")
        
        # 在常驻进程中执行任务
        success, error_msg, result_data = daemon_manager.execute_task(widget_id, params, timeout)
        
        if success and isinstance(result_data, dict):
            # 使用daemon返回的结果格式
            result_obj = result_data
        else:
            # 构造错误结果
            result_obj = {"result": [], "status": 1, "message": error_msg}
        
        # 处理结果
        is_ok = success and result_obj.get("status", 1) == 0
        msg = result_obj.get("message", error_msg)
        
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== daemon task {taskUUID} is_ok={is_ok}")
        taskUtils.saveCounter(taskUUID, (calendar.timegm(time.gmtime()) - start_time), is_ok)
        
        return is_ok, msg, json.dumps(result_obj.get("result", []), separators=(',', ':'))
        
    except Exception as e:
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== daemon task {taskUUID} failed: {e}")
        taskUtils.saveCounter(taskUUID, (calendar.timegm(time.gmtime()) - start_time), False)
        return False, str(e), json.dumps([], separators=(',', ':'))


def execute_with_subprocess(taskUUID: str, widget_id: str, params: dict, timeout: int, start_time: float):
    """使用子进程执行任务（传统方式）"""
    #cmd
    cmd = cmdWithWidget(widget_id)
    #params
    params["task_id"] = taskUUID
    #run
    taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== start execute task : {taskUUID}")
    executeSuccess, result_obj = executeLocalPython(taskUUID, cmd, params, timeout)
    #result
    is_ok = executeSuccess and result_obj["status"] == 0
    msg = ""
    if len(result_obj["message"]) > 0:
        msg = str(result_obj["message"])
    taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== task {taskUUID} is_ok={is_ok} ")
    taskUtils.saveCounter(taskUUID, (calendar.timegm(time.gmtime()) - start_time), is_ok)
    return is_ok, msg, json.dumps(result_obj["result"], separators=(',', ':'))

def cmdWithWidget(widget_id):
    map = store.widgetMap()
    if widget_id in map:
        path = ""
        is_block = False
        if isinstance(map[widget_id], (dict)):
            is_block = map[widget_id]["isBlock"]
            path = map[widget_id]["path"]
        else:
            is_block = False
            path = map[widget_id]
        if len(path) > 0 and is_block == False:
            return path
    return None

def maxTaskNumberWithWidget(widget_id):
    map = store.widgetMap()
    if widget_id in map:
        return map[widget_id].get("max_task_number", 1)
    return 1

def cmdWithWidgetName(name):
    map = store.widgetMap()
    for widget_id in map.keys():
        if "name" not in map[widget_id]:
            continue
        if map[widget_id]["name"] == name and map[widget_id]["isBlock"] == False:
            is_block = map[widget_id]["isBlock"]
            return map[widget_id]["path"]
    return None

def widgetIDWithWidgetName(name):
    map = store.widgetMap()
    for widget_id in map.keys():
        if "name" not in map[widget_id]:
            continue
        if map[widget_id]["name"] == name and map[widget_id]["isBlock"] == False:
            return widget_id
    return None

def executeLocalPython(taskUUID, cmd, param, timeout=3600):
    # # 检查代码更新
    # check_code_update()
    
    # # 确保RPC服务器运行
    # ensure_rpc_server_running()
    
    # # 添加RPC服务器信息到环境变量
    env = os.environ.copy()
    # env['RPC_SERVER_PORT'] = str(_rpc_port)
    
    inputArgs = os.path.join(constant.base_path, f"{taskUUID}.in")
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w', encoding='utf-8') as f:
        json.dump(param, f)
    outArgs = os.path.join(constant.base_path, f"{taskUUID}.out")
    if os.path.exists(outArgs):
        os.remove(outArgs)
        
    outData = {
        "result" : [ 
        ],
        "status" : -1,
        "message" : "script error"
    }
    executeSuccess = False
    command = [sys.executable, cmd, "--run", inputArgs, "--out", outArgs]
    taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== exec => {command}")
    process = None
    try:
        if timeout == 0:
            timeout = 60*30
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        timeout_killprocess(process, timeout)
        output, error = process.communicate()
        if process.returncode == 0:
            taskUtils.taskPrint(taskUUID, output.decode(encoding="utf8", errors="ignore"))
            if os.path.exists(outArgs) and os.stat(outArgs).st_size > 0:
                try:
                    with open(outArgs, 'r', encoding='UTF-8') as f:
                        outData = json.load(f)
                    executeSuccess = True
                    taskUtils.taskPrint(taskUUID, f"[{taskUUID}]exec success result => {outData}")
                except:
                    taskUtils.taskPrint(taskUUID, f"[{taskUUID}]task result format error, please check => {outData}")
            else:
                taskUtils.taskPrint(taskUUID, f"[{taskUUID}]task result is empty!, please check {cmd}")
        else:
            taskUtils.taskPrint(taskUUID, f"====================== script error [{taskUUID}]======================")
            o1 = output.decode(encoding="utf8", errors="ignore")
            o2 = error.decode(encoding="utf8", errors="ignore")
            error_msg = f"{o1}\n{o2}"
            short_error_msg = ""
            if len(error_msg) > 1810:
                short_error_msg = f"{error_msg[0:900]}\n...\n{error_msg[len(error_msg)-900:]}"
            else:
                short_error_msg = error_msg
            outData["message"] = short_error_msg
            taskUtils.taskPrint(taskUUID, error_msg)
            taskUtils.taskPrint(taskUUID, "======================     end      ======================")
            taskUtils.notifyScriptError(taskUUID)
    except Exception as e:
        time.sleep(1) 
        taskUtils.taskPrint(taskUUID, f"====================== process error [{taskUUID}]======================")
        taskUtils.taskPrint(taskUUID, e)
        taskUtils.taskPrint(taskUUID, "======================      end      ======================")
        if process:
            os.kill(process.pid, signal.SIGTERM) 
            if process.poll() is None:
                os.kill(process.pid, signal.SIGKILL)  
        taskUtils.notifyScriptError(taskUUID)
        outData["message"] = str(e)
    finally:
        if process and process.returncode is None:
            try:
                print("kill -9 " + str(process.pid))
                os.system("kill -9 " + str(process.pid))
            except ProcessLookupError:
                pass
        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        if os.path.exists(outArgs):
            os.remove(outArgs)
    return executeSuccess, outData

def updateProgress(data, progress=50, taskUUID=None):
    realTaskUUID = taskUUID
    if realTaskUUID == None or len(realTaskUUID) <= 0:
        realTaskUUID = taskUtils.taskInfoWithFirstTask()
        
    if progress < 0:
        progress = 0
    if progress > 100:
        progress = 100
    if realTaskUUID and len(realTaskUUID) > 10 and realTaskUUID.startswith("local_") == False:
        return ryry_webapi.TaskUpdateProgress(realTaskUUID, progress, json.dumps(data))

def timeout_killprocess(proc, timeout): # """超过指定的秒数后杀死进程"""
    import threading
    timer = threading.Timer(timeout, lambda p: p.kill(), [proc])
    try:
        timer.start()
        proc.communicate()
    except Exception as e:
        print(e)
    finally:
        timer.cancel()

