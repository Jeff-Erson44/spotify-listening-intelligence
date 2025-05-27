import uuid
import os 

SESSION_FILE = ".session"

def generate_session_id():
    session_id = str(uuid.uuid4())[:8]
    with open(SESSION_FILE, "w") as f:
        f.write(session_id)
    return session_id

def get_session_id(force_new=False):
    if force_new or not os.path.exists(SESSION_FILE):
        return generate_session_id()
    with open(SESSION_FILE, "r") as f:
        return f.read().strip()