import sys, os, urllib3, time, platform, json

from ryry import utils
from ryry import ryry_service
from ryry import ryry_widget
from ryry import store
from ryry import utils
from ryry import taskUtils

ll = 29
def scr_str(s):
    return "| " + s + " |"
def scr_str1(s):
    return "| " + s
def scr_line(s):
    return "|" + s + "|"

def service_status(stdscr, idx):
    def real_stdsrc(*args):
        if platform.system() == 'Windows':
            print(args[2])
        else:
            stdscr.addstr(*args)
    if platform.system() != 'Windows':
        real_stdsrc(idx, 0, scr_str("Processing".ljust(ll*3-2)))
        idx+=1
    def running_task_uuids():
        lst = []
        if os.path.exists(taskUtils.task_config_file):
            with open(taskUtils.task_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            infos = ""
            for it in data:
                if it not in ["last_task_pts"]:
                    lst.append(it)
        return lst
    lst = running_task_uuids()
    for d in range(0, max([len(lst)])):
        def widget_stdscr(this_d, this_lst, row_idx, col_idx, append_str):
            if this_d < len(this_lst):
                real_s = this_lst[this_d]
                if len(append_str) > 0:
                    real_s += f" [{append_str}]"
                real_stdsrc(row_idx, col_idx, scr_str(" " + real_s.ljust(ll*2-1)))
            else:
                real_stdsrc(row_idx, col_idx, scr_str(" " + " ".ljust(ll*2-1)))
        widget_stdscr(d, lst, idx, 0, "task" if platform.system() == 'Windows' else "")
        idx+=1
    return idx

def device_status(stdscr, idx):
    def real_stdsrc(*args):
        if platform.system() == 'Windows':
            print(args[2])
        else:
            stdscr.addstr(*args)
    import psutil
    import GPUtil
    cpu_load = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_load = mem.percent
    gpu_list = GPUtil.getGPUs()
    if len(gpu_list) > 0:
        gpu_load = gpu_list[0].load * 100  # 只考虑第一块显卡
    else:
        gpu_load = 0
    real_stdsrc(idx, 0, scr_str(f"Device Usage   |   CPU : {cpu_load}%   |   Memory : {mem_load}%   |   GPU : {gpu_load}%".ljust(ll*3-2)))
    idx+=1
    return idx

def widget_status(stdscr, idx):
    def real_stdsrc(*args):
        if platform.system() == 'Windows':
            print(args[2])
        else:
            stdscr.addstr(*args)
    real_stdsrc(idx, 0, scr_str("Widget List".ljust(ll*3-2)))
    idx+=1
    widget_map = store.widgetMap()
    if len(widget_map) == 0:
        real_stdsrc(idx, 0, scr_str("empty".ljust(ll*3-2)))
        idx+=1
        return idx
    
    # 获取daemon状态
    try:
        from ryry.daemon_manager import daemon_manager
        daemon_statuses = {}
        for widget_id in widget_map:
            daemon_statuses[widget_id] = daemon_manager.get_daemon_status(widget_id)
    except:
        daemon_statuses = {}
    
    maxJust = 10
    for it in widget_map:
        if len(it) > maxJust:
            maxJust = len(it)
    maxJust += 5
    for it in widget_map:
        path = widget_map[it]["path"]
        is_block = widget_map[it]["isBlock"]
        name = widget_map[it]["name"]
        version = widget_map[it].get("version", "1.0")
        max_task_number = widget_map[it].get("max_task_number", 1)
        timeout = widget_map[it].get("timeout", 600)
        end_args = ""
        if is_block:
            end_args = "[X]"
        
        # 检查daemon状态
        daemon_status = daemon_statuses.get(it, {})
        if daemon_status.get("running", False):
            if daemon_status.get("accept_tasks", False):
                end_args += "[D]"  # 运行中且接受任务
            else:
                end_args += "[D-]" # 运行中但不接受任务
        elif daemon_manager and daemon_manager.should_start_daemon(it):
            end_args += "[d]"  # 应该启动但未运行
        
        max_task_number_str = ""
        if max_task_number > 0:
            max_task_number_str = f"*{max_task_number}"
        real_stdsrc(idx, 0, scr_str(f'{f"[{name}{max_task_number_str} v{version}] {it}{end_args} OOT:{timeout}s".ljust(maxJust)}'.ljust(ll*3-2)))
        idx+=1
        real_stdsrc(idx, 0, scr_str(f'  PATH:{path}'.ljust(ll*3-2)))
        idx+=1
        real_stdsrc(idx, 0, scr_str(f' '.ljust(ll*3-2)))
        idx+=1
    return idx

def status():
    from pkg_resources import parse_version, get_distribution
    ver = get_distribution("ryry-cli").version
    deviceid = utils.generate_unique_id()
    import socket
    machine_name = socket.gethostname()
    service = ryry_service.ryryService()
    thread_num = store.get_multithread()
    def get_shared_memory_max_counter():
        # 获取系统推荐的共享目录
        system = platform.system()
        if system == 'Windows':
            temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or os.path.expanduser('~\\AppData\\Local\\Temp')
            data_dir = os.path.join(temp_dir, 'widget_shared_memory')
        elif system == 'Darwin':
            cache_dir = os.path.expanduser('~/Library/Caches')
            data_dir = os.path.join(cache_dir, 'widget_shared_memory')
        else:
            data_dir = '/tmp/widget_shared_memory'
        data_file = os.path.join(data_dir, 'widget_power.json')
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('max_counter', None)
        except Exception:
            return None
    shared_max_counter = get_shared_memory_max_counter()
    shared_max_counter_str = ""
    if shared_max_counter and shared_max_counter != thread_num:
        shared_max_counter_str = f"({shared_max_counter} 共享限制)"

    if platform.system() == 'Windows':
        service_is_running = service.is_running()
        print(scr_line("-" * ll*3))
        print(scr_str(f"ryry".ljust(ll*3-2)))
        print(scr_str(f"版本: {ver}".ljust(ll*3-4)))
        print(scr_str(f"设备号: {deviceid}".ljust(ll*3-5)))
        print(scr_str(f"容器HostName: {machine_name}".ljust(ll*3-4)))
        print(scr_line("-" * ll*3))
        if service_is_running:
            print(scr_str1(f"运行中 ({thread_num} 线程) {shared_max_counter_str}".ljust(ll*3-2)))
        else:
            print(scr_str1("未运行".ljust(ll*3-2)))
        print(scr_line("-" * ll*3))
        service_status(None, 0)
        print(scr_line("-" * ll*3))
        device_status(None, 0)
        print(scr_line("-" * ll*3))
        widget_status(None, 0)
        print(scr_line("-" * ll*3))
    else:
        import curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        stdscr.keypad(True)
        try:
            tiktak = 0
            while True:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                service_is_running = service.is_running()
                idx=0
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                idx+=1
                stdscr.addstr(idx, 0, scr_str(f"ryry".ljust(ll*3-2)))
                idx+=1
                stdscr.addstr(idx, 0, scr_str(f"版本: {ver}".ljust(ll*3-4)))
                idx+=1
                stdscr.addstr(idx, 0, scr_str(f"设备号: {deviceid}".ljust(ll*3-5)))
                idx+=1
                stdscr.addstr(idx, 0, scr_str(f"容器HostName: {machine_name}".ljust(ll*3-4)))
                idx+=1
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                idx+=1
                if service_is_running:
                    if tiktak > 3:
                        tiktak = 0
                    stdscr.addstr(idx, 0, scr_str1("运行中"+"."*tiktak+f" ({thread_num} 线程) {shared_max_counter_str}".ljust(ll*3-2)), curses.color_pair(1))
                    tiktak+=1
                else:
                    stdscr.addstr(idx, 0, scr_str1("未运行".ljust(ll*3-2)), curses.color_pair(2))
                idx+=1
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                idx+=1
                idx = service_status(stdscr, idx)
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                idx+=1
                idx = device_status(stdscr, idx)
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                idx+=1
                idx = widget_status(stdscr, idx)
                stdscr.addstr(idx, 0, scr_line("-" * ll*3))
                stdscr.refresh()
                time.sleep(1)
        except:
            pass
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

def service():
    if len(sys.argv) <= 2:
        print('please set command!')
        return

    command = sys.argv[2]
    service = ryry_service.ryryService()
    if command == 'start':
        if service.is_running():
            print('Service is already running.')
        else:
            print(f'Starting service...[args = {" ".join(sys.argv)}]')
            threadNum = 1
            idx = 2
            while idx < len(sys.argv):
                if sys.argv[idx] == "-thread":
                    threadNum = int(sys.argv[idx+1])
                    if threadNum < 1 or threadNum > 500:
                        print('multi thread number must be 1~500')
                        return
                idx+=1
            service.start(threadNum)
    elif command == 'stop':
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.stop()
    elif command == 'status': 
        status()
    else:
        print("Unknown command:", command)

def get_widget_config_from_path(main_path):
    """从main.py路径获取widget配置"""
    try:
        config_path = os.path.join(os.path.dirname(main_path), "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None





def widget():
    if len(sys.argv) <= 2:
        print('please set command! Usage: ryry widget [init|publish|list|add|remove|enable|disable|install]')
        return

    command = sys.argv[2]
    work_path = os.getcwd()
    if len(sys.argv) > 3:
        work_path = sys.argv[3]
    if command == 'init':
        ryry_widget.createWidget(work_path)
    elif command == 'publish':
        ryry_widget.publishWidget(work_path)
    elif command == 'list':
        map = store.widgetMap()
        if len(map) == 0:
            print("local widget is empty")
        maxJust = 20
        for it in map:
            if len(it) > maxJust:
                maxJust = len(it)
        maxJust += 10
        showStatus = ""
        if len(sys.argv) > 3:
            showStatus = sys.argv[3]
        for it in map:
            path = ""
            is_block = False
            daemon_enabled = False
            if isinstance(map[it], (dict)):
                path = map[it]["path"]
                is_block = map[it]["isBlock"]
                # 检查是否启用常驻进程
                widget_config = get_widget_config_from_path(path)
                if widget_config:
                    daemon_enabled = widget_config.get("daemon_enabled", False)
            else:
                path = map[it]
            end_args = ""
            if is_block:
                end_args = " [X]"
            if daemon_enabled:
                end_args += " [D]"
            ss = f"{it}{end_args}"
            if showStatus in ["disable", "enable"]:
                if is_block and showStatus == "disable":
                    print(f'{ss.ljust(maxJust + 4)} {path}')
                elif is_block == False and showStatus == "enable":
                    print(f'{ss.ljust(maxJust + 4)} {path}')
            else:
                print(f'{ss.ljust(maxJust + 4)} {path}')
    elif command == 'add':
        ryry_widget.addWidgetToEnv(work_path)
    elif command == 'remove':
        ryry_widget.remove(work_path)
    elif command == 'enable':
        ryry_widget.enable(work_path)
    elif command == 'disable':
        ryry_widget.disable(work_path)
    elif command == 'install':
        ryry_widget.installWidget(work_path)
    else:
        print("Unknown command:", command)

def main():
    urllib3.disable_warnings()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) >= 2:
        module = sys.argv[1]
        if module == "widget":
            widget()
        elif module == "service":
            service()
        elif module == "status":
            status()
        else:
            print(f"Unknown command:{module}")
            sys.exit(0)
    else:
        status()

if __name__ == '__main__':
    status()
