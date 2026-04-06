from qq_console.services.codex_runner import run_codex_readonly
from qq_console.config import PROJECT_MAP


def handle_code_help() -> str:
    projects = ", ".join(PROJECT_MAP.keys())
    return (
        "用法：#code <项目名> <任务描述>\n"
        f"当前可用项目：{projects}\n"
        "示例：#code webclean_mini 用中文总结这个项目的目录结构和主要文件职责"
    )


def handle_code(text: str) -> str:
    parts = text.split(maxsplit=2)

    if len(parts) < 3:
        return handle_code_help()

    _, project_name, prompt = parts

    if not prompt.strip():
        return handle_code_help()

    return run_codex_readonly(project_name, prompt.strip())
