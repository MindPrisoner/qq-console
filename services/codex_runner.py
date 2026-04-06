import os
import subprocess

from qq_console.config import PROJECT_MAP


def resolve_project(project_name: str) -> str | None:
    return PROJECT_MAP.get(project_name)


def run_codex_readonly(project_name: str, prompt: str) -> str:
    project_dir = resolve_project(project_name)
    if not project_dir:
        available = ", ".join(PROJECT_MAP.keys())
        return f"未知项目：{project_name}\n当前可用项目：{available}"

    env = os.environ.copy()
    env.pop("OPENAI_BASE_URL", None)

    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-C",
        project_dir,
        prompt,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
        env=env,
    )

    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip() or "Codex 执行失败"
        return f"Codex 执行失败：\n{err}"

    output = result.stdout.strip()
    if not output:
        return "Codex 没有返回内容。"

    return output
