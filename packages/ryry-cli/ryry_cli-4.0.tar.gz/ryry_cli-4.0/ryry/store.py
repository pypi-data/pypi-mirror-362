import os, platform, json, requests, locale
from ryry import constant 

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class Store(object):

    def __init__(self):
        self.path = os.path.join(constant.base_path, f"data.json")
        
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
                
    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return data
    
    def write(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    
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
    
def insertWidget(widget_id, name, version, max_task_number, path, timeout):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    widgetsMap[widget_id] = {
        "isBlock": False,
        "path" : path,
        "name" : name,
        "version" : version,
        "max_task_number" : max_task_number,
        "timeout" : timeout
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
    if widget_id == "all":
        read_data["widgets"] = {}
    else:
        if widget_id in widgetsMap:
            del widgetsMap[widget_id]
    sp.write(read_data)
    
def disableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data or not isinstance(read_data["widgets"], dict):
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    def block_one(key):
        value = widgetsMap[key]
        if isinstance(value, dict):
            widgetsMap[key]["isBlock"] = True
        else:
            widgetsMap[key] = {
                "isBlock": True,
                "path": value
            }

    if widget_id == "all":
        for key in widgetsMap:
            block_one(key)
    elif widget_id in widgetsMap:
        block_one(widget_id)
    sp.write(read_data)
    
def enableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data or not isinstance(read_data["widgets"], dict):
        read_data["widgets"] = {}    
    widgetsMap = read_data["widgets"]
    def unblock_one(key):
        value = widgetsMap[key]
        if isinstance(value, dict):
            widgetsMap[key]["isBlock"] = False
        else:
            widgetsMap[key] = {
                "isBlock": False,
                "path": value
            }
    if widget_id == "all":
        for key in widgetsMap:
            unblock_one(key)
    elif widget_id in widgetsMap:
        unblock_one(widget_id)
    sp.write(read_data)
    
#============================== device id ================================

def writeDeviceInfo(data):
    sp = Store()
    read_data = sp.read()
    read_data["deviceInfo"] = data
    sp.write(read_data)
    extend()
    
GLOBAL_EXT_JSON = "{}"
def extend():
    global GLOBAL_EXT_JSON   
    if len(GLOBAL_EXT_JSON) < 10:
        sp = Store()
        read_data = sp.read()
        if "extend" in read_data:
            GLOBAL_EXT_JSON = json.dumps(read_data["extend"])
            if len(GLOBAL_EXT_JSON) < 10:
                _genExtend()
            elif read_data["extend"].get("device_id", "") != read_data.get("deviceInfo", {}).get("device_id", ""):
                _genExtend()
        else:
            _genExtend()
    return GLOBAL_EXT_JSON

def _genExtend():
    sp = Store()
    read_data = sp.read()
    if "deviceInfo" in read_data:
        extInfo = read_data["deviceInfo"]
    else:
        extInfo = {}
    extInfo["app"] = constant.app_name + " " + constant.app_version
    extInfo["device"] = platform.system()
    extInfo["device_version"] = platform.version()
    extInfo["device_name"] = platform.node()
    extInfo["device_model"] = platform.machine()

    try:
        extInfo["ip_address"] = requests.get('https://api.ipify.org', timeout=3).text
    except Exception as e:
        extInfo["ip_address"] = "unknown"

    system_language, _ = locale.getdefaultlocale()
    system_platform = platform.system().lower()
    extInfo["language"] = system_language if system_language else "unknown"
    extInfo["platform"] = system_platform if system_platform else "unknown"
    #save
    read_data["extend"] = extInfo
    sp.write(read_data)
    global GLOBAL_EXT_JSON
    GLOBAL_EXT_JSON = json.dumps(extInfo)
    
def is_multithread():
    return get_multithread() > 1

def get_multithread():
    env_file = os.path.join(constant.base_path, "multi_thread.config")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            n = int(f.read())
            return n
    except:
        return 1
    
def save_multithread(n):
    file = os.path.join(constant.base_path, "multi_thread.config")
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(n))
    except:
        pass