import uuid
import platform
import subprocess
import os
import sys
import requests
from io import BytesIO
import psutil
import pynvml
from datetime import datetime, timedelta
import http
import json
from pathlib import Path
import socket
from PIL import Image
from ryry import constant

def get_mac_from_nettools():
    try:
        cmd = "ifconfig"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode(encoding='UTF-8')
        mac = output_str[output_str.index('ether') + 6:output_str.index('ether') + 23].replace(':', '')
        return True, mac
    except Exception as e:
        return False, None
    
def get_mac_from_system():
    try:
        root_path = '/sys/class/net/'
        dbtype_list = os.listdir(root_path)
        for dbtype in dbtype_list:
            if os.path.isfile(os.path.join(root_path, dbtype)):
                dbtype_list.remove(dbtype)

        if len(dbtype_list) == 0:
            return False, None
        mac = ''
        for dbtype in dbtype_list:
          cmd = f"cat {root_path}{dbtype}/address"
          output = subprocess.check_output(cmd, shell=True)
          mac += output.decode(encoding='UTF-8')
        return True, mac
    except Exception as e:
        return False, None

mac_value = ""
def get_mac_address():
    global mac_value
    if mac_value and len(mac_value) > 0:
        return mac_value
    
    if platform.system() == 'Windows':
        cmd = "ipconfig /all"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.find('Physical Address')
        if pos == -1:
            pos = output_str.find('物理地址')
        mac_value = (output_str[pos:pos+100].split(':')[1]).strip().replace('-', '')
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        ok, mac_value = get_mac_from_nettools()
        if ok:
            return mac_value
        ok, mac_value = get_mac_from_system()
        if ok:
            return mac_value
        return None
    else:
        mac_value = None
    return mac_value

cpu_serial = ""
def get_cpu_serial():
    global cpu_serial
    if cpu_serial and len(cpu_serial) > 0:
        return cpu_serial
    
    if platform.system() == 'Windows':
        cmd = "wmic cpu get ProcessorId"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.index("\n")
        cpu_serial = output_str[pos:].strip()
    elif platform.system() == 'Linux':
        with open('/proc/cpuinfo') as f:
            
            for line in f:
                if line[0:6] == 'Serial':
                    return "1"
                if line.strip().startswith('serial'):
                    cpu_serial = line.split(":")[1].strip()
                    break
        if not cpu_serial:
            cpu_serial = None
    elif platform.system() == 'Darwin':
        cmd = "/usr/sbin/system_profiler SPHardwareDataType"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode(encoding='UTF-8')
        cpu_serial = output_str[output_str.index('Hardware UUID:') + 14:output_str.index('Hardware UUID:') + 51].replace('-', '')
    else:
        cpu_serial = None
    return cpu_serial

def get_hostname():
    return socket.gethostname()

def generate_unique_id():
    mac = get_mac_address()
    cpu_serial = get_cpu_serial()
    hostname = get_hostname()
    if mac and cpu_serial:
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac + cpu_serial + hostname)
        return str(unique_id).replace('-', '')
    if mac :
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac + hostname)
        return str(unique_id).replace('-', '')

def getOssImageSize(p):
    try:
        s = requests.session()
        s.keep_alive = False
        res = s.get(p, timeout=60)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0
    
def deviceInfo():
    mac = get_mac_address()
    mac = "" if mac == None else mac
    cpu_serial = get_cpu_serial()
    cpu_serial = "" if cpu_serial == None else cpu_serial
    hostname = get_hostname()
    G=1024*1024*1024
    cpu_freq = "None"
    try:
        cpu_freq = psutil.cpu_freq().max / 1000
    except:
        pass
    
    virtual_mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    data = {
        "cpu": {
            "logical_count" : psutil.cpu_count(),
            "count" : psutil.cpu_count(logical=False),
            "max_freq" : f"{cpu_freq} GHz",
        },
        "disk": {
            "total": f"{(disk.total / G):.1f} G",
            "used": f"{(disk.used / G):.1f} G",
            "free": f"{(disk.free / G):.1f} G",
            "percent": f"{disk.percent}%"
        },
        "memory": {
            "total": f"{(virtual_mem.total / G):.1f} G",
            "free": f"{(virtual_mem.free / G):.1f} G"
        },
        "gpu": {
            "count" : 0,
            "list" : [],
            "mem" : []
        },
        "device_id": generate_unique_id(),
        "host_name": hostname
    }
    try:
        pynvml.nvmlInit()
        gpuCount = pynvml.nvmlDeviceGetCount()
        data["gpu"]["count"] = gpuCount
        for i in range(gpuCount):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            data["gpu"]["list"].append(f"GPU{i}: {pynvml.nvmlDeviceGetName(handle)}")
            memInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            data["gpu"]["mem"].append(f"GPU{i}: total:{(memInfo.total/G):.1f} G free:{(memInfo.free/G):.1f} G")
            
        pynvml.nvmlShutdown()
    except Exception as e:
        data["gpu"]["count"] = 1
        data["gpu"]["list"].append(f"GPU0: Normal")
    return data

def process_is_alive(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        pstatus = process.status()
        if pstatus == psutil.STATUS_RUNNING or pstatus == psutil.STATUS_SLEEPING:
            return True
        else:
            return False
    except (FileNotFoundError, psutil.NoSuchProcess):
        return False
    except Exception as e:
        return False
    
def process_is_zombie_but_cannot_kill(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        pstatus = process.status()
        if pstatus == psutil.STATUS_DISK_SLEEP:
            return True
    except Exception as e:
        return False
    return False
    
def firstExitWithDir(root, suffix):
    for root,dirs,files in os.walk(root):
        for file in files:
            if file.find(".") <= 0:
                continue
            ext = file[file.rindex("."):]
            if ext == f".{suffix}":
                return os.path.join(root, file)
        if root != files:
            break
    return None

def begin_restart(reason, update_cli=False, simple="https://pypi.python.org/simple/"):
    restart_file = os.path.join(constant.base_path, "restart")
    if os.path.exists(restart_file):
        os.remove(restart_file)
    stop_file = os.path.join(constant.base_path, "stop.now")
    with open(stop_file, 'w', encoding='utf-8') as f:
        f.write("")
    with open(restart_file, 'w', encoding='utf-8') as f:
        json.dump({
            "reason": reason,
            "update_cli": update_cli,
            "simple": simple
        },f)
    
K1 = "TFRBSTV0THNlRkFYWTMzSkE3eldEZjRv"
K2 = "MlV0ekE5Y0huZk5kWk90eExWdWhNOFNPejVIRWR2"
def _decode_key(encoded_key):
    import base64
    try:
        # 尝试解码为UTF-8字符串
        decoded_bytes = base64.b64decode(encoded_key.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，直接返回字节数据的十六进制表示
        decoded_bytes = base64.b64decode(encoded_key.encode('utf-8'))
        return decoded_bytes.hex()


def check_restart():
    restart_file = os.path.join(constant.base_path, "restart")
    if os.path.exists(restart_file) == False:
        return
    from ryry import taskUtils
    from ryry import store
    import time, calendar, platform, subprocess
    reason = "unknow"
    update_cli = False
    simple = "https://pypi.python.org/simple/"
    try:
        with open(restart_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            reason = config["reason"]
            update_cli = config["update_cli"]
            simple = config["simple"]
    except:
        pass

    if platform.system() == 'Windows':
        time_task_file = os.path.join(constant.base_path, "update_ryry.bat")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        time_task_file = os.path.join(constant.base_path, "update_ryry.sh")
    else:
        time_task_file = os.path.join(constant.base_path, "update_ryry.txt")
    if os.path.exists(time_task_file):
        os.remove(time_task_file)

    def getCommandResult(cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    print(" restart_ryry_cli begin...")
    taskUtils.restartNotify(reason)
    restart_command = "ryry service start"
    threadNum = store.get_multithread()
    if threadNum > 1:
        restart_command = f"{restart_command} -thread {threadNum}"
    restart_command = f"{restart_command}"
    if platform.system() == 'Windows':
        new_time = datetime.now() + timedelta(minutes=1)
        win_time = new_time.strftime("%H:%M")
        with open(time_task_file, 'w', encoding='utf-8') as f:
            if update_cli:
                f.write(f'''pip uninstall ryry-cli -y 
pip install -U ryry-cli -i {simple} --extra-index-url https://pypi.python.org/simple/
start /B {restart_command}''')
            else:
                f.write(f'''start /B {restart_command}''')
        result = subprocess.Popen(['schtasks', '/create', '/sc', 'ONCE', '/st', f'{win_time}', '/tn', f'ryryUpdate-{calendar.timegm(time.gmtime())}', '/tr', f"\"{time_task_file}\""], shell=True)
        print(f"{result.stdout}\n{result.stderr}")
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        def run_subprocess(s):
            r = subprocess.run(s, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            print(f"{r.stdout}\n{r.stderr}")
        if len(getCommandResult("which at")) <= 0:
            run_subprocess(f"apt-get update")
            run_subprocess(f"apt-get upgrade")
            run_subprocess(f"apt-get install -y at libopencv-features2d-dev=4.5.4+dfsg-9ubuntu4 systemctl")
        run_subprocess(f"systemctl start atd")
        with open(time_task_file, 'w', encoding='utf-8') as f:
            if update_cli:
                f.write(f'''#!/bin/bash
pip uninstall ryry-cli -y 
pip3 uninstall ryry-cli -y 
pip install -U ryry-cli -i {simple} --extra-index-url https://pypi.python.org/simple/
pip3 install -U ryry-cli -i {simple} --extra-index-url https://pypi.python.org/simple/
nohup {restart_command} &''')
            else:
                f.write(f'''#!/bin/bash
nohup {restart_command} &''')
        ot = os.path.join(constant.base_path, "update_ryry.out")
        result = subprocess.run(f"at now + 1 minutes -f {time_task_file} > {ot}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print(f"{result.stdout}\n{result.stderr}")
    os.remove(restart_file)
    print("one minute later must be start!")