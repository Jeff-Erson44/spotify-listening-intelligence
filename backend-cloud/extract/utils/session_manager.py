import os
import uuid
import json

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
KEY_NAME = "sessions/session_state.json"
SESSION_FILE = "/tmp/session_state.json"

def set_active_session(session_id: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"active_session": session_id}, f)

def get_active_session() -> str:
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("active_session")

def reset_session() -> str:
    new_session_id = str(uuid.uuid4())
    with open(SESSION_FILE, "w") as f:
        json.dump({"active_session": new_session_id}, f)
    return new_session_id