import boto3
import os
import json
import logging
from utils.file_utils import upload_json_to_s3
from mock_features import generate_mock_features_by_genre

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "spotify-listening-data")

def lambda_handler(event, context):
    logger.info("Transform Lambda invoked")

    try:
        headers = event.get("headers") or {}
        session_id = headers.get("x-session-id")
        mode = headers.get("x-mode")

        logger.info(f"Session ID: {session_id}, Mode: {mode}")

        if not session_id or mode not in ["user", "simulated"]:
            raise ValueError("Missing or invalid session_id/mode")

        key = (
            f"data/{session_id}/{mode}/recent_tracks.json"
            if mode == "user"
            else f"data/{session_id}/{mode}/top_tracks.json"
        )

        logger.info(f"Fetching S3 file: {key}")
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        tracks = json.loads(obj["Body"].read())

        unknown_genres = set()
        enriched = []
        for track in tracks:
            genres = track.get("genres", ["pop"])
            genre = genres[0] if genres else "pop"
            try:
                features = generate_mock_features_by_genre(genre)
            except ValueError:
                logger.warning(f"Genre inconnu : {genre}, fallback vers 'pop'")
                unknown_genres.add(genre)
                features = generate_mock_features_by_genre("pop")
            enriched.append({**track, **features})


        enriched_key = f"data/{session_id}/{mode}/enriched_tracks.json"
        upload_json_to_s3(enriched, BUCKET_NAME, enriched_key)
        logger.info(f"Enriched tracks uploaded to S3: {enriched_key}")

        if unknown_genres:
            log_key = f"logs/{session_id}/unknown_genres.json"
            upload_json_to_s3(list(unknown_genres), BUCKET_NAME, log_key)
            logger.info(f"Unknown genres log uploaded to S3: {log_key}")

        return {
            "statusCode": 200,
            "body": json.dumps(enriched)
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }