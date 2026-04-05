import os
import sys
import time
from pathlib import Path
from collections import Counter
from datetime import datetime


SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


def maybe_sleep(seconds: float, label: str):
    if seconds > 0:
        print(f"[snapshot] {label}，等待 {seconds} 秒...", flush=True)
        time.sleep(seconds)


def main():
    if len(sys.argv) not in (4, 5):
        print("用法: python project_snapshot.py <project_name> <project_path> <report_dir> [sleep_seconds]")
        sys.exit(1)

    project_name = sys.argv[1]
    project_path = Path(sys.argv[2]).expanduser().resolve()
    report_dir = Path(sys.argv[3]).expanduser().resolve()
    sleep_seconds = float(sys.argv[4]) if len(sys.argv) == 5 else 0.0

    print(f"[snapshot] project_name={project_name}", flush=True)
    print(f"[snapshot] project_path={project_path}", flush=True)
    print(f"[snapshot] sleep_seconds={sleep_seconds}", flush=True)

    if not project_path.exists():
        print("[snapshot] ERROR: 项目目录不存在", flush=True)
        sys.exit(1)

    maybe_sleep(sleep_seconds, "准备扫描项目")

    top_level_items = []
    for item in sorted(project_path.iterdir(), key=lambda p: p.name.lower()):
        name = item.name + ("/" if item.is_dir() else "")
        top_level_items.append(name)

    maybe_sleep(sleep_seconds, "顶层目录扫描完成")

    ext_counter = Counter()
    readmes = []
    total_files = 0
    truncated = False

    for dirpath, dirnames, filenames in os.walk(project_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            rel_path = file_path.relative_to(project_path)

            total_files += 1
            if total_files > 5000:
                truncated = True
                break

            suffix = file_path.suffix.lower() or "[no_ext]"
            ext_counter[suffix] += 1

            if filename.lower().startswith("readme"):
                readmes.append(str(rel_path))

        if truncated:
            break

    maybe_sleep(sleep_seconds, "文件统计完成")

    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = report_dir / f"{project_name}_snapshot_{timestamp}.md"

    top_ext_lines = []
    for ext, count in ext_counter.most_common(10):
        top_ext_lines.append(f"- {ext}: {count}")

    report_lines = [
        f"# 项目快照：{project_name}",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 项目路径：`{project_path}`",
        f"- 文件总数（最多统计 5000 个）：{total_files}",
        f"- 是否截断统计：{'是' if truncated else '否'}",
        "",
        "## 顶层目录结构",
        "",
    ]

    if top_level_items:
        report_lines.extend([f"- {item}" for item in top_level_items[:50]])
    else:
        report_lines.append("- (空目录)")

    report_lines.extend([
        "",
        "## README 文件",
        "",
    ])

    if readmes:
        report_lines.extend([f"- {item}" for item in readmes])
    else:
        report_lines.append("- 未发现 README")

    report_lines.extend([
        "",
        "## 文件类型统计（Top 10）",
        "",
    ])

    if top_ext_lines:
        report_lines.extend(top_ext_lines)
    else:
        report_lines.append("- 没有可统计文件")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    maybe_sleep(sleep_seconds, "报告写入完成")

    print("[snapshot] 顶层目录：", flush=True)
    for item in top_level_items[:20]:
        print(f"  - {item}", flush=True)

    print("[snapshot] README：", flush=True)
    if readmes:
        for item in readmes:
            print(f"  - {item}", flush=True)
    else:
        print("  - 未发现 README", flush=True)

    print("[snapshot] 文件类型统计 Top 10：", flush=True)
    for ext, count in ext_counter.most_common(10):
        print(f"  - {ext}: {count}", flush=True)

    print(f"[snapshot] report_path={report_path}", flush=True)
    print("[snapshot] done", flush=True)


if __name__ == "__main__":
    main()