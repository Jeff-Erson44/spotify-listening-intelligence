import uuid

_session_id = None 

# Création d'un id de session
def get_session_id(force_new=False):
    global _session_id
    if _session_id is None or force_new:
        _session_id = "#" + uuid.uuid4().hex[:8]
    return _session_id

# Vérifie si une session existe
def get_existing_session_id():
    return _session_id

def reset_session():
    global _session_id
    _session_id = None