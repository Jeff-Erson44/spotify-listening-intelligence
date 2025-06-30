import json
from utils.auth import get_spotify_client_oauth
from utils.session import get_session_id
from utils.session_manager import set_active_session

def lambda_handler(event, context):
    try:
        # Initialiser session utilisateur
        session_id = get_session_id()
        set_active_session(session_id)

        # Authentifier l'utilisateur avec OAuth
        scope = "user-read-recently-played"
        sp = get_spotify_client_oauth(scope=scope)

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
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }