import requests


def send_c2c_reply(access_token: str, user_openid: str, msg_id: str, content: str):
    url = f"https://api.sgroup.qq.com/v2/users/{user_openid}/messages"
    payload = {
        "content": content[:1500],
        "msg_type": 0,
        "msg_id": msg_id,
        "msg_seq": 1,
    }

    resp = requests.post(
        url,
        headers={
            "Authorization": f"QQBot {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()
