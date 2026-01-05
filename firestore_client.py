import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, db

# Lấy JSON từ environment variable
service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

if not service_account_json:
    raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON env var")

cred_dict = json.loads(service_account_json)

# Init Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(
        credentials.Certificate(cred_dict),
        {
            "databaseURL": "https://tree-watcher-4bddd-default-rtdb.asia-southeast1.firebasedatabase.app"
        }
    )

firestore_db = firestore.client()
rtdb = db.reference()

