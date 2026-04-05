import os
import sys

BASE_DIR = "/home/ai/1_Projects/AiAgent_Project/qq_openclaw_bridge"
SCRIPT_DIR = os.path.join(BASE_DIR, "qq_console", "scripts")
REPORT_DIR = os.path.join(BASE_DIR, "qq_console", "data", "reports")

WEB_CLEAN_MINI = "/home/ai/1_Projects/AiAgent_Project/webclean_mini"
CODEX_TEST = "/home/ai/1_Projects/AiAgent_Project/codex_test"

PROJECT_SNAPSHOT_SCRIPT = os.path.join(SCRIPT_DIR, "project_snapshot.py")

TASKS = {
    "webclean_snapshot": {
        "cmd": [
            sys.executable,
            PROJECT_SNAPSHOT_SCRIPT,
            "webclean_mini",
            WEB_CLEAN_MINI,
            REPORT_DIR,
        ],
        "cwd": BASE_DIR,
        "description": "生成 webclean_mini 项目的快照报告",
    },
    "webclean_snapshot_slow": {
        "cmd": [
            sys.executable,
            PROJECT_SNAPSHOT_SCRIPT,
            "webclean_mini",
            WEB_CLEAN_MINI,
            REPORT_DIR,
            "5",
        ],
        "cwd": BASE_DIR,
        "description": "生成 webclean_mini 项目的慢速快照报告（便于测试 stop）",
    },
    "codex_test_snapshot": {
        "cmd": [
            sys.executable,
            PROJECT_SNAPSHOT_SCRIPT,
            "codex_test",
            CODEX_TEST,
            REPORT_DIR,
        ],
        "cwd": BASE_DIR,
        "description": "生成 codex_test 项目的快照报告",
    },
}


def get_task_spec(task_name: str):
    return TASKS.get(task_name)


def list_task_specs():
    return TASKS
