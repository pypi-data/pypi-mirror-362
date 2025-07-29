import os
import requests
import datetime
import json
import socket
from requests_toolbelt import MultipartEncoder
from urllib import parse
import base64
import calendar, time
import hashlib
from ryry import utils, constant
from pkg_resources import get_distribution

task_config_file = os.path.join(constant.base_path, f"task_config.txt")
def taskInfoWithFirstTask():
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for it in data:
            if it not in ["last_task_pts"]:
                return it
    return None
def taskDomainWithUUID(taskUUID):
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r', encoding='utf-8') as f:
            task_config = json.load(f)
        if taskUUID in task_config:
            return task_config[taskUUID]["domain"]
    return ""
    
WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1b006560-7012-4bf0-8c5e-a23830bc0a0b"
def uploadFile2Wechat(filepath):
    real_robot_url = WECHAT_URL
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
def notifyWechatRobot(param):
    real_robot_url = WECHAT_URL
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        res = s.post(real_robot_url, json.dumps(param), headers=headers, verify=False, timeout=30)
        s.close()
    except Exception as e:
        print(f"===== qyapi.weixin.qq.com fail ", True)

logs = {}
def taskPrint(taskUUID, msg):
    global logs
    if (taskUUID == None or len(taskUUID) == 0) and msg == None:
        return
    if taskUUID and msg == None:
        del logs[taskUUID]
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

def _uploadLog(taskUUID):
    log_path = f"{constant.base_path}/log_{taskUUID}.log"
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(getTaskLog(taskUUID)))
        notifyWechatRobot({
            "msgtype": "file",
            "file": {
                "media_id": uploadFile2Wechat(log_path)
            }
        })
    except:
        pass
    finally:
        if os.path.exists(log_path):
            os.remove(log_path)

def notifyTaskFail(taskUUID, reason):
    try:
        real_reason = ""
        if len(reason) > 2010:
            real_reason = f"{reason[0:1000]}\n...\n{reason[len(reason)-1000:]}"
        else:
            real_reason = reason
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> 执行任务<{taskUUID}>失败\n<{real_reason}>"
            }
        })
        _uploadLog(taskUUID)
    except:
        pass

def notifyServerError(taskUUID):
    try:
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> 执行任务<{taskUUID}>上报失败, retry..."
            }
        })
    except:
        pass

def notifyScriptError(taskUUID):
    try:
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> 执行任务<{taskUUID}>异常"
            }
        })
        _uploadLog(taskUUID)
    except:
        pass

def idlingNotify(cnt):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    hour = int(float(cnt)/(60.0*60.0))
    if hour<72:
        if hour not in [1, 2, 3, 10, 30, 50, 70]:
            return
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 空转{hour}小时"
        }
    })

def onlineNotify():
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("ryry-cli").version
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]>[{ver}] 上线"
        }
    })

def restartNotify(msg):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 即将下线，原因：{msg}"
        }
    })
    
def offlineNotify():
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("ryry-cli").version
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 下线"
        }
    })

#===================================================== counter ===============================================#
task_counter_file = os.path.join(constant.base_path, "task_counter.txt")
def notifyCounterIfNeed():
    if os.path.exists(task_counter_file) == False:
        return
    with open(task_counter_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    now_hour = datetime.datetime.now().hour
    if now_hour == 0 and len(data) > 2:
        yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        s_cnt = 0
        f_cnt = 0
        all_day_usage = 0
        t_l = []
        s_l = []
        f_l = []
        for i in range(0,24):
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
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> {yesterday} 日报 \n\n\
                                >过去24小时执行任务<<font color=\"warning\">{s_cnt+f_cnt}</font>>个, 负载<<font color=\"warning\">{usage_percentage}%</font>> \n\
                                >成功<font color=\"warning\">{s_cnt}</font>个 \n\
                                >失败<font color=\"warning\">{f_cnt}</font>个"
            }
        })
        
        # import subprocess, platform
        # #darwin Command Line cannot create pyplot gui because not application with gui
        # if platform.system() != 'Darwin':
        #     try:
        #         import matplotlib.pyplot as plt
        #         plt.figure(figsize=(8,3))
        #         plt.rcParams.update({
        #             'font.size': 7
        #         })
        #         plt.bar(t_l, s_l, color='g', label='success')
        #         plt.bar(t_l, f_l, bottom=s_l, color='r', label='fail')
        #         plt.title(f'[{socket.gethostname()}] [{yesterday}] success/fail={s_cnt}/{f_cnt}')
        #         plt.xlabel('time')
        #         plt.xticks(ticks=t_l,rotation=45)
        #         plt.ylabel('count')
        #         plt.subplots_adjust(bottom=0.25)
        #         plt.legend()
        #         fff = os.path.join(constant.base_path, "plt.png")
        #         plt.savefig(fff)
        #         with open(fff, "rb") as f:
        #             encode_string = str(base64.b64encode(f.read()), encoding='utf-8')
        #         md5 = hashlib.md5()
        #         md5.update(base64.b64decode(encode_string))
        #         hash = md5.hexdigest()
        #         notifyWechatRobot({
        #             "msgtype": "image",
        #             "image": {
        #                 "base64": encode_string,
        #                 "md5": hash
        #             }
        #         })
        #         os.remove(fff)
        #         os.remove(task_counter_file)
        #     except:
        #         pass

def saveCounter(taskUUID, duration, isSuccess):
    try:
        notifyCounterIfNeed()
        if os.path.exists(task_counter_file) == False:
            with open(task_counter_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        with open(task_counter_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        #update
        now_hour = str(datetime.datetime.now().hour)
        if now_hour in data:
            if isSuccess:
                data[now_hour]["success"] += 1
            else:
                data[now_hour]["fail"] += 1
            if "usage" not in data[now_hour]:
                data[now_hour]["usage"] = 0
            data[now_hour]["usage"] += duration
        else:
            data[now_hour] = {
                "success" : 1 if isSuccess else 0,
                "fail" : 0 if isSuccess else 1,
                "usage" : 0
            }
        #save
        with open(task_counter_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except:
        pass