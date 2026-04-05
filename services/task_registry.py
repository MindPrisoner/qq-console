import os
import sys

BASE_DIR = "/home/ai/1_Projects/AiAgent_Project/qq_openclaw_bridge"
DEMO_TASK = os.path.join(BASE_DIR, "qq_console", "scripts", "demo_task.py")

TASKS = {
    "demo": {
        "cmd": [sys.executable, DEMO_TASK],
        "cwd": BASE_DIR,
        "description": "演示后台任务：每3秒写一条日志，共10次",
    }
}


def get_task_spec(task_name: str):
    return TASKS.get(task_name)


def list_task_specs():
    return TASKS
