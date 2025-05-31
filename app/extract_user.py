from spotify_api.auth import get_spotify_client_oauth
from spotify_api.recent_tracks import get_recent_tracks
from utils.file_writer import save_json
from utils.session import get_session_id
from utils.upload_to_s3 import upload_file_to_s3

# Scope requis pour récupérer les musiques 
SCOPE = "user-read-recently-played user-read-private"

def main():
    sp = get_spotify_client_oauth(scope=SCOPE)
    print("Connexion OAuth réussie.")
    
    session_id = get_session_id(force_new=True)
    print(f"Session ID : {session_id}")
    
    tracks = get_recent_tracks(sp, limit=50)
    # Ajout des genres à chaque piste
    for track in tracks:
        artist_id = track["track"]["artists"][0]["id"]
        try:
            artist_data = sp.artist(artist_id)
            genres = artist_data.get("genres", [])
        except:
            genres = []
        track["genres"] = genres
    print(f"{len(tracks)} morceaux récupérés.")
    
    # Enregistrement structuré dans le dossier de session
    save_json(tracks, directory=f"app/data/user/{session_id}/", prefix="recently_played")
    
    import os

    saved_files = [f for f in os.listdir(f"app/data/user/{session_id}/") if f.startswith("recently_played") and f.endswith(".json")]
    if saved_files:
        file_path = os.path.join(f"app/data/user/{session_id}/", saved_files[0])
        upload_file_to_s3(
            file_path,
            "spotify-listening-intelligence",
            f"user/{session_id}/{saved_files[0]}"
        )
        print("Fichier utilisateur uploadé vers S3.")

if __name__ == "__main__":
    main()
