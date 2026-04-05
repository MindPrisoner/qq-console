import asyncio

from qq_console.qq.client import run_client
from qq_console.storage.task_store import ensure_store


def main():
    ensure_store()
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
