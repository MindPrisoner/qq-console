import os
from dotenv import load_dotenv

load_dotenv(".env.qqconsole")

QQ_APP_ID = os.getenv("QQ_APP_ID")
QQ_APP_SECRET = os.getenv("QQ_APP_SECRET")

if not QQ_APP_ID or not QQ_APP_SECRET:
    raise RuntimeError("请先在 .env.qqconsole 里填写 QQ_APP_ID 和 QQ_APP_SECRET")

INTENTS_GROUP_AND_C2C = 1 << 25

PROJECTS_ROOT = "/home/ai/1_Projects/AiAgent_Project"
DATA_DIR = "/home/ai/1_Projects/AiAgent_Project/qq_openclaw_bridge/qq_console/data"
TASK_STORE_PATH = f"{DATA_DIR}/tasks.json"

TIMEZONE = "Asia/Shanghai"
OPENCLAW_AGENT = "qqconsole"
