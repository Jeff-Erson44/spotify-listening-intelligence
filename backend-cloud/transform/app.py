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

    try:
        headers = event.get("headers") or {}
        session_id = headers.get("x-session-id")
        if not session_id:
            logger.error("Missing session_id header")
            raise ValueError("Missing session_id")

        logger.info(f"Session ID: {session_id}")
        logger.info(f"Trying to fetch key: data/{session_id}/recent_tracks.json")
        try:
            key = f"data/{session_id}/recent_tracks.json"
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        except s3.exceptions.NoSuchKey:
            logger.info(f"recent_tracks.json not found, trying top_tracks.json")
            key = f"data/{session_id}/top_tracks.json"
            logger.info(f"Trying to fetch key: {key}")
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)

        logger.info(f"S3 object metadata: {obj}")
        logger.info(f"Reading object body")
        raw = obj["Body"].read()
        logger.info(f"Raw type: {type(raw)}")
        logger.info(f"Raw content: {raw[:200]}")  # affiche les 200 premiers caractères
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        tracks = json.loads(raw)
        if isinstance(tracks, dict) and "tracks" in tracks:
            tracks = tracks["tracks"]
        elif isinstance(tracks, list) and all(isinstance(t, str) for t in tracks):
            logger.error("Expected list of dicts, got list of strings.")
            raise ValueError("Expected list of dicts, got list of strings.")
        elif not all(isinstance(t, dict) for t in tracks):
            logger.error("Invalid format: expected list of dicts.")
            raise ValueError("Invalid format: expected list of dicts.")
        logger.info(f"Tracks loaded: {len(tracks)} items")

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

        enriched_key = f"data/{session_id}/enriched_tracks.json"
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