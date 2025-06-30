import json
import uuid
import datetime

def create_session(event):
    session_id = "#" + uuid.uuid4().hex[:8]
    created_at = datetime.datetime.utcnow().isoformat() + "Z"

    return {
        "statusCode": 201,
        "body": json.dumps({ "session_id": session_id, "created_at": created_at })
    }

def lambda_handler(event, context):
    return create_session(event)