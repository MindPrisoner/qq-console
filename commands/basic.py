from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess

from qq_console.config import PROJECTS_ROOT, TIMEZONE


def run_fixed_command(args: list[str]) -> str:
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=15,
    )

    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip() or "命令执行失败"
        raise RuntimeError(err)

    output = result.stdout.strip()
    return output if output else "(空结果)"


def handle_help() -> str:
    return (
        "当前可用命令：\n"
        "#help - 查看帮助\n"
        "#time - 查看当前服务器时间\n"
        "#pwd - 查看当前工作目录\n"
        "#projects - 查看项目总目录内容\n"
        "#run <任务名> - 启动一个预设任务\n"
        "#ps - 查看任务状态\n"
        "#logs <任务名> - 查看任务最近日志\n"
        "#ask <内容> - 交给 Agent 思考并回复"
    )


def handle_time() -> str:
    now = datetime.now(ZoneInfo(TIMEZONE))
    return f"当前服务器时间：{now.strftime('%Y-%m-%d %H:%M:%S')}（{TIMEZONE}）"


def handle_pwd() -> str:
    return run_fixed_command(["/usr/bin/pwd"])


def handle_projects() -> str:
    return run_fixed_command(["/usr/bin/ls", PROJECTS_ROOT])
