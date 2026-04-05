import asyncio
import json

import requests

from qq_console.config import QQ_APP_ID, QQ_APP_SECRET


def get_access_token() -> str:
    url = "https://bots.qq.com/app/getAppAccessToken"
    resp = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "appId": QQ_APP_ID,
            "clientSecret": QQ_APP_SECRET,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"获取 access_token 失败: {data}")

    return token


def get_gateway_url(access_token: str) -> str:
    url = "https://api.sgroup.qq.com/gateway"
    resp = requests.get(
        url,
        headers={"Authorization": f"QQBot {access_token}"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    gateway_url = data.get("url")
    if not gateway_url:
        raise RuntimeError(f"获取 gateway url 失败: {data}")

    return gateway_url


def build_identify_payload(access_token: str, intents: int) -> dict:
    return {
        "op": 2,
        "d": {
            "token": f"QQBot {access_token}",
            "intents": intents,
            "shard": [0, 1],
            "properties": {
                "$os": "linux",
                "$browser": "qq-console",
                "$device": "qq-console",
            },
        },
    }


async def heartbeat(ws, interval_ms: int, seq_holder: dict):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        payload = {"op": 1, "d": seq_holder.get("seq")}
        await ws.send(json.dumps(payload))
        print("[heartbeat] sent")
