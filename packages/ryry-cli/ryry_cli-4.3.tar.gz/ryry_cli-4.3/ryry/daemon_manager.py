import os
import sys
import json
import time
import signal
import subprocess
import threading
from threading import Thread, Lock
from typing import Dict, Optional, Tuple
import queue
import calendar
import uuid

from ryry import constant, store, taskUtils, utils


class DaemonManager:
    """基于文件的常驻进程管理器"""
    
    def __init__(self):
        self.daemon_config_file = os.path.join(constant.base_path, "daemon_processes.json")
        self.lock = Lock()
        self._ensure_config_file()
    
    def _ensure_config_file(self):
        """确保配置文件存在"""
        if not os.path.exists(self.daemon_config_file):
            with open(self.daemon_config_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _read_daemon_config(self) -> dict:
        """读取daemon配置"""
        try:
            with open(self.daemon_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _write_daemon_config(self, config: dict):
        """写入daemon配置"""
        try:
            with open(self.daemon_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            taskUtils.taskPrint(None, f"Write daemon config failed: {e}")
    
    def _is_process_alive(self, pid: int) -> bool:
        """检查进程是否还活着"""
        try:
            if pid <= 0:
                return False
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False
    
    def _send_command_to_process(self, widget_id: str, command: dict, timeout: int = 30) -> Optional[dict]:
        """发送命令到进程"""
        try:
            config = self._read_daemon_config()
            daemon_info = config.get(widget_id, {})
            
            if not daemon_info.get("running", False):
                return None
            
            # 这里可以通过管道、socket等方式与进程通信
            # 为了简化，我们假设进程会创建一个命令文件
            cmd_file = os.path.join(constant.base_path, f"daemon_cmd_{widget_id}.json")
            result_file = os.path.join(constant.base_path, f"daemon_result_{widget_id}.json")
            
            # 清理旧的结果文件
            if os.path.exists(result_file):
                os.remove(result_file)
            
            # 写入命令
            with open(cmd_file, 'w', encoding='utf-8') as f:
                json.dump(command, f)
            
            # 等待结果
            start_time = time.time()
            while time.time() - start_time < timeout:  # 使用传入的timeout
                if os.path.exists(result_file):
                    try:
                        with open(result_file, 'r', encoding='utf-8') as f:
                            response = json.load(f)
                        os.remove(result_file)
                        return response
                    except:
                        pass
                time.sleep(1)
            
            return None
        except Exception as e:
            taskUtils.taskPrint(None, f"Send command to daemon {widget_id} failed: {e}")
            return None
    
    def has_daemon_file(self, widget_id: str) -> bool:
        """检查widget是否有daemon.py文件"""
        try:
            widget_path = self._get_widget_path(widget_id)
            if not widget_path:
                return False
            daemon_file = os.path.join(os.path.dirname(widget_path), "daemon.py")
            return os.path.exists(daemon_file)
        except:
            return False
    
    def is_daemon_enabled(self, widget_id: str) -> bool:
        """检查widget是否启用daemon功能"""
        try:
            widget_config = self._get_widget_config(widget_id)
            if not widget_config:
                return False
            return widget_config.get("daemon_enabled", False)
        except:
            return False
    
    def should_start_daemon(self, widget_id: str) -> bool:
        """判断是否应该启动daemon"""
        return self.has_daemon_file(widget_id) and self.is_daemon_enabled(widget_id)
    
    def _get_widget_config(self, widget_id: str) -> Optional[dict]:
        """获取widget配置"""
        try:
            widget_path = self._get_widget_path(widget_id)
            if not widget_path:
                return None
            
            config_path = os.path.join(os.path.dirname(widget_path), "config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return None
    
    def _get_widget_path(self, widget_id: str) -> Optional[str]:
        """获取widget主文件路径"""
        widget_map = store.widgetMap()
        if widget_id not in widget_map:
            return None
        
        widget_info = widget_map[widget_id]
        if isinstance(widget_info, dict):
            return widget_info["path"]
        else:
            return widget_info
    
    def start_daemon(self, widget_id: str, widget_info: dict = None) -> bool:
        """启动指定widget的常驻进程"""
        with self.lock:
            config = self._read_daemon_config()
            # 检查是否已经在运行
            if widget_id in config:
                daemon_info = config[widget_id]
                if daemon_info.get("running", False) and self._is_process_alive(daemon_info.get("pid", 0)):
                    return True  # 已经在运行
                # 清理无效的进程信息
                del config[widget_id]
                self._write_daemon_config(config)
            if not self.should_start_daemon(widget_id):
                return False
            try:
                widget_path = self._get_widget_path(widget_id)
                if not widget_path:
                    return False
                widget_dir = os.path.dirname(widget_path)
                daemon_file = os.path.join(widget_dir, "daemon.py")
                # 获取widget的timeout配置和version
                if widget_info and isinstance(widget_info, dict):
                    timeout = widget_info.get("timeout", 600)
                    version = widget_info.get("version", "1.0")
                else:
                    widget_config = self._get_widget_config(widget_id)
                    timeout = widget_config.get("timeout", 600) if widget_config else 600
                    version = widget_config.get("version", "1.0") if widget_config else "1.0"
                # 启动进程
                process = subprocess.Popen(
                    [sys.executable, daemon_file, widget_id, constant.base_path],
                    cwd=widget_dir,
                    env=os.environ.copy()
                )
                # 记录进程信息
                daemon_info = {
                    "widget_id": widget_id,
                    "pid": process.pid,
                    "start_time": time.time(),
                    "running": True,
                    "ready": False,
                    "accept_tasks": False,
                    "timeout": timeout,
                    "version": version
                }
                config[widget_id] = daemon_info
                self._write_daemon_config(config)
                # 等待就绪信号（通过文件）
                ready_file = os.path.join(constant.base_path, f"daemon_ready_{widget_id}.json")
                start_time = time.time()
                while time.time() - start_time < 30:  # 30秒超时
                    if os.path.exists(ready_file):
                        try:
                            with open(ready_file, 'r', encoding='utf-8') as f:
                                ready_info = json.load(f)
                            os.remove(ready_file)
                            daemon_info["ready"] = True
                            daemon_info["accept_tasks"] = ready_info.get("accept_tasks", False)
                            config[widget_id] = daemon_info
                            self._write_daemon_config(config)
                            break
                        except:
                            pass
                    time.sleep(1)
                if not daemon_info["ready"]:
                    process.terminate()
                    del config[widget_id]
                    self._write_daemon_config(config)
                    return False
                taskUtils.taskPrint(None, f"Daemon process {widget_id} started, PID: {process.pid}, accept_tasks: {daemon_info['accept_tasks']}")
                return True
            except Exception as e:
                taskUtils.taskPrint(None, f"Start daemon process {widget_id} failed: {e}")
                return False

    def stop_daemon(self, widget_id: str) -> bool:
        """停止指定widget的常驻进程"""
        with self.lock:
            config = self._read_daemon_config()
            
            if widget_id not in config:
                return True  # 已经停止
            
            daemon_info = config[widget_id]
            pid = daemon_info.get("pid", 0)
            
            if not self._is_process_alive(pid):
                del config[widget_id]
                self._write_daemon_config(config)
                return True
            
            try:
                # 发送停止命令
                response = self._send_command_to_process(widget_id, {"type": "stop"}, 600)
                if response and response.get("type") == "stop_result":
                    # 等待进程结束
                    start_time = time.time()
                    while time.time() - start_time < 30:  # 30秒超时
                        if not self._is_process_alive(pid):
                            break
                        time.sleep(1)
                
                # 如果进程还在运行，强制终止
                if self._is_process_alive(pid):
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(2)
                    if self._is_process_alive(pid):
                        os.kill(pid, signal.SIGKILL)
                
                del config[widget_id]
                self._write_daemon_config(config)
                taskUtils.taskPrint(None, f"Daemon process {widget_id} stopped")
                return True
                
            except Exception as e:
                taskUtils.taskPrint(None, f"Stop daemon {widget_id} failed: {e}")
                return False
    
    def execute_task(self, widget_id: str, task_data: dict, timeout: int = 600) -> Tuple[bool, str, dict]:
        """在常驻进程中执行任务"""
        config = self._read_daemon_config()
        daemon_info = config.get(widget_id, {})
        
        if not daemon_info.get("running", False):
            return False, "Daemon process not running", {}
        
        if not self._is_process_alive(daemon_info.get("pid", 0)):
            # 清理无效进程
            with self.lock:
                config = self._read_daemon_config()
                if widget_id in config:
                    del config[widget_id]
                    self._write_daemon_config(config)
            return False, "Daemon process is dead", {}
        
        if not daemon_info.get("accept_tasks", False):
            return False, "Daemon process does not accept tasks", {}
        
        try:
            # 生成任务ID
            task_id = str(uuid.uuid4())
            
            # 发送任务到进程
            task_request = {
                "type": "task",
                "task_id": task_id,
                "data": task_data,
                "timeout": timeout
            }
            
            response = self._send_command_to_process(widget_id, task_request, timeout)
            if response and response.get("type") == "task_result":
                success = response.get("success", False)
                data = response.get("data", {})
                error = response.get("error", "")
                return success, error, data
            
            return False, "No response from daemon", {}
            
        except Exception as e:
            return False, f"Execute task failed: {str(e)}", {}
    
    def get_daemon_status(self, widget_id: str) -> dict:
        """获取常驻进程状态"""
        config = self._read_daemon_config()
        daemon_info = config.get(widget_id, {})
        
        if not daemon_info:
            return {"running": False, "ready": False, "accept_tasks": False}
        
        running = daemon_info.get("running", False) and self._is_process_alive(daemon_info.get("pid", 0))
        
        if not running and daemon_info.get("running", False):
            # 清理无效进程
            with self.lock:
                config = self._read_daemon_config()
                if widget_id in config:
                    del config[widget_id]
                    self._write_daemon_config(config)
        
        return {
            "running": running,
            "ready": daemon_info.get("ready", False),
            "accept_tasks": daemon_info.get("accept_tasks", False),
            "pid": daemon_info.get("pid", 0),
            "start_time": daemon_info.get("start_time", 0)
        }
    
    def stop_all_daemons(self) -> bool:
        """停止所有常驻进程"""
        config = self._read_daemon_config()
        widget_ids = list(config.keys())
        
        all_stopped = True
        for widget_id in widget_ids:
            if not self.stop_daemon(widget_id):
                all_stopped = False
        
        return all_stopped
    
    def sync_daemons_with_widget_map(self):
        """同步daemon状态与widgetMap，自动关闭不需要的daemon，启动需要的新daemon"""
        config = self._read_daemon_config()
        widget_map = store.widgetMap()
        # 1. 关闭不需要的daemon（被移除、被屏蔽、版本不一致）
        for widget_id in list(config.keys()):
            daemon_info = config[widget_id]
            widget_info = widget_map.get(widget_id)
            need_stop = False
            # widget已被移除
            if widget_info is None:
                need_stop = True
            else:
                # 屏蔽
                is_block = widget_info.get("isBlock", False)
                if is_block:
                    need_stop = True
                # 版本号不一致（仅当daemon正在运行时才判断）
                version = widget_info.get("version", "1.0")
                daemon_version = daemon_info.get("version", None)
                if daemon_info.get("running", False) and daemon_version is not None and daemon_version != version:
                    need_stop = True
            if need_stop:
                self.stop_daemon(widget_id)
        # 2. 启动需要的daemon（未运行、或因上述原因被重启）
        for widget_id, widget_info in widget_map.items():
            is_block = widget_info.get("isBlock", False)
            version = widget_info.get("version", "1.0")
            if not is_block and self.should_start_daemon(widget_id):
                status = self.get_daemon_status(widget_id)
                daemon_info = config.get(widget_id)
                # 未运行 或 版本号不一致（仅当daemon正在运行时才判断）
                if (not status.get("running", False)) or (daemon_info and daemon_info.get("running", False) and daemon_info.get("version", None) != version):
                    self.start_daemon(widget_id, widget_info)

    # 建议在start_all_daemons后调用一次同步
    def start_all_daemons(self):
        """启动所有应该启动的常驻进程"""
        widget_map = store.widgetMap()
        for widget_id in widget_map:
            widget_info = widget_map[widget_id]
            if self.should_start_daemon(widget_id) and not widget_info.get("isBlock", False):
                self.start_daemon(widget_id, widget_info)


# 创建全局实例
daemon_manager = DaemonManager() 