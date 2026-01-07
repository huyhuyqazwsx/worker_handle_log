import time
from datetime import datetime
from firestore_client import rtdb

TIMEOUT_SECONDS = 10


def parse_time_today(hms: str) -> int | None:
    try:
        today = datetime.now().date()
        t = datetime.strptime(hms, "%H:%M:%S").time()
        dt = datetime.combine(today, t)
        return int(dt.timestamp())
    except Exception:
        return None


def check_device_online_status():
    now = int(time.time())
    print("[ONLINE CHECK] now =", now)

    sensors = rtdb.child("sensors").get()

    if not isinstance(sensors, dict):
        print("[ONLINE CHECK] No sensors found")
        return

    for device_id, device_data in sensors.items():
        view = device_data.get("view", {})
        status_ref = rtdb.child(f"sensors/{device_id}/status")

        raw_time = view.get("time")

        # Mặc định offline
        is_online = False
        last_seen_ts = None

        # Parse hh:mm:ss
        if isinstance(raw_time, str):
            last_seen_ts = parse_time_today(raw_time)
            if last_seen_ts is not None:
                is_online = (now - last_seen_ts) <= TIMEOUT_SECONDS

        # Trạng thái hiện tại
        current_status = device_data.get("status", {}).get("isOnline")

        # Chỉ update khi có thay đổi hoặc chưa tồn tại
        if current_status != is_online:
            status_ref.update({
                "isOnline": is_online,
                "lastSeen": last_seen_ts
            })

            print(
                f"[ONLINE CHECK] {device_id} -> "
                f"{'ONLINE' if is_online else 'OFFLINE'} "
                f"(time={raw_time})"
            )
