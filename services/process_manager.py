import os
import subprocess
from datetime import datetime

from qq_console.config import DATA_DIR
from qq_console.storage.task_store import get_task, list_tasks, set_task
from qq_console.services.task_registry import get_task_spec

LOG_DIR = os.path.join(DATA_DIR, "logs")


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_pid_running(pid: int) -> bool:
    """
    判断一个 pid 是否还在真正运行。
    在 Linux / WSL 下，僵尸进程（Z）虽然还占着 pid，
    但实际上任务已经结束了，不应继续算 running。
    """
    proc_stat_path = f"/proc/{pid}/stat"

    if not os.path.exists(proc_stat_path):
        return False

    try:
        with open(proc_stat_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # /proc/<pid>/stat 的第三个字段是进程状态
        # 常见值：
        # R = running
        # S = sleeping
        # D = uninterruptible sleep
        # Z = zombie
        fields = content.split()
        if len(fields) < 3:
            return False

        state = fields[2]

        # 僵尸进程不算“正在运行”
        if state == "Z":
            return False

        return True

    except Exception:
        return False


def refresh_task_status(task_name: str):
    task = get_task(task_name)
    if not task:
        return None

    pid = task.get("pid")
    status = task.get("status", "unknown")

    if status == "running" and pid:
        if not is_pid_running(pid):
            task["status"] = "finished"
            task["finished_at"] = now_str()
            set_task(task_name, task)

    return task


def start_task(task_name: str) -> str:
    spec = get_task_spec(task_name)
    if not spec:
        return f"未知任务：{task_name}"

    old_task = refresh_task_status(task_name)
    if old_task and old_task.get("status") == "running":
        return f"任务 {task_name} 已经在运行中，pid={old_task.get('pid')}"

    ensure_log_dir()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = os.path.join(LOG_DIR, f"{task_name}-{timestamp}.log")

    log_file = open(log_path, "a", encoding="utf-8")

    process = subprocess.Popen(
        spec["cmd"],
        cwd=spec["cwd"],
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )

    task_info = {
        "task_name": task_name,
        "status": "running",
        "pid": process.pid,
        "started_at": now_str(),
        "finished_at": "",
        "log_path": log_path,
        "command": spec["cmd"],
        "description": spec.get("description", ""),
    }
    set_task(task_name, task_info)

    return (
        f"任务已启动：{task_name}\n"
        f"pid: {process.pid}\n"
        f"log: {log_path}"
    )


def list_task_statuses() -> str:
    tasks = list_tasks()
    if not tasks:
        return "当前没有登记中的任务。"

    lines = ["当前任务状态："]
    for name in tasks:
        task = refresh_task_status(name)
        if not task:
            continue
        lines.append(
            f"- {name}: {task.get('status', 'unknown')} (pid={task.get('pid', '-')})"
        )
    return "\n".join(lines)


def read_task_logs(task_name: str, last_n: int = 20) -> str:
    task = refresh_task_status(task_name)
    if not task:
        return f"没有找到任务：{task_name}"

    log_path = task.get("log_path", "")
    if not log_path or not os.path.exists(log_path):
        return f"任务 {task_name} 目前没有可读日志。"

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    tail = lines[-last_n:] if lines else []
    if not tail:
        return f"任务 {task_name} 的日志目前为空。"

    return "".join(tail).strip()
