from qq_console.commands.basic import (
    handle_help,
    handle_time,
    handle_pwd,
    handle_projects,
)
from qq_console.commands.tasks import (
    handle_ps,
    handle_logs,
    handle_run,
    handle_stop,
)


def route_command(text: str) -> tuple[str, str]:
    """
    返回两种模式：
    - direct: 由 Python 直接返回
    - agent: 交给 OpenClaw 处理
    """
    text = text.strip()

    if not text.startswith("#"):
        return "direct", "请使用 #help 查看可用控制台命令。"

    if text == "#help":
        return "direct", handle_help()

    if text == "#time":
        return "direct", handle_time()

    if text == "#pwd":
        return "direct", handle_pwd()

    if text == "#projects":
        return "direct", handle_projects()

    if text == "#ps":
        return "direct", handle_ps()

    if text.startswith("#logs "):
        task_name = text[len("#logs "):].strip()
        if not task_name:
            return "direct", "用法：#logs <任务名>"
        return "direct", handle_logs(task_name)

    if text.startswith("#run "):
        task_name = text[len("#run "):].strip()
        if not task_name:
            return "direct", "用法：#run <任务名>"
        return "direct", handle_run(task_name)

    if text.startswith("#stop "):
        task_name = text[len("#stop "):].strip()
        if not task_name:
            return "direct", "用法：#stop <任务名>"
        return "direct", handle_stop(task_name)

    if text.startswith("#ask "):
        prompt = text[len("#ask "):].strip()
        if not prompt:
            return "direct", "用法：#ask 你的问题"
        return "agent", prompt

    return "direct", "未知命令。请发送 #help 查看可用控制台命令。"
