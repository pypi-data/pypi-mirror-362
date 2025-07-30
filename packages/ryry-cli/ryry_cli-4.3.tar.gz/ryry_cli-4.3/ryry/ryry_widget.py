import os, json,sys,shutil,zipfile,pkg_resources,threading,time,requests
import random, uuid, re, subprocess, platform, zipfile
from pkg_resources import get_distribution
import socket

from pathlib import Path
from ryry import store, ryry_webapi, upload, taskUtils, utils, constant

def compare_versions(version1, version2):
    if len(version1) <= 0:
        version1 = "0"
    if len(version2) <= 0:
        version2 = "0"
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))
    while len(v1) < len(v2):
        v1.append(0)
    while len(v2) < len(v1):
        v2.append(0)
    for i in range(len(v1)):
        if v1[i] < v2[i]:
            return -1
        elif v1[i] > v2[i]:
            return 1
    return 0

#real time version get
def _local_package_info(py_package):
    _map = store.widgetMap()
    for it in _map:
        try:
            widget_path = os.path.dirname(_map[it]["path"])
            widget_config = GetWidgetConfig(widget_path)
            if widget_config["name"] == py_package:
                return widget_config["version"], widget_path
        except:
            pass
    return '', ''

def _pypi_folder_name(name):
    import re
    return re.sub(r"[/,\-\s]", "", name)

def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
    if os.path.exists(path):
        for filename in os.listdir(path):
            pathname = os.path.join(path, filename) 
            if (os.path.isfile(pathname)) and filename in ["config.json", "config.json.py"]:
                with open(pathname, 'r', encoding='UTF-8') as f:
                    return json.load(f)
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename in ["config.json", "config.json.py"]:
            with open(pathname, 'r', encoding='UTF-8') as f:
                return json.load(f)
    return {}

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def replaceIfNeed(dstDir, name, subfix):
    newsubfix = subfix + ".py"
    if name.find(newsubfix) != -1:
        os.rename(os.path.join(dstDir, name), os.path.join(dstDir, name.replace(newsubfix, subfix)))

def copyWidgetTemplate(root, name):
    templateDir = os.path.join(constant.base_path, name)#sys.prefix
    dstDir = root
    for item in os.listdir(templateDir):
        source = os.path.join(templateDir, item)
        destination = os.path.join(dstDir, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    shutil.rmtree(os.path.join(dstDir, "__pycache__"))
    os.remove(os.path.join(dstDir, "__init__.py"))
    for filename in os.listdir(dstDir):
        replaceIfNeed(dstDir, filename, ".json")
        replaceIfNeed(dstDir, filename, ".js")
        replaceIfNeed(dstDir, filename, ".png")
        replaceIfNeed(dstDir, filename, ".html")

def setWidgetData(root, widgetid):
    data = GetWidgetConfig(root)
    data["widget_id"] = widgetid
    data["name"] = "Demo"
    data["version"] = "1.0"
    data["max_task_number"] = 1
    data["cmd"] = os.path.join(root, "main.py")
    data["timeout"] = 600
    data["daemon_enabled"] = False
    with open(os.path.join(root, "config.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f)

def createWidget(root):
    if PathIsEmpty(root) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = ryry_webapi.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create widget fail! ryry server is not avalid")
        return
    
    copyWidgetTemplate(root, "script_template")
    setWidgetData(root, widgetid)
    addWidgetToEnv(root, True)
    print("create widget success")

def CheckWidgetDataInPath(path):
    data = GetWidgetConfig(path)
    if "widget_id" not in data:
        print("folder is not widget")
        return False

    if "widget_id" in data:
        widget_id = data["widget_id"]
        if len(widget_id) == 0:
            print("widget_id is empty!")
            return False
        
    return True

def addWidgetToEnv(name_or_root, mute=False):
    #maybe pip package
    root = ""
    try:
        package = pkg_resources.get_distribution(name_or_root)
        local_version = package.version
        name = package.project_name
        version = package.version
        root = os.path.join(package.location, name.replace("-", "_"))
    except:
        pass
    
    if os.path.exists(root) == False:
        root = os.path.join(constant.base_path, "widget", name_or_root)
        
    if os.path.exists(root) == False:
        if mute == False:
            print(f"{name_or_root} not found")
        return
    
    if CheckWidgetDataInPath(root) == False:
        return
    data = GetWidgetConfig(root)
    widget_id = data["widget_id"]
    name = data["name"]
    version = data["version"]
    max_task_number = data.get("max_task_number", 1)
    timeout = data.get("timeout", 600)
    mainPythonPath = os.path.join(root, "main.py")
    store.insertWidget(widget_id, name, version, max_task_number, mainPythonPath, timeout)
    if mute == False:
        print(f"add {widget_id.ljust(len(widget_id)+4)} {mainPythonPath}")

def remove(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    # if ryry_webapi.DeleteWidget(widget_id):
    store.removeWidget(widget_id)
    print(f"widget:{widget_id} is removed with local")
        
def enable(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    store.enableWidget(widget_id)
    print(f"widget:{widget_id} updated")
        
def disable(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    store.disableWidget(widget_id)
    print(f"widget:{widget_id} updated")

def publishWidget(package_folder):
    if CheckWidgetDataInPath(package_folder) == False:
        return
        
    data = GetWidgetConfig(package_folder)
    widget_id = data["widget_id"]
    name = None
    if "name" in data:
        name = data["name"]
    if name == "Demo":
        print(f"请修改widget名字, 位置为{package_folder}/config.json")
        return
    if "py_package" in data:
        name = data["py_package"]
    if re.match(r'^[A-Za-z0-9_-]+$', name) == False:  
        print(f"请修改widget名字, 只能包含英文字母、数字、下划线、中划线")
        return
    local_version = "1.0"
    if "version" in data:
        local_version = data["version"]
    user_id = utils.generate_unique_id()
        
    #if in h5&script parent folder, add env path
    if len(package_folder) > 0:
        addWidgetToEnv(package_folder, True)
        
    #package python to private pip server
    requirements_txts = [
        os.path.join(package_folder, "requirements.txt")
    ]
    requirements = ""
    for requirements_txt in requirements_txts:
        if os.path.exists(requirements_txt):
            with open(requirements_txt, "r", encoding="UTF-8") as f:
                ss = f.readlines()
                for s in ss:
                    reals = s.replace("\n","").replace(" ","")
                    if ";" in reals:
                        requirements += f"'{reals[:reals.index(';')]}',"  
                    elif "#" not in reals:
                        requirements += f"'{reals}',"
    temp_dir = os.path.join(os.path.dirname(package_folder), "tmp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    publish_zip_file = os.path.join(os.path.dirname(package_folder), "tmp.zip")
    try:
        shutil.copytree(package_folder, temp_dir)
        #archive zip file
        with zipfile.ZipFile(publish_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:  
            for root, dirs, files in os.walk(temp_dir):  
                if root.startswith(".") or root == "__pycache__":
                    continue
                for file in files:  
                    file_path = os.path.join(root, file)  
                    relative_path = os.path.relpath(file_path, temp_dir)  
                    zipf.write(file_path, arcname=relative_path)  
        #upload
        ryry_webapi.uploadWidget(widget_id, name, publish_zip_file, ".zip", local_version)
        print(f"发布 {name}_{local_version} -> 成功")
    except Exception as ex:
        print(ex)
    finally:
        shutil.rmtree(temp_dir)
        if os.path.exists(publish_zip_file):
            os.remove(publish_zip_file)

def widgetUpdateNotify(widgetName, oldver, newver):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("ryry-cli").version
    taskUtils.notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]>[{ver}] widget:[{widgetName}]升级版本[{oldver}]->[{newver}]"
        }
    })
    
def widgetUninstallNotify(widgetName, newver):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("ryry-cli").version
    taskUtils.notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]>[{ver}] 卸载widget:[{widgetName}][{newver}]"
        }
    })
    
def widgetInstallNotify(widgetName, newver):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    ver = get_distribution("ryry-cli").version
    taskUtils.notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]>[{ver}] 安装widget:[{widgetName}][{newver}]"
        }
    })

def widgetReInstall(name, url, local_path):
    def find_pip_command():
        possible_pips = ['pip3.11', 'pip', 'pip3']
        for cmd in possible_pips:
            pip_path = shutil.which(cmd)
            if pip_path:
                return cmd

        for version in range(12, 11, 10, 9, 8, 13, -1):
            cmd = f"pip3.{version}"
            pip_path = shutil.which(cmd)
            if pip_path:
                return cmd
                
        raise RuntimeError("No pip command found on the system.")
    pip_cmd = find_pip_command()
    if url.endswith(".whl"):
        if name:
            subprocess.run(f"{pip_cmd} uninstall {name} -y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        subprocess.run(f"{pip_cmd} install {url} -i https://pypi.python.org/simple/ --extra-index-url https://pypi.python.org/simple/", 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    elif url.endswith(".zip"):
        if os.path.exists(local_path) == False:
            local_path = os.path.join(constant.base_path, "widget", name)
    
        download_file = os.path.join(constant.base_path, ''.join(str(uuid.uuid4()).split('-')) + ".zip")
        try:
            with open(download_file, 'wb+') as f:
                f.write(requests.get(url).content)
        except:
            #bak url
            bak_url = url.replace("widget.dalipen.com", "aigc.zjtemplate.com/widget")
            bak_url = bak_url.replace("r2.dalipen.com", "aigc.zjtemplate.com/r2")
            bak_url = bak_url.replace("datenet.dalipen.com", "aigc.zjtemplate.com/datenet")
            bak_url = bak_url.replace("upload.dalipen.com", "aigc.zjtemplate.com/upload")
            bak_url = bak_url.replace("api.dalipen.com", "aigc.zjtemplate.com")
            with open(download_file, 'wb+') as f:
                f.write(requests.get(bak_url).content)
        try:
            if os.path.exists(download_file) and os.stat(download_file).st_size > 100:
                if os.path.exists(local_path):
                    shutil.rmtree(local_path)
                os.makedirs(local_path)
                with zipfile.ZipFile(download_file, "r") as zip_ref:
                    zip_ref.extractall(local_path)
                requirements_file = os.path.join(local_path, "requirements.txt")
                if os.path.exists(requirements_file):
                    subprocess.run(f"{pip_cmd} install -r {requirements_file} -i https://pypi.python.org/simple/", 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except Exception as ex:
            print(ex)
        finally:
            if os.path.exists(download_file):
                os.remove(download_file)
        
def widgetUninstall(name, url):
    def find_pip_command():
        possible_pips = ['pip3.11', 'pip', 'pip3']
        for cmd in possible_pips:
            pip_path = shutil.which(cmd)
            if pip_path:
                return cmd

        for version in range(12, 11, 10, 9, 8, 13, -1):
            cmd = f"pip3.{version}"
            pip_path = shutil.which(cmd)
            if pip_path:
                return cmd
                
        raise RuntimeError("No pip command found on the system.")
    if url.endswith(".whl"):
        if name:
            pip_cmd = find_pip_command()
            subprocess.run(f"{pip_cmd} uninstall {name} -y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    elif url.endswith(".zip"):
        local_path = os.path.join(constant.base_path, "widget", name)
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
                
def UpdateWidgetFromPypi():
    _map = store.widgetMap()
    
    # 获取daemon管理器
    daemon_manager_instance = None
    try:
        from ryry.daemon_manager import daemon_manager
        daemon_manager_instance = daemon_manager
    except:
        pass
    
    for it in _map:
        is_block = False
        if isinstance(_map[it], (dict)):
            is_block = _map[it]["isBlock"]
            path = _map[it]["path"]
        else:
            path = _map[it]
        local_path = os.path.dirname(path)
        if is_block == False and os.path.exists(local_path):
            data = GetWidgetConfig(local_path)
            if "name" in data and len(data["name"]) > 0:
                try:
                    py_package = data["name"]
                    local_version = data.get("version", "")
                    widgetid, remote_version, package_url = ryry_webapi.findWidget(py_package)
                    if len(local_version) <= 0:
                        local_version, local_path = _local_package_info(py_package)
                    if len(local_version) <= 0:
                        continue
                    if compare_versions(remote_version, local_version) > 0:
                        print(f"开始更新 {py_package}")
                        # 停止对应的daemon进程
                        if daemon_manager_instance:
                            daemon_status = daemon_manager_instance.get_daemon_status(it)
                            if daemon_status.get("running", False):
                                print(f"Stopping daemon for widget {it} before update...")
                                daemon_manager_instance.stop_daemon(it)
                        
                        #update
                        widgetReInstall(py_package, package_url, local_path)
                        widgetUpdateNotify(py_package, local_version, remote_version)
                        
                        # 如果daemon之前在运行且应该启动，则重启
                        if daemon_manager_instance and daemon_status.get("running", False):
                            if daemon_manager_instance.should_start_daemon(it):
                                print(f"Restarting daemon for widget {it} after update...")
                                widget_info = _map[it] if isinstance(_map[it], dict) else {"path": _map[it]}
                                daemon_manager_instance.start_daemon(it, widget_info)
                        print(f"更新 {py_package} {local_version} -> {remote_version} 完成")
                                
                except Exception as ex:
                    print(ex)
                    continue
    for widget_id, widget_name, remote_version, package_url, is_install in ryry_webapi.getAutoDeployWidget():
        try:
            if widget_id not in _map and is_install:
                local_version, local_path = _local_package_info(widget_name)
                # 安装前无需停止daemon，因为本地没有
                widgetReInstall(widget_name, package_url, local_path)
                widgetInstallNotify(widget_name, remote_version)
                addWidgetToEnv(widget_name)
                print(f"auto install {widget_name}")
                # 安装后如果需要daemon则启动
                try:
                    from ryry.daemon_manager import daemon_manager
                    _map_new = store.widgetMap()
                    if widget_id in _map_new and isinstance(_map_new[widget_id], dict):
                        if daemon_manager.should_start_daemon(widget_id):
                            print(f"Auto starting daemon for widget {widget_id} after install...")
                            daemon_manager.start_daemon(widget_id, _map_new[widget_id])
                except Exception as ex:
                    print(f"Auto start daemon failed: {ex}")
            elif is_install == False and widget_id in _map:
                # 卸载前如果daemon在运行则先停止
                try:
                    from ryry.daemon_manager import daemon_manager
                    daemon_status = daemon_manager.get_daemon_status(widget_id)
                    if daemon_status.get("running", False):
                        print(f"Auto stopping daemon for widget {widget_id} before uninstall...")
                        daemon_manager.stop_daemon(widget_id)
                except Exception as ex:
                    print(f"Auto stop daemon failed: {ex}")
                print(f"auto remove {widget_name}")
                widgetUninstall(widget_name, package_url)
                widgetUninstallNotify(widget_name, remote_version)
                store.removeWidget(widget_id)
        except Exception as ex:
            print(ex)
            continue

def installWidget(name):
    widgetid, remote_version, package_url = ryry_webapi.findWidget(name)
    if len(widgetid) <= 0:
        print(f"{name} 不存在")
        return
    local_version, local_path = _local_package_info(name)
    if compare_versions(remote_version, local_version) > 0:
        #update
        widgetReInstall(name, package_url, local_path)
        widgetInstallNotify(name, remote_version)
        addWidgetToEnv(name, True)
        print(f"成功安装 {name} {remote_version}")
    else:
        print(f"本地已是最新版本 {remote_version}")