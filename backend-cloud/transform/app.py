import boto3
import os
import json
import logging
from utils.file_utils import upload_json_to_s3
from mock_features import generate_mock_features_by_genre

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "spotify-listening-data")

def lambda_handler(event, context):
    logger.info(f"Incoming event: {json.dumps(event)[:500]}")

    try:
        session_id = None

        # 1) Tentative de récupération à partir d'un event S3 (notification)
        if "Records" in event and "s3" in event["Records"][0]:
            try:
                s3_key = event["Records"][0]["s3"]["object"]["key"]
                session_id = s3_key.split("/")[1]
            except (KeyError, IndexError):
                logger.error("Malformed S3 event")
                session_id = None

        # 2) Sinon récupération du session_id depuis le body JSON (pas les headers)
        elif "body" in event:
            try:
                body = event["body"]
                # Le body peut être une string JSON
                if isinstance(body, str):
                    body = json.loads(body)
                session_id = body.get("session_id")
            except Exception as e:
                logger.error(f"Error parsing body JSON: {e}")
                session_id = None

        if not session_id:
            logger.error("Missing session_id from S3 event or request body")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing session_id"})
            }

        logger.info(f"session_id determined: {session_id}")

        key = f"data/{session_id}/recent_tracks.json"
        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        except s3.exceptions.NoSuchKey:
            logger.info(f"recent_tracks.json not found, trying top_tracks.json")
            key = f"data/{session_id}/top_tracks.json"
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)

        logger.info("S3 object retrieved successfully")
        raw = obj["Body"].read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        tracks = json.loads(raw)

        if isinstance(tracks, dict) and "tracks" in tracks:
            tracks = tracks["tracks"]

        if not all(isinstance(t, dict) for t in tracks):
            logger.error("Invalid format: expected list of dicts.")
            raise ValueError("Invalid format: expected list of dicts.")

        unknown_genres = set()
        enriched = []

        for track in tracks:
            genres = track.get("genres", ["pop"])
            genre = genres[0] if genres else "pop"
            try:
                features = generate_mock_features_by_genre(genre)
            except ValueError:
                logger.warning(f"Unknown genre encountered: {genre}, fallback to 'pop'")
                unknown_genres.add(genre)
                features = generate_mock_features_by_genre("pop")
            enriched.append({**track, **features})

        enriched_key = f"data/{session_id}/enriched_tracks.json"
        upload_json_to_s3(enriched, BUCKET_NAME, enriched_key)
        logger.info(f"Enriched tracks uploaded to S3 at {enriched_key}")

        if unknown_genres:
            log_key = f"logs/{session_id}/unknown_genres.json"
            upload_json_to_s3(list(unknown_genres), BUCKET_NAME, log_key)
            logger.info(f"Unknown genres logged to S3 at {log_key}")

        return {
            "statusCode": 200,
            "body": json.dumps(enriched)
        }

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }