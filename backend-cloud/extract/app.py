import json
from utils.auth import get_spotify_client_from_token
from utils.session import get_session_id
from utils.session_manager import set_active_session

def lambda_handler(event, context):
    try:
        # Initialiser session utilisateur
        session_id = get_session_id()
        set_active_session(session_id)

        # Récupérer le token Spotify depuis le header Authorization ou les cookies
        token = None

        headers = event.get("headers", {}) or {}
        # Cherche le token dans Authorization header (ex: "Bearer <token>")
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()

        # Sinon chercher dans les cookies
        if not token:
            cookies = headers.get("Cookie") or headers.get("cookie") or ""
            for cookie in cookies.split(";"):
                if "spotify_token" in cookie:
                    token = cookie.split("=")[1].strip()
                    break

        print(f"Token récupéré : {token}")  # Log token extrait

        if not token:
            raise Exception("Token Spotify manquant dans la requête (ni header Authorization ni cookie).")

        # Créer un client Spotify avec le token
        sp = get_spotify_client_from_token(token)

        # Tester si l'auth fonctionne en récupérant les derniers morceaux
        results = sp.current_user_recently_played(limit=5)
        tracks = [{
            "track_name": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "played_at": item["played_at"]
        } for item in results["items"]]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Extraction réussie",
                "session_id": session_id,
                "recent_tracks": tracks
            })
        }
    except Exception as e:
        print(f"Erreur attrapée : {e}")  # Log erreur
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }