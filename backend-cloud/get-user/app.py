import json
import os
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv("BUCKET_NAME")

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        print("get-user-profile lambda started")

        # Récupération du body JSON
        body_str = event.get("body", "{}")
        try:
            body = json.loads(body_str)
        except Exception as e:
            raise Exception(f"Invalid JSON body: {e}")

        session_id = body.get("session_id")
        if not session_id:
            raise Exception("Missing 'session_id' in request body.")
        print(f"Session ID: {session_id}")

        s3_key = f"data/{session_id}/profile.json"

        # Téléchargement du fichier profile.json depuis S3
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            profile_content = response['Body'].read().decode('utf-8')
            profile_json = json.loads(profile_content)
        except ClientError as e:
            print(f"Error fetching profile.json from S3: {e}")
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Profile not found"})
            }

        print("Profile fetched successfully")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(profile_json)
        }

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }