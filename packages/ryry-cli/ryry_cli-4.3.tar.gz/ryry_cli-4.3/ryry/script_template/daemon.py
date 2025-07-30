##################################################
# 常驻进程模板 - 继承自ryry.daemon_base.DaemonBase
# 你只需实现自己的业务逻辑方法：
#   - initialize(self): 进程启动时自动调用（可做初始化）
#   - process_task(self, task_data, timeout=None): 收到短链任务时自动调用
#   - loop_function(self): 每秒自动调用一次（可做定时任务）
#   - on_stop(self): 进程退出前自动调用（可做清理）
# 其余生命周期、通信、配置、日志等已由父类统一处理。
##################################################
from ryry.daemon_base import DaemonBase
import sys

class MyWidgetDaemon(DaemonBase):
    def initialize(self):
        """
        进程启动时自动调用（只调用一次）。
        你可以在这里加载模型、初始化数据库、准备资源等。
        """
        # 例如：self.accept_tasks = True  # 如果你希望支持短链任务
        pass

    def process_task(self, task_data, timeout=None):
        """
        收到短链任务时自动调用。
        task_data: 任务参数（dict）
        timeout: 超时时间（秒）
        返回值：dict，格式如下：
            {
                "result": [...],  # 结果数据
                "status": 0,      # 0表示成功，非0表示失败
                "message": ""     # 消息
            }
        """
        # 这里写你的任务处理逻辑
        return {
            "result": [{"type": "text", "content": [f"Processed: {task_data}"]}],
            "status": 0,
            "message": "Success"
        }

    def loop_function(self):
        """
        每秒自动调用一次（定时任务/心跳/后台维护等可写这里）。
        你可以在这里做周期性检查、缓存刷新等。
        """
        pass

    def on_stop(self):
        """
        进程退出前自动调用（只调用一次）。
        你可以在这里保存状态、关闭连接、清理资源等。
        """
        pass

if __name__ == "__main__":
    widget_id = sys.argv[1]
    daemon = MyWidgetDaemon(widget_id)
    print(f"【{daemon.widget_name}后台进程】启动", file=sys.stderr)
    daemon.run() 