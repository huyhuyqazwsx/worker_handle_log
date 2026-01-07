from datetime import datetime
from firestore_client import firestore_db

def cleanup_expired_logs():
    now = datetime.utcnow()
    deleted = 0

    devices = firestore_db.collection("log").stream()

    for device in devices:
        device_id = device.id

        expired_docs = (
            firestore_db
            .collection("log")
            .document(device_id)
            .collection("view")
            .where("expired_at", "<", now)
            .stream()
        )

        for doc in expired_docs:
            doc.reference.delete()
            deleted += 1
            print(f"Deleted: {device_id}/view/{doc.id}")

    print(f"[CLEANUP] Done. Deleted {deleted} docs")
