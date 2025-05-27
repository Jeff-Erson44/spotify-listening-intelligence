from spotify_api.auth import get_spotify_client_oauth
from spotify_api.recent_tracks import get_recent_tracks
from utils.file_writer import save_json
from utils.session import get_session_id

# Scope requis pour récupérer les musiques 
SCOPE = "user-read-recently-played user-read-private"

def main():
    sp = get_spotify_client_oauth(scope=SCOPE)
    print("Connexion OAuth réussie.")
    
    session_id = get_session_id(force_new=True)
    print(f"Session ID : {session_id}")
    
    tracks = get_recent_tracks(sp, limit=50)
    print(f"{len(tracks)} morceaux récupérés.")
    
    # Enregistrement structuré dans le dossier de session
    save_json(tracks, directory=f"app/data/user/{session_id}/", prefix="recently_played")

if __name__ == "__main__":
    main()
