import time
from apscheduler.schedulers.background import BackgroundScheduler

from listener_rtdb import start_rtdb_listener
from scheduler import flush_to_firestore
from cleanup import cleanup_expired_logs

def main():
    print("RTDB Log Collector starting...")

    # Listen realtime database
    start_rtdb_listener()

    scheduler = BackgroundScheduler()

    # Gửi mỗi n thời gian để ghi log vào firestore
    scheduler.add_job(
        flush_to_firestore,
        "interval",
        seconds=10,
        id="flush_job"
    )

    # Cleanup mỗi 1 ngày
    scheduler.add_job(
        cleanup_expired_logs,
        "interval",
        minutes=1,
        id="cleanup_job"
    )

    scheduler.start()

    print("Collector running")
    print("Flush every 10 seconds")
    print("Cleanup every 1 minute")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
