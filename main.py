import time
from apscheduler.schedulers.background import BackgroundScheduler

from check_device_online_status import check_device_online_status
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

    # Cleanup mỗi n ngày
    scheduler.add_job(
        cleanup_expired_logs,
        "interval",
        minutes=5,
        id="cleanup_job"
    )

    #kiem tra online
    scheduler.add_job(
        check_device_online_status,
        "interval",
        seconds=10,
        id="online_check_job"
    )

    scheduler.start()

    print("Collector running")
    print("Flush every 10 seconds")
    print("Cleanup every 5 minute")
    print("Check online status every 10 seconds")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
