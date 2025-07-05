import uuid
import boto3
from botocore.exceptions import NoCredentialsError
import os
import json

BUCKET_NAME = "spotify-listening-intelligence"
KEY_NAME = "sessions/session_state.json"  # chemin dans le bucket S3
SESSION_FILE = "session_state.json"

def set_active_session(session_id: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"active_session": session_id}, f)
    upload_to_s3(SESSION_FILE, BUCKET_NAME, KEY_NAME)

def get_active_session() -> str:
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("active_session")

def upload_to_s3(file_path: str, bucket: str, key: str):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_path, bucket, key)
        print(f"{file_path} uploaded to s3://{bucket}/{key}")
    except NoCredentialsError:
        print("❌ AWS credentials not found.")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        
def reset_session() -> str:
    new_session_id = str(uuid.uuid4())
    with open(SESSION_FILE, "w") as f:
        json.dump({"active_session": new_session_id}, f)
    upload_to_s3(SESSION_FILE, BUCKET_NAME, KEY_NAME)
    return new_session_id