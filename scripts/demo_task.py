import time
from datetime import datetime

for i in range(1, 11):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[demo_task] step={i} time={now}", flush=True)
    time.sleep(3)

print("[demo_task] done", flush=True)
