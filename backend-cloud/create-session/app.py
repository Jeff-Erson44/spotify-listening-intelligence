import json
import uuid
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_session(event):
    try:
        session_id = uuid.uuid4().hex[:6]  
        created_at = datetime.datetime.utcnow().isoformat() + "Z"
        logger.info(f"Session created: {session_id} at {created_at}")

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps({
                "sessionId": session_id,
                "createdAt": created_at,
                "message": "Session created"
            })
        }
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps({
                "message": "Internal Server Error"
            })
        }

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    return create_session(event)