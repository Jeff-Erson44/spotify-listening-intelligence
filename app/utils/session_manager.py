import os
import json

SESSION_FILE = "session_state.json"

def set_active_session(session_id: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"active_session": session_id}, f)

def get_active_session() -> str:
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("active_session")