from qq_console.services.process_manager import (
    list_task_statuses,
    read_task_logs,
    start_task,
)


def handle_ps() -> str:
    return list_task_statuses()


def handle_logs(task_name: str) -> str:
    return read_task_logs(task_name)


def handle_run(task_name: str) -> str:
    return start_task(task_name)
