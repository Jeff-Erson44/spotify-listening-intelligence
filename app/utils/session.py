import uuid 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os 
from dotenv import load_dotenv

load_dotenv()

_spotify_client = None
_session_id = None

# Retourne la session existante sans en créer une nouvelle
def get_existing_session_id():
    return _session_id

#Générer une session utilisateur unique 
def get_session_id(force_new=False):
    global _session_id
    if _session_id is None or force_new:
        _session_id = "#" + uuid.uuid4().hex[:8]
    return _session_id

#Initialiser une instance Spotipy
def get_spotify_client():
    global _spotify_client
    if _spotify_client is None:
        _spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-recently-played"
        ))
    return _spotify_client

#Vérifier si Spotippy est prêt def is_authenticated():
def is_authenticated():
    return _spotify_client is not None

#Reset Session 
def reset_session():
    global _spotify_client, _session_id
    _spotify_client = None
    _session_id = None

if __name__ == "__main__":
    print("Fichier session.py exécuté avec succès. Spotify client prêt :", is_authenticated())