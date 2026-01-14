import time
from firestore_client import rtdb

TIMEOUT_SECONDS = 30


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

        last_seen_ts = view.get("time_epoch")

        if not isinstance(last_seen_ts, int):
            is_online = False
        else:
            is_online = (now - last_seen_ts) <= TIMEOUT_SECONDS

        current_status = device_data.get("status", {}).get("isOnline")

        # Chỉ update khi thay đổi hoặc chưa tồn tại
        if current_status != is_online:
            status_ref.update({
                "isOnline": is_online,
                "lastSeen": last_seen_ts
            })

            print(
                f"[ONLINE CHECK] {device_id} -> "
                f"{'ONLINE' if is_online else 'OFFLINE'} "
                f"(lastSeen={last_seen_ts})"
            )
