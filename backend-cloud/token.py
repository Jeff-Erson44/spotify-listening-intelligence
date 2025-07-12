import urllib.parse
import uuid

CLIENT_ID = "2ceb15aa0a854450b84b14d54f02df5a"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-read-recently-played user-read-private"

def generate_spotify_auth_url():
    state = str(uuid.uuid4())
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",  # <--- ici on change
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "show_dialog": "true"
    }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return url

if __name__ == "__main__":
    auth_url = generate_spotify_auth_url()
    print("Ouvre ce lien dans ton navigateur pour te connecter à Spotify et récupérer le code :")
    print(auth_url)