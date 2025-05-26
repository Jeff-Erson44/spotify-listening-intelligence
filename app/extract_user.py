from spotify_api.auth import get_spotify_client_oauth
from spotify_api.recent_tracks import get_recent_tracks
from utils.file_writer import save_json

#Scope requis pour l'utilisateur
SCOPE = "user-read-recently-played user-read-private"

def main():
    sp = get_spotify_client_oauth(scope=SCOPE)
    print("Connexion réussie.")
    
    tracks = get_recent_tracks(sp, limit=50)
    print (f"Nombre de morceaux récupérés: {len(tracks)}")
    
    save_json(tracks, directory="app/data/user/")
    
if __name__ == "__main__":
    main()
