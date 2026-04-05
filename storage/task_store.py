import json
import os
from qq_console.config import TASK_STORE_PATH, DATA_DIR


def ensure_store():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TASK_STORE_PATH):
        with open(TASK_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def load_tasks():
    ensure_store()
    with open(TASK_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(data):
    ensure_store()
    with open(TASK_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_task(task_name: str, task_info: dict):
    tasks = load_tasks()
    tasks[task_name] = task_info
    save_tasks(tasks)


def get_task(task_name: str):
    tasks = load_tasks()
    return tasks.get(task_name)


def list_tasks():
    tasks = load_tasks()
    return tasks
