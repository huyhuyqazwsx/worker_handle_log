import os
import firebase_admin
from firebase_admin import credentials, firestore, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "serviceAccount.json")

print("Service account path:", SERVICE_ACCOUNT_PATH)

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://tree-watcher-4bddd-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
)

firestore_db = firestore.client()
rtdb = db.reference()
