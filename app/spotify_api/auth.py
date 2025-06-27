import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    raise ValueError("Variables d'environnement SPOTIPY manquantes. Vérifie ton fichier .env.")

def get_spotify_client_oauth(scope=None):
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        show_dialog=True,
        cache_path=".cache"  # stocke le token et refresh token dans ce fichier
    )

def print_access_token(scope=None):
    sp_oauth = get_spotify_client_oauth(scope=scope)
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print("Pas de token en cache, lance l'authentification dans le navigateur...")
        auth_url = sp_oauth.get_authorize_url()
        print("Ouvre cette URL et récupère le code dans la redirection :\n", auth_url)
        response = input("Colle ici l'URL de redirection complète après authentification :\n")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    
    # Rafraîchir le token si expiré
    if sp_oauth.is_token_expired(token_info):
        print("Token expiré, rafraîchissement en cours...")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    access_token = token_info.get("access_token")
    refresh_token = token_info.get("refresh_token")

    print("Access Token Spotify (à mettre dans les cookies) :", access_token)
    print("Refresh Token Spotify (à conserver en sécurité) :", refresh_token)

    return access_token

if __name__ == "__main__":
    print_access_token(scope="user-read-recently-played")