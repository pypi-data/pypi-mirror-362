import json, os, datetime
import uuid, requests, calendar, time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, urlunparse

from ryry import store, utils, taskUtils, constant, task

def _domain_post(func, params, files={}, timeout=10, domain="api.dalipen.com"):
    headers = {
        'Connection': 'close',
        'Usertoken': "0cce7cfe3629e16ee9b3ea8563305d3a15c524804da1861db07c2c867d79da63"
    }
    url = f"https://{domain}/{func}"
    try:
        if not files:
            headers['Content-Type'] = 'application/json'
            res = requests.post(url, json=params, timeout=timeout, verify=False, headers=headers)
        else:
            res = requests.post(url, data=params, files=files, timeout=timeout, verify=False, headers=headers)
        if res.status_code == 200:
            result_data = res.json()
            if result_data.get("code") == 0:
                return 0, "", result_data.get("data", "")
            else:
                return result_data.get("code", -1), result_data.get("msg", "Unknown error"), ""
        print(f"HTTP {res.status_code}: {res.text}")
        return -99, f"HTTP {res.status_code}: {res.text}", ""
    except requests.RequestException as e:
        # print(f"request {func} RequestException! {e}")
        return -99, f"request {func} RequestException!", ""
    except Exception as e:
        # print(f"request {func} Exception! {e}")
        return -99, f"request {func} Exception!", ""

def _aigc_post(func, params, files={}, timeout=10):
    status, msg, data = _domain_post(func, params, files, timeout, "api.dalipen.com")
    if status != -99:
        return status, msg, data
    return _domain_post(func, params, files, timeout, "aigc.zjtemplate.com")
#======================================== Task Function ==============================
def ServerTaskConfig():
    r1, r2, r3 = _aigc_post("aigc/task/config", {})
    if r1 != 0:
        raise Exception("")
    
    min_wait_time = r3["min_wait_time"]
    max_wait_time = r3["max_wait_time"]
    consecutive_step = r3["step"]
    return min_wait_time, max_wait_time, consecutive_step

def GetTask(widget_list):
    all_files = set(os.listdir(constant.base_path))
    if len(all_files) > 0:
        for filename in all_files:
            if filename.startswith("local_") and not filename.endswith(".result"):
                result_filename = filename + ".result"
                if result_filename in all_files:
                    continue  # 有 .result 文件，跳过
                file_path = os.path.join(constant.base_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        params = json.load(f)

                    config = params.get("config", {})
                    widget_id = config.get("widget_id")
                    if widget_id in widget_list:
                        with open(os.path.join(constant.base_path, filename + ".result"), "w") as f:
                            json.dump({
                                "finish": False,
                                "success": False,
                                "data": "{}",
                                "progress": 0
                            }, f)
                        return [{
                            "taskUUID": params.get("taskUUID", filename),
                            "config": json.dumps(config),
                            "data": params.get("data", {}),
                            "timeout": params.get("timeout", 600)
                        }]
                except Exception as e:
                    continue
    req = {
        "widget_map": json.dumps(widget_list),
        "limit": 1,
        "extend": store.extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/getTask", req)
    if r1 != 0:
        return []
    datas = []
    for it in r3:
        datas.append({
            "taskUUID": it["task_uuid"],
            "config": it["config"],
            "data": it["data"],
            "timeout": it["timeout"],
        })
    #Previous tasks may have failed due to network problems, so collect and resend
    retryLastTaskNotify()
    return datas

TASK_NOTIFY_DATA = os.path.join(constant.base_path, f"task_notify_data.json")
def saveTaskNotifyData(taskUUID, status, msg, dataStr):
    taskUtils.taskPrint(taskUUID, f"save {taskUUID} to next notify")
    data = []
    try:
        if not os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'w', encoding='utf-8') as f:
                json.dump([], f)
        with open(TASK_NOTIFY_DATA, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        pass
    try:
        data.append({
            "taskUUID":taskUUID,
            "status":status,
            "msg":msg,
            "dataStr":dataStr,
            "pts": calendar.timegm(time.gmtime())
        })
        with open(TASK_NOTIFY_DATA, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except:
        pass
def resetLastTaskNotify(taskUUID):
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            if it["taskUUID"] != taskUUID:
                newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w', encoding='utf-8') as f:
            json.dump(newData, f)
    except:
        pass
def retryLastTaskNotify():
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            msg = it["msg"]
            fail_count = 0
            if "fail_count" in it:
                fail_count = it["fail_count"]
            else:
                it["fail_count"] = 0
            pts = 0
            if "pts" in it:
                pts = it["pts"]
            if abs(calendar.timegm(time.gmtime())-pts) < 10: #notify late after 10 sec
                newData.append(it)
                continue
            if fail_count < 10:
                if TaskNotify(it["taskUUID"], it["status"], f"{msg} *", it["dataStr"], False) == False:
                    it["fail_count"] += 1
                    newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w', encoding='utf-8') as f:
            json.dump(newData, f)
    except:
        pass
    
def TaskNotify(taskUUID, status, msg, dataStr, failSaveNotify=True):
    if taskUUID.startswith("local_"):
        with open(os.path.join(constant.base_path, taskUUID + ".result"), "w") as f:
            json.dump( {
                "finish": True,
                "success": status,
                "data": dataStr,
                "progress": 100
            }, f)
        return True
    req = {
        "task_uuid": taskUUID,
        "status": status,
        "msg": msg,
        "dataStr": dataStr
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskNotify", req)
    if r1 != 0:
        if failSaveNotify:
            #tasks may have failed due to network problems, so collect and resend
            saveTaskNotifyData(taskUUID, status, msg, dataStr)
        return False
    return r3
  
def TaskUpdateProgress(taskUUID, progress, dataStr):
    if taskUUID.startswith("local_"):
        with open(os.path.join(constant.base_path, taskUUID + ".result"), "w") as f:
            json.dump( {
                "finish": False,
                "success": False,
                "data": dataStr,
                "progress": progress
            }, f)
        return True
    req = {
        "task_uuid": taskUUID,
        "progress": progress,
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskProgress", req)
    if r1 != 0:
        return False
    return True

def TaskCancel(taskUUID):
    if taskUUID.startswith("local_"):
        with open(os.path.join(constant.base_path, taskUUID + ".result"), "w") as f:
            json.dump( {
                "finish": True,
                "success": False,
                "data": "{}",
                "progress": 100
            }, f)
        return True
    req = {
        "task_uuid": taskUUID,
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskCancel", req)
    if r1 != 0:
        return False
    return True

def removeLocalTask(taskUUID):
    if taskUUID.startswith("local_"):
        if os.path.exists(os.path.join(constant.base_path, taskUUID)):
            os.remove(os.path.join(constant.base_path, taskUUID))
        if os.path.exists(os.path.join(constant.base_path, taskUUID + ".result")):
            os.remove(os.path.join(constant.base_path, taskUUID + ".result"))
    return True

def multiTaskCancel(checkUUIDs):
    req = {
        "task_uuids": checkUUIDs
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskCancels", req)
    if r1 != 0:
        return False
    return True

def _upload(localFilePath, ext, keepItAlways=False):
    with open(localFilePath, "rb") as f:
        files = { 'file':f }
        params = { 'ext':ext }
        if keepItAlways:
            r1, r2, r3 = _aigc_post("upload/datanet", params, files=files,timeout=100)
        else:
            r1, r2, r3 = _aigc_post("upload/create", params, files=files,timeout=100)
    if r1 != 0:
        raise Exception(f"upload fail!, reason={r2}")
    return r3

def _changeDomain(url, fix_domain):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(netloc=fix_domain))
    # netloc = parsed_url.netloc
    # if 'meco-web-hk-beta.oss-cn-hongkong.aliyuncs.com' in netloc:
    #     mecord_netloc = 'oss.zjtemplate.com'
    # elif 'meco-web-sg.oss-accelerate.aliyuncs.com' in netloc:
    #     mecord_netloc = 'oss.zjtemplate.com'
    # elif 'p-template-hk.oss-cn-hongkong.aliyuncs.com' in netloc:
    #     mecord_netloc = 'oss.zjtemplate.com'
    # elif 'p-upload-gz.oss-cn-guangzhou.aliyuncs.com' in netloc:
    #     mecord_netloc = 'upload.zjtemplate.com'
    # elif 'mecord' in netloc:
    #     mecord_netloc = 'm.mecordai.com'
    # mecord_url = parsed_url._replace(netloc=fix_domain)
    
def upload(localFilePath, ext, keepItAlways=False):
    try:
        return _upload(localFilePath, ext, keepItAlways=False)
    except:
        pass
    from mecord import upload as mecord_upload
    try:
        url = mecord_upload.upload(localFilePath, None, "sg")
        return _changeDomain(url, "m.mecordai.com")
    except:
        pass
    def upload_oss(localFilePath, ext, bucket, endpoint):
        import hashlib
        import hmac
        import base64
        timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")        
        content_type = "application/octet-stream"
        
        key_id = utils._decode_key(utils.K1)
        key_secret = utils._decode_key(utils.K2)
        
        random_name = ''.join(str(uuid.uuid4()).split('-'))
        if ext[0:1] == ".":
            ext = ext[1:]
        object_key = f"temp/{random_name}.{ext}"
        resource = f"/{bucket}/{object_key}"
        string_to_sign = f"PUT\n\n{content_type}\n{timestamp}\n{resource}"    
        signature = base64.b64encode(
            hmac.new(key_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
        ).decode('utf-8')        
        url = f"https://{bucket}.{endpoint}/{object_key}"
        headers = {
            "Date": timestamp,
            "Authorization": f"OSS {key_id}:{signature}",
            "Content-Type": content_type
        }
        with open(localFilePath, "rb") as file:
            file_data = file.read()
        response = requests.put(url, data=file_data, headers=headers)
        if response.status_code == 200:
            return url
    try:
        url = upload_oss(localFilePath, ext, "p-template-hk", "oss-cn-hongkong.aliyuncs.com")
        return _changeDomain(url, "oss.zjtemplate.com")
    except:
        pass
    try:
        url = upload_oss(localFilePath, ext, "p-upload-gz", "oss-cn-guangzhou.aliyuncs.com")
        return _changeDomain(url, "upload.zjtemplate.com")
    except:
        pass
    raise Exception("all upload target is fail!")

def uploadWidget(widget_id, name, whl, ext, version):
    with open(whl, "rb") as f:
        files = { 'file':f }
        params = {
            'widget_id':widget_id,
            'name':name,
            'version':version,
            'ext':ext
        }
        r1, r2, r3 = _aigc_post("aigc/task/publishWidget", params, files=files, timeout=300)
    if r1 != 0:
        raise Exception(f"upload widget fail!, reason={r2}")
    return r3

def CreateWidgetUUID():
    req = {}
    r1, r2, r3 = _aigc_post("aigc/task/createWidget", req)
    if r1 != 0:
        raise Exception(f"CreateWidgetUUID fail!, reason={r2}")
    return r3

#======================================== Task Function ==============================
def createLocalTask(widget_name, params, timeout):
    taskUUID = "local_" + ''.join(str(uuid.uuid4()).split('-'))
    params["task_id"] = taskUUID
    widget_id = task.widgetIDWithWidgetName(widget_name)
    with open(os.path.join(constant.base_path, taskUUID), "w") as f:
        []
        json.dump({
            "taskUUID": taskUUID,
            "config": {
                "widget_id": widget_id
            },
            "data": json.dumps(params),
            "timeout": timeout
        }, f)
    print(f"local task {taskUUID} is ready!")
    return taskUUID

def createTask(widget_name, params):
    req = {
        "widget_name": widget_name,
        "widget_data": json.dumps(params),
        "extend": store.extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/createTask", req)
    if r1 != 0:
        raise Exception(f"create task fail!, reason={r2}")
    print(f"task {r3} is pending now!")
    return r3

def findWidget(name):
    req = {
        "name": name
    }
    r1, r2, r3 = _aigc_post("aigc/task/findWidget", req)
    if r1 != 0:
        return "", "", ""
    for it in r3:
        widget_id = it["widget_id"]
        widget_name = it["name"]
        version = it["version"]
        package = it["package"]
        if widget_name.strip().lower() == name.strip().lower():
            return widget_id, version, package
    return "", "", ""

def getAutoDeployWidget():
    req = {
        "extend": store.extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/getAutoDeployWidget", req)
    result = []
    if r1 != 0:
        return result
    for it in r3:
        widget_id = it["widget_id"]
        widget_name = it["name"]
        version = it["version"]
        package = it["package"]
        is_install = it["is_install"]
        result.append([widget_id, widget_name, version, package, is_install])
    return result

def checkTask(checkUUID):
    if checkUUID.startswith("local_"):
        if os.path.exists(os.path.join(constant.base_path, checkUUID + ".result")):
            with open(os.path.join(constant.base_path, checkUUID + ".result"), "r") as f:
                result_data = json.load(f)
            finish = result_data["finish"]
            success = result_data["success"]
            data = json.loads(result_data["data"])
            progress = result_data["progress"]
            return finish, success, data, progress
        else:
            return False, False, "", 0
    req = {
        "task_uuid": checkUUID
    }
    r1, r2, r3 = _aigc_post("aigc/task/checkTask", req)
    if r1 != 0:
        return False, False, "server fail", 0
    if r3["status"] < 2:
        return False, False, "", r3["progress"]
    elif r3["status"] == 2:
        return True, True, json.loads(r3["task_result"]), r3["progress"]
    elif r3["status"] == 3:
        return True, False, r3["fail_reason"], r3["progress"]
    
def multiCheckTask(checkUUIDs):
    req = {
        "task_uuids": checkUUIDs
    }
    r1, r2, r3 = _aigc_post("aigc/task/checkTasks", req)
    result = []
    if r1 != 0:
        for checkUUID in checkUUIDs:
            result.append([checkUUID, False, False, "server fail", 0])
    for r3_item in r3:
        if r3_item["status"] < 2:
            result.append([r3_item["uuid"], False, False, "", r3_item["progress"]])
        elif r3_item["status"] == 2:
            result.append([r3_item["uuid"], True, True, json.loads(r3_item["task_result"]), r3_item["progress"]])
        elif r3_item["status"] == 3:
            result.append([r3_item["uuid"], True, False, r3_item["fail_reason"], r3_item["progress"]])
    return result
