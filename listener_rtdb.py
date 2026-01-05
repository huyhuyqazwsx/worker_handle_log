from datetime import datetime
from firestore_client import rtdb
from accumulator import add_metric

METRICS = {"temp", "hum_air", "hum_soil", "light"}

def process_full_view(device_id, view: dict):
    for metric, value in view.items():
        if metric not in METRICS:
            continue

        try:
            val = float(value)
        except (TypeError, ValueError):
            continue

        add_metric(device_id, metric, val)
        print(f"[VIEW READ] {device_id} {metric} = {val}")

def rtdb_listener(event):
    # bỏ snapshot root
    if event.path == "/":
        print("Skip (root snapshot)")
        return

    path = event.path.strip("/")
    parts = path.split("/")

    # path dạng: device_001/view/hum_air
    if len(parts) == 3 and parts[1] == "view":
        device_id = parts[0]

        # Lay toan bo snapshot
        view = rtdb.child(f"sensors/{device_id}/view").get()

        #Phat hien null
        if not isinstance(view, dict):
            print("Skip (view not dict)")
            return

        process_full_view(device_id, view)
        return

    print("Skip (unhandled path)")

def start_rtdb_listener():
    print("Start listening RTDB at /sensors")
    rtdb.child("sensors").listen(rtdb_listener)
