import json
import uuid
import datetime

def create_session(event):
    session_id = uuid.uuid4().hex[:8]
    created_at = datetime.datetime.utcnow().isoformat() + "Z"

    return {
    "statusCode": 201,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Session-Id",
        "Access-Control-Expose-Headers": "X-Session-Id",
        "X-Session-Id": session_id,
        "X-Created-At": created_at
    },
    "body": json.dumps({ "message": "Session created" })
}

def lambda_handler(event, context):
    return create_session(event)