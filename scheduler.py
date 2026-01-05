from datetime import datetime, timedelta
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from firestore_client import firestore_db
from accumulator import acc, reset_metric

METRICS = {"temp", "hum_air", "hum_soil", "light"}

def flush_to_firestore():
    now = datetime.utcnow()
    expired_at = now + timedelta(minutes=2)

    for device_id, metrics in acc.items():
        doc = {}

        for metric in METRICS:
            bucket = metrics.get(metric)
            if not bucket or bucket["count"] == 0:
                continue

            doc[metric] = bucket["sum"] / bucket["count"]
            reset_metric(bucket)

        if not doc:
            continue

        doc["logged_at"] = SERVER_TIMESTAMP
        doc["expired_at"] = expired_at

        #ghi log vào firestore /log/device_id/view
        firestore_db \
            .collection("log") \
            .document(device_id) \
            .collection("view") \
            .add(doc)

        print(f"[FLUSH] Written view snapshot for {device_id}")

    print("[FLUSH] Done")
