import json
import os
from utils.auth import get_spotify_client_from_token
from utils.file_utils import upload_json_to_s3

BUCKET_NAME = os.getenv("BUCKET_NAME")
SCOPE = "user-read-recently-played user-read-private"

def get_recent_tracks(sp, limit=50):
    results = sp.current_user_recently_played(limit=limit)
    return results.get("items", [])

def lambda_handler(event, context):
    try:
        print("Lambda execution started")

        token = None
        headers = event.get("headers", {}) or {}

        # Récupération du token depuis header Authorization
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()

        # Si pas dans header, essayer dans cookie
        if not token:
            cookies = headers.get("Cookie") or headers.get("cookie") or ""
            for cookie in cookies.split(";"):
                if "spotify_token" in cookie:
                    token = cookie.split("=")[1].strip()
                    break

        # Si pas dans cookie, essayer dans body
        if not token:
            body_str = event.get("body", "{}")
            try:
                body = json.loads(body_str)
                token = body.get("spotify_token")
            except Exception as e:
                print(f"Error parsing JSON body for token: {e}")

        if not token:
            raise Exception("Missing Spotify token in request.")
        print(f"Spotify token received: {'present' if token else 'absent'}")

        sp = get_spotify_client_from_token(token)
        print("Spotify client initialized")

        # Récupérer le body JSON et parser pour extraire session_id
        body_str = event.get("body", "{}")
        try:
            body = json.loads(body_str)
        except Exception as e:
            raise Exception(f"Invalid JSON body: {e}")

        session_id = body.get("session_id")
        if not session_id:
            raise Exception("Missing 'session_id' in request body.")
        print(f"Session ID received: {session_id}")

        tracks = get_recent_tracks(sp, limit=50)
        print(f"Number of tracks retrieved: {len(tracks)}")

        for track in tracks:
            artist_id = track["track"]["artists"][0]["id"]
            try:
                artist_data = sp.artist(artist_id)
                genres = artist_data.get("genres", [])
            except Exception:
                genres = []
            track["genres"] = genres

        if not BUCKET_NAME:
            raise Exception("Environment variable S3_BUCKET_NAME is not set.")
        print(f"Target S3 bucket: {BUCKET_NAME}")

        s3_key = f"data/{session_id}/recent_tracks.json"
        upload_json_to_s3(tracks, BUCKET_NAME, s3_key)
        print("Upload to S3 completed successfully")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "x-session-id": session_id
            },
            "body": json.dumps({
                "message": "Extraction successful",
                "session_id": session_id,
                "recent_tracks_count": len(tracks),
                "uploaded_file_s3_key": s3_key,
                "recent_tracks_preview": tracks[:5]
            })
        }

    except Exception as e:
        print(f"Error encountered: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }