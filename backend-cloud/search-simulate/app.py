import boto3
from datetime import datetime
import os
import logging
import json
from utils.auth import get_spotify_client_credentials
from utils.file_utils import upload_json_to_s3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        session_id = body.get("x-session-id") or event.get("headers", {}).get("x-session-id")
        artists = body.get("artists", [])

        if not session_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing session_id."})}

        if not isinstance(artists, list) or len(artists) < 1:
            return {"statusCode": 400, "body": json.dumps({"error": "Au moins 1 artiste est requis."})}

        logger.info("Creating Spotify client...")
        sp = get_spotify_client_credentials()
        tracks = []

        for artist in artists:
            artist_id = artist.get("id")
            artist_name = artist.get("name")
            if not artist_id or not artist_name:
                continue

            logger.info(f"Fetching top tracks for artist: {artist_name} ({artist_id})")

            top_tracks = sp.artist_top_tracks(artist_id, country="US").get("tracks", [])[:5]
            logger.info(f"Found {len(top_tracks)} tracks for {artist_name}")

            fallback_genres = artist.get("genres") or ["pop"]
            for track in top_tracks:
                track_genres = track.get("genres")
                tracks.append({
                    "id": track.get("id"),
                    "name": track.get("name"),
                    "artist": artist_name,
                    "genres": track_genres if track_genres else fallback_genres
                })

        logger.info(f"Returning {len(tracks)} total tracks for session: {session_id}")

        # Enregistrement en bucket S3

        bucket_name = os.environ.get("S3_BUCKET_NAME")
        if not bucket_name:
            raise Exception("Variable d'environnement S3_BUCKET_NAME non définie.")

        s3_key = f"data/{session_id}/simulated/top_tracks.json"
        upload_json_to_s3({
            "session_id": session_id,
            "tracks": tracks
        }, bucket_name, s3_key)

        logger.info(f"Upload vers S3 réussi : {s3_key}")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": session_id,
                "tracks": tracks
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }