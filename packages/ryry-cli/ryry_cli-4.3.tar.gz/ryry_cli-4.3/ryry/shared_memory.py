import os
import json
import time
import threading
import tempfile
import platform
import subprocess
from threading import Lock
from typing import Optional, Dict, Any
from pathlib import Path
import psutil
import sys

# 跨平台文件锁支持
try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False
    if platform.system() == 'Windows':
        import msvcrt
    else:
        import fcntl

class SharedMemoryService:
    """基于文件系统的轻量级共享内存服务"""
    
    def __init__(self):
        self.service_name = "widget_power"
        # 使用系统推荐目录，确保多进程共享
        self.data_dir = self._get_system_shared_dir()
        self.data_file = os.path.join(self.data_dir, f"{self.service_name}.json")
        self.lock_file = os.path.join(self.data_dir, f"{self.service_name}.lock")
        self.process_count_file = os.path.join(self.data_dir, f"{self.service_name}_process_count.json")
        self.process_count_lock_file = self.process_count_file + '.lock'
        self.current_service_name = os.path.basename(sys.argv[0])
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 增加启动标志位，避免重复初始化
        self._started = False
    
    def _get_system_shared_dir(self) -> str:
        """获取系统推荐的共享目录"""
        system = platform.system()
        
        if system == 'Windows':
            # Windows: 使用 %TEMP% 或 %LOCALAPPDATA%
            temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or os.path.expanduser('~\\AppData\\Local\\Temp')
            return os.path.join(temp_dir, 'widget_shared_memory')
        
        elif system == 'Darwin':  # macOS
            # macOS: 使用 /tmp 或 ~/Library/Caches
            cache_dir = os.path.expanduser('~/Library/Caches')
            return os.path.join(cache_dir, 'widget_shared_memory')
        
        else:  # Linux 和其他 Unix-like 系统
            # Linux: 使用 /tmp 或 /var/tmp
            return '/tmp/widget_shared_memory'
    
    def _acquire_shared_lock(self, file_obj):
        """获取共享锁（跨平台）"""
        if HAS_PORTALOCKER:
            # 使用portalocker（推荐）
            portalocker.lock(file_obj, portalocker.LOCK_SH)
        elif platform.system() == 'Windows':
            # Windows使用msvcrt.locking
            msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
        else:
            # Unix-like系统使用fcntl
            fcntl.flock(file_obj.fileno(), fcntl.LOCK_SH)
    
    def _acquire_exclusive_lock(self, file_obj):
        """获取独占锁（跨平台）"""
        if HAS_PORTALOCKER:
            # 使用portalocker（推荐）
            portalocker.lock(file_obj, portalocker.LOCK_EX)
        elif platform.system() == 'Windows':
            # Windows使用msvcrt.locking
            msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
        else:
            # Unix-like系统使用fcntl
            fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)
    
    def _release_lock(self, file_obj):
        """释放锁（跨平台）"""
        if HAS_PORTALOCKER:
            # 使用portalocker（推荐）
            portalocker.unlock(file_obj)
        elif platform.system() == 'Windows':
            # Windows使用msvcrt.locking
            msvcrt.locking(file_obj.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            # Unix-like系统使用fcntl
            fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
    
    def _register_process(self):
        """注册当前进程（带防呆机制）"""
        current_pid = os.getpid()
        current_time = time.time()
        
        def operation(data):
            # 验证数据完整性
            if not self._validate_process_data(data):
                data = {"processes": {}}
            
            # 清理死亡进程（只清理本服务的）
            self._cleanup_dead_processes_internal(data, current_time, skip_pid=current_pid)
            
            # 检查当前进程是否已经注册
            if str(current_pid) in data["processes"]:
                data["processes"][str(current_pid)]["last_heartbeat"] = current_time
            else:
                # 注册新进程，带service_name
                data["processes"][str(current_pid)] = {
                    "start_time": current_time,
                    "last_heartbeat": current_time,
                    "service_name": self.current_service_name
                }
            
            return len(data["processes"])
        
        # 原子性地注册进程
        with open(self.process_count_lock_file, 'w') as lock_f:
            self._acquire_exclusive_lock(lock_f)
            try:
                if os.path.exists(self.process_count_file):
                    try:
                        with open(self.process_count_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                        data = {"processes": {}}
                else:
                    data = {"processes": {}}
                
                process_count = operation(data)
                
                # 检查清理后是否只剩下当前进程（说明没有其他进程了）
                remaining_processes = [pid for pid in data["processes"].keys() if pid != str(current_pid)]
                if len(remaining_processes) == 0 and process_count == 1:
                    self._reset_all_files()
                    # 重新注册当前进程
                    data = {"processes": {}}
                    data["processes"][str(current_pid)] = {
                        "start_time": current_time,
                        "last_heartbeat": current_time,
                        "service_name": self.current_service_name
                    }
                    process_count = 1
                
                with open(self.process_count_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                return process_count
            finally:
                self._release_lock(lock_f)
    
    def _cleanup_dead_processes_internal(self, data: dict, current_time: float, skip_pid=None):
        """内部清理死亡进程（不涉及文件操作）"""
        timeout = 30  # 30秒超时
        
        if "processes" not in data:
            return
        
        dead_processes = []
        for pid_str, info in list(data["processes"].items()):
            try:
                pid = int(pid_str)
                
                if skip_pid is not None and pid == skip_pid:
                    continue  # 跳过当前进程
                
                # 只清理本服务的进程
                if info.get("service_name") != self.current_service_name:
                    continue

                # 检测1: 检查进程是否真的存在
                if not self._is_process_alive(pid):
                    dead_processes.append(pid_str)
                    continue
                
            except (ValueError, TypeError):
                dead_processes.append(pid_str)
                continue
        
        for pid_str in dead_processes:
            del data["processes"][pid_str]
        
        if dead_processes:
            pass
    
    def _unregister_process(self):
        """注销当前进程（带防呆机制）"""
        current_pid = os.getpid()
        current_time = time.time()
        
        def operation(data):
            # 验证数据完整性
            if not self._validate_process_data(data):
                return 0
            
            # 清理死亡进程（只清理本服务的）
            self._cleanup_dead_processes_internal(data, current_time, skip_pid=current_pid)
            
            # 注销当前进程（只注销本服务的）
            if str(current_pid) in data["processes"] and data["processes"][str(current_pid)].get("service_name") == self.current_service_name:
                del data["processes"][str(current_pid)]
            
            return len(data["processes"])
        
        # 原子性地注销进程
        with open(self.process_count_lock_file, 'w') as lock_f:
            self._acquire_exclusive_lock(lock_f)
            try:
                if os.path.exists(self.process_count_file):
                    try:
                        with open(self.process_count_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                        return 0
                    
                    remaining_processes = operation(data)
                    
                    with open(self.process_count_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    return remaining_processes
                else:
                    return 0
            finally:
                self._release_lock(lock_f)
    
    def _get_process_count(self) -> int:
        """获取当前进程数（带防呆机制）"""
        try:
            if os.path.exists(self.process_count_file):
                try:
                    with open(self.process_count_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                    return 0
                
                # 验证数据完整性
                if not self._validate_process_data(data):
                    return 0
                
                # 清理死亡进程
                with open(self.process_count_lock_file, 'w') as lock_f:
                    self._acquire_exclusive_lock(lock_f)
                    try:
                        self._cleanup_dead_processes_internal(data, time.time())
                        with open(self.process_count_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                    finally:
                        self._release_lock(lock_f)
                return len(data.get("processes", {}))
            else:
                return 0
        except Exception as e:
            return 0
    
    def _cleanup_dead_processes(self):
        """清理已死亡的进程（仅依靠pid存在性检测）"""
        
        def operation(data):
            if "processes" not in data:
                return 0
            
            dead_processes = []
            for pid_str, info in data["processes"].items():
                try:
                    pid = int(pid_str)
                    
                    # 检测1: 检查进程是否真的存在
                    if not self._is_process_alive(pid):
                        dead_processes.append(pid_str)
                        continue
                    
                except (ValueError, TypeError):
                    # PID格式错误，直接清理
                    dead_processes.append(pid_str)
                    continue
            
            for pid_str in dead_processes:
                del data["processes"][pid_str]
            
            if dead_processes:
                pass
            
            return len(data["processes"])
        
        # 原子性地清理死亡进程
        with open(self.process_count_lock_file, 'w') as lock_f:
            self._acquire_exclusive_lock(lock_f)
            try:
                if os.path.exists(self.process_count_file):
                    try:
                        with open(self.process_count_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                        data = {"processes": {}}
                    
                    remaining_processes = operation(data)
                    
                    with open(self.process_count_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    return remaining_processes
                else:
                    return 0
            finally:
                self._release_lock(lock_f)
    
    def _is_process_alive(self, pid: int) -> bool:
        """使用psutil跨平台判断进程是否存活"""
        try:
            return psutil.pid_exists(pid)
        except Exception as e:
            return False
    
    def _validate_process_data(self, data: dict) -> bool:
        """验证进程数据的完整性"""
        try:
            if not isinstance(data, dict):
                return False
            
            if "processes" not in data:
                return False
            
            processes = data["processes"]
            if not isinstance(processes, dict):
                return False
            
            for pid_str, info in processes.items():
                # 检查PID格式
                try:
                    pid = int(pid_str)
                    if pid <= 0:
                        return False
                except (ValueError, TypeError):
                    return False
                
                # 检查info结构
                if not isinstance(info, dict):
                    return False
                
                # 检查必要字段
                required_fields = ["start_time", "last_heartbeat", "service_name"]
                for field in required_fields:
                    if field not in info:
                        return False
                    if field in ["start_time", "last_heartbeat"] and not isinstance(info[field], (int, float)):
                        return False
                    if field == "service_name" and not isinstance(info[field], str):
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _update_heartbeat(self):
        """更新当前进程的心跳（简化版，仅保持数据结构一致性）"""
        current_pid = os.getpid()
        current_time = time.time()
        
        def operation(data):
            if "processes" in data and str(current_pid) in data["processes"]:
                data["processes"][str(current_pid)]["last_heartbeat"] = current_time
            return len(data.get("processes", {}))
        
        # 原子性地更新心跳
        with open(self.process_count_lock_file, 'w') as lock_f:
            self._acquire_exclusive_lock(lock_f)
            try:
                if os.path.exists(self.process_count_file):
                    try:
                        with open(self.process_count_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                        data = {"processes": {}}
                    
                    operation(data)
                    
                    with open(self.process_count_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._release_lock(lock_f)
    
    def _init_data_file(self):
        """初始化数据文件（只在第一个进程时执行）"""
        try:
            # 清理死亡进程
            self._cleanup_dead_processes()
            
            # 获取当前进程数
            process_count = self._get_process_count()
            
            # 如果是第一个进程，初始化数据文件
            if process_count == 1 and not os.path.exists(self.data_file):
                initial_data = {
                    "max_counter": 999,
                    "cur_counter": 0,
                    "widget_power": {},
                    "last_update": time.time(),
                    "created_by_pid": os.getpid(),
                    "created_time": time.time()
                }
                self._write_data(initial_data)
        except Exception as e:
            # 如果初始化失败，尝试清理并重新开始
            try:
                self.emergency_cleanup()
            except:
                pass
    
    def _read_data(self) -> Dict[str, Any]:
        """读取数据文件"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # 跨平台文件锁读取
                self._acquire_shared_lock(f)
                try:
                    data = json.load(f)
                finally:
                    self._release_lock(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或损坏，返回默认数据
            return {
                "max_counter": 999,
                "cur_counter": 0,
                "widget_power": {},
                "last_update": time.time()
            }
    
    def _write_data(self, data: Dict[str, Any]):
        """写入数据文件"""
        data["last_update"] = time.time()
        
        # 创建临时文件
        temp_file = f"{self.data_file}.tmp"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # 确保数据写入磁盘
            
            # 原子性地替换文件
            os.replace(temp_file, self.data_file)
        except Exception as e:
            # 清理临时文件
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            raise e
    
    def _atomic_operation(self, operation):
        """执行原子操作（多进程安全）"""
        # 使用文件锁确保多进程间的原子性
        with open(self.lock_file, 'w') as lock_f:
            # 获取独占锁，阻塞直到获得锁
            self._acquire_exclusive_lock(lock_f)
            try:
                data = self._read_data()
                result = operation(data)
                self._write_data(data)
                return result
            finally:
                self._release_lock(lock_f)
    
    def start_service(self):
        """启动共享内存服务（轻量级，无需额外进程）"""
        if self._started:
            # 如果已经启动，只更新心跳
            self._update_heartbeat()
            return 0
        
        # 注册当前进程
        self._register_process()
        
        # 初始化数据文件（如果是第一个进程）
        self._init_data_file()
        
        # 标记为已启动
        self._started = True
        
        # 更新心跳
        self._update_heartbeat()
        return 0  # 返回0表示使用文件系统模式
    
    def stop_service(self):
        """停止共享内存服务"""
        # 注销当前进程
        remaining_processes = self._unregister_process()
        
        # 统计所有服务的主服务进程数
        total_main_proc_count = 0
        current_service_proc_count = 0
        
        if os.path.exists(self.process_count_file):
            try:
                with open(self.process_count_file, 'r', encoding='utf-8') as f:
                    pdata = json.load(f)
                for pid, info in pdata.get("processes", {}).items():
                    service_name = info.get("service_name", "")
                    if service_name:  # 只统计有service_name的进程
                        total_main_proc_count += 1
                        if service_name == self.current_service_name:
                            current_service_proc_count += 1
            except Exception as e:
                pass
        
        # 只有当所有服务都没有进程时，才清理共享数据
        if total_main_proc_count == 0:
            self.clear_all_data()
            # 清理进程计数文件
            try:
                if os.path.exists(self.process_count_file):
                    os.remove(self.process_count_file)
            except:
                pass
            # 删除widget_power.json
            try:
                if os.path.exists(self.data_file):
                    os.remove(self.data_file)
            except Exception as e:
                pass
    
    def set_max_counter(self, max_counter: int):
        """设置最大计数器，如果传入的max_counter更小则覆盖"""
        def operation(data):
            old_max = data.get("max_counter", 999)
            if max_counter < old_max:
                data["max_counter"] = max_counter
            return data["max_counter"]
        return self._atomic_operation(operation)
    
    def get_max_counter(self) -> int:
        """获取最大计数器（只读操作）"""
        data = self._read_data()
        return data.get("max_counter", 1)
    
    def set_cur_counter(self, cur_counter: int):
        """设置当前计数器"""
        def operation(data):
            data["cur_counter"] = cur_counter
            return cur_counter
        return self._atomic_operation(operation)
    
    def get_cur_counter(self) -> int:
        """获取当前计数器（只读操作）"""
        data = self._read_data()
        return data.get("cur_counter", 0)
    
    def increment_cur_counter(self) -> int:
        """增加当前计数器"""
        def operation(data):
            data["cur_counter"] = data.get("cur_counter", 0) + 1
            return data["cur_counter"]
        return self._atomic_operation(operation)
    
    def decrement_cur_counter(self) -> int:
        """减少当前计数器"""
        def operation(data):
            data["cur_counter"] = max(0, data.get("cur_counter", 0) - 1)
            return data["cur_counter"]
        return self._atomic_operation(operation)
    
    def set_widget_power(self, widget_id: str, max_task_number: int, cur_task_number: int = 0):
        """设置widget power"""
        def operation(data):
            if "widget_power" not in data:
                data["widget_power"] = {}
            data["widget_power"][widget_id] = {
                "max": max_task_number,
                "cur": cur_task_number
            }
            return data["widget_power"][widget_id]
        return self._atomic_operation(operation)
    
    def get_widget_power(self, widget_id: str) -> Optional[Dict[str, int]]:
        """获取widget power（只读操作）"""
        data = self._read_data()
        return data.get("widget_power", {}).get(widget_id)
    
    def increment_widget_cur_power(self, widget_id: str) -> int:
        """增加widget当前power"""
        def operation(data):
            if "widget_power" not in data:
                data["widget_power"] = {}
            if widget_id not in data["widget_power"]:
                data["widget_power"][widget_id] = {"max": 0, "cur": 0}
            
            data["widget_power"][widget_id]["cur"] += 1
            return data["widget_power"][widget_id]["cur"]
        return self._atomic_operation(operation)
    
    def decrement_widget_cur_power(self, widget_id: str) -> int:
        """减少widget当前power"""
        def operation(data):
            if "widget_power" not in data:
                data["widget_power"] = {}
            if widget_id not in data["widget_power"]:
                data["widget_power"][widget_id] = {"max": 0, "cur": 0}
            
            data["widget_power"][widget_id]["cur"] = max(0, data["widget_power"][widget_id]["cur"] - 1)
            return data["widget_power"][widget_id]["cur"]
        return self._atomic_operation(operation)
    
    def get_all_widget_power(self) -> Dict[str, Dict[str, int]]:
        """获取所有widget power（只读操作）"""
        data = self._read_data()
        return data.get("widget_power", {}).copy()
    
    def clear_all_data(self):
        """清除所有数据"""
        initial_data = {
            "max_counter": 1,
            "cur_counter": 0,
            "widget_power": {},
            "last_update": time.time()
        }
        self._write_data(initial_data)
    
    def get_service_info(self) -> Dict[str, Any]:
        """获取服务信息"""
        data = self._read_data()
        return {
            "service_type": "file_based",
            "data_dir": self.data_dir,
            "data_file": self.data_file,
            "lock_file": self.lock_file,
            "platform": platform.system(),
            "last_update": data.get("last_update", 0),
            "max_counter": data.get("max_counter", 1),
            "cur_counter": data.get("cur_counter", 0),
            "widget_count": len(data.get("widget_power", {}))
        }
    
    def get_shared_dir_info(self) -> Dict[str, Any]:
        """获取共享目录信息"""
        return {
            "platform": platform.system(),
            "shared_dir": self.data_dir,
            "data_file": self.data_file,
            "lock_file": self.lock_file,
            "process_count_file": self.process_count_file,
            "data_file_exists": os.path.exists(self.data_file),
            "lock_file_exists": os.path.exists(self.lock_file),
            "process_count_file_exists": os.path.exists(self.process_count_file),
            "dir_exists": os.path.exists(self.data_dir)
        }
    
    def get_process_info(self) -> Dict[str, Any]:
        """获取进程信息（带防呆机制）"""
        try:
            if os.path.exists(self.process_count_file):
                try:
                    with open(self.process_count_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
                    return {
                        "current_pid": os.getpid(),
                        "total_processes": 0,
                        "processes": {},
                        "is_first_process": True,
                        "data_valid": False
                    }
                
                # 验证数据完整性
                if not self._validate_process_data(data):
                    return {
                        "current_pid": os.getpid(),
                        "total_processes": 0,
                        "processes": {},
                        "is_first_process": True,
                        "data_valid": False
                    }
                
                # 清理死亡进程
                self._cleanup_dead_processes_internal(data, time.time())
                
                return {
                    "current_pid": os.getpid(),
                    "total_processes": len(data.get("processes", {})),
                    "processes": data.get("processes", {}),
                    "is_first_process": len(data.get("processes", {})) == 1,
                    "data_valid": True
                }
            else:
                return {
                    "current_pid": os.getpid(),
                    "total_processes": 0,
                    "processes": {},
                    "is_first_process": True,
                    "data_valid": True
                }
        except Exception as e:
            return {
                "current_pid": os.getpid(),
                "total_processes": 0,
                "processes": {},
                "is_first_process": True,
                "data_valid": False
            }
    
    def force_cleanup_dead_processes(self) -> int:
        """强制清理死亡进程（手动调用）"""
        return self._cleanup_dead_processes()
    
    def reset_process_count_file(self):
        """重置进程计数文件（紧急情况使用）"""
        try:
            if os.path.exists(self.process_count_file):
                os.remove(self.process_count_file)
        except Exception as e:
            pass
    
    def _reset_all_files(self):
        """重置所有相关文件"""
        try:
            # 重置数据文件
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            
            # 重置进程计数文件
            if os.path.exists(self.process_count_file):
                os.remove(self.process_count_file)
            
            # 重置锁文件
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except Exception as e:
            pass
    
    def emergency_cleanup(self):
        """紧急清理（清理所有文件）"""
        try:
            # 清理数据文件
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            
            # 清理进程计数文件
            if os.path.exists(self.process_count_file):
                os.remove(self.process_count_file)
            
            # 清理锁文件
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except Exception as e:
            pass

shared_memory_service = SharedMemoryService()
