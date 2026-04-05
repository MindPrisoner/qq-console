import asyncio
import json
import subprocess

import websockets

from qq_console.commands.router import route_command
from qq_console.config import INTENTS_GROUP_AND_C2C, OPENCLAW_AGENT
from qq_console.qq.gateway import (
    get_access_token,
    get_gateway_url,
    build_identify_payload,
    heartbeat,
)
from qq_console.qq.sender import send_c2c_reply


def ask_openclaw(message: str, session_id: str) -> str:
    cmd = [
        "openclaw",
        "agent",
        "--agent",
        OPENCLAW_AGENT,
        "--session-id",
        session_id,
        "--message",
        message,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=180,
    )

    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"OpenClaw 调用失败: {err}")

    reply = result.stdout.strip()
    if not reply:
        raise RuntimeError("OpenClaw 没有返回内容")

    return reply


async def run_client():
    access_token = get_access_token()
    print("[step] access_token 获取成功")

    gateway_url = get_gateway_url(access_token)
    print(f"[step] gateway url: {gateway_url}")

    seq_holder = {"seq": None}

    async with websockets.connect(gateway_url, ping_interval=None) as ws:
        hello_raw = await ws.recv()
        hello = json.loads(hello_raw)
        print("[recv] hello:", hello)

        if hello.get("op") != 10:
            raise RuntimeError(f"未收到 Hello(op=10)，实际收到: {hello}")

        heartbeat_interval = hello["d"]["heartbeat_interval"]
        asyncio.create_task(heartbeat(ws, heartbeat_interval, seq_holder))

        identify_payload = build_identify_payload(access_token, INTENTS_GROUP_AND_C2C)
        await ws.send(json.dumps(identify_payload))
        print("[step] identify 已发送")

        while True:
            raw = await ws.recv()
            payload = json.loads(raw)

            if "s" in payload and payload["s"] is not None:
                seq_holder["seq"] = payload["s"]

            op = payload.get("op")
            t = payload.get("t")
            d = payload.get("d")

            if op == 11:
                print("[recv] heartbeat ack")
                continue

            if t == "READY":
                print("[recv] READY:", d)
                continue

            if t == "C2C_MESSAGE_CREATE":
                user_openid = d.get("author", {}).get("user_openid")
                content = d.get("content", "").strip()
                msg_id = d.get("id")

                print("=" * 60)
                print("[recv] 控制台单聊消息来了")
                print("user_openid:", user_openid)
                print("msg_id:", msg_id)
                print("content:", content)
                print("=" * 60)

                if not content:
                    print("[skip] 空消息，跳过")
                    continue

                try:
                    mode, result = route_command(content)

                    if mode == "agent":
                        session_id = f"{OPENCLAW_AGENT}-{user_openid}"
                        print("[step] 正在调用 OpenClaw...")
                        reply = ask_openclaw(result, session_id)
                    else:
                        reply = result

                    print("[step] 最终回复:", reply)
                    print("[step] 正在回发到 QQ...")
                    send_result = send_c2c_reply(access_token, user_openid, msg_id, reply)
                    print("[step] 已回发到 QQ:", send_result)

                except Exception as e:
                    print("[error]", e)

                continue

            print("[recv] other event:", payload)
