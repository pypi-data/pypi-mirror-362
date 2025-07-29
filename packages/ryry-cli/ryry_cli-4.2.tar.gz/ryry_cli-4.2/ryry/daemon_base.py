import sys
import os
import json
import time
from threading import Event

DEFAULT_ACCEPT_TASKS = False  # 默认是否接受短链任务

class DaemonBase:
    def __init__(self, widget_id: str):
        self.widget_id = widget_id
        self.running = True
        self.stop_event = Event()
        self.accept_tasks = self.default_accept_tasks()
        self.widget_name = "???"
        # 获取子类文件（即实际widget的daemon.py）所在目录
        self._script_path = os.path.abspath(sys.modules[self.__class__.__module__].__file__)
        self.base_path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.ryry")
        config_path = os.path.join(os.path.dirname(self._script_path), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.timeout = config.get("timeout", 600)
                    self.widget_name = config.get("name", self.widget_name)
            except:
                self.timeout = 600
        else:
            self.timeout = 600

    def default_accept_tasks(self):
        return DEFAULT_ACCEPT_TASKS

    def initialize(self):
        pass

    def process_task(self, task_data, timeout=None):
        raise NotImplementedError("process_task必须由子类实现")

    def on_stop(self):
        pass

    def health_check(self):
        return {
            "healthy": True,
            "accept_tasks": self.accept_tasks,
            "timestamp": time.time()
        }

    def loop_function(self):
        pass

    def _send_ready_signal(self):
        try:
            ready_file = os.path.join(self.base_path, f"daemon_ready_{self.widget_id}.json")
            with open(ready_file, 'w', encoding='utf-8') as f:
                json.dump({"accept_tasks": self.accept_tasks}, f)
        except Exception as e:
            print(f"Failed to send ready signal: {e}", file=sys.stderr)

    def _send_response(self, response):
        try:
            result_file = os.path.join(self.base_path, f"daemon_result_{self.widget_id}.json")
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(response, f)
        except Exception as e:
            print(f"Failed to send response: {e}", file=sys.stderr)

    def _process_command(self, command):
        cmd_type = command.get("type")
        if cmd_type == "task":
            task_data = command.get("data", {})
            timeout = command.get("timeout", self.timeout)
            try:
                result = self.process_task(task_data, timeout)
                self._send_response({
                    "type": "task_result",
                    "task_id": command.get("task_id"),
                    "success": True,
                    "data": result
                })
            except Exception as e:
                self._send_response({
                    "type": "task_result", 
                    "task_id": command.get("task_id"),
                    "success": False,
                    "error": str(e),
                    "data": {"result": [], "status": 1, "message": str(e)}
                })
        elif cmd_type == "health":
            health = self.health_check()
            self._send_response({
                "type": "health_result",
                "data": health
            })
        elif cmd_type == "stop":
            print(f"【{self.widget_name}后台进程】Received stop command", file=sys.stderr)
            self.running = False
            self.stop_event.set()
            self._send_response({
                "type": "stop_result",
                "success": True
            })

    def run(self):
        try:
            self.initialize()
            self._send_ready_signal()
            cmd_file = os.path.join(self.base_path, f"daemon_cmd_{self.widget_id}.json")
            while self.running:
                try:
                    if os.path.exists(cmd_file):
                        try:
                            with open(cmd_file, 'r', encoding='utf-8') as f:
                                command = json.load(f)
                            os.remove(cmd_file)
                            self._process_command(command)
                        except Exception as e:
                            print(f"Error processing command: {e}", file=sys.stderr)
                    if self.stop_event.is_set():
                        break
                    self.loop_function()
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error in main loop: {e}", file=sys.stderr)
                    time.sleep(1)
        finally:
            self.on_stop()
            print(f"【{self.widget_name}】已终止", file=sys.stderr) 