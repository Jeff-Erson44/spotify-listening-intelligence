import json
import os
from utils.auth import get_spotify_client_from_token
from utils.file_utils import upload_json_to_s3

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SCOPE = "user-read-recently-played user-read-private"

def get_recent_tracks(sp, limit=50):

    results = sp.current_user_recently_played(limit=limit)
    return results.get("items", [])

def lambda_handler(event, context):
    try:
        print("Début du traitement lambda")

        token = None
        headers = event.get("headers", {}) or {}

        # Recherche du token dans Authorization header
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()

        # Sinon tentative dans les cookies
        if not token:
            cookies = headers.get("Cookie") or headers.get("cookie") or ""
            for cookie in cookies.split(";"):
                if "spotify_token" in cookie:
                    token = cookie.split("=")[1].strip()
                    break

        if not token:
            raise Exception("Token Spotify manquant dans la requête.")
        print(f"Token Spotify reçu (début): {token[:20]}...")

        sp = get_spotify_client_from_token(token)
        print("Client Spotify initialisé")

        session_id = headers.get("x-session-id")
        if not session_id:
            raise Exception("Header 'x-session-id' manquant.")
        print(f"Session reçue via header : {session_id}")

        tracks = get_recent_tracks(sp, limit=50)
        print(f"{len(tracks)} morceaux récupérés")

        for track in tracks:
            artist_id = track["track"]["artists"][0]["id"]
            try:
                artist_data = sp.artist(artist_id)
                genres = artist_data.get("genres", [])
            except Exception:
                genres = []
            track["genres"] = genres

        if not BUCKET_NAME:
            raise Exception("Variable d'environnement S3_BUCKET_NAME non définie.")
        print(f"Bucket S3 cible : {BUCKET_NAME}")

        s3_key = f"data/{session_id}/user/recent_tracks.json"
        upload_json_to_s3(tracks, BUCKET_NAME, s3_key)
        print("Upload vers S3 réussi")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Extraction réussie",
                "session_id": session_id,
                "recent_tracks_count": len(tracks),
                "uploaded_file_s3_key": s3_key,
                "recent_tracks_preview": tracks[:5]
            })
        }

    except Exception as e:
        print(f"Erreur attrapée : {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }