import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from utils.session import get_session_id
from utils.file_writer import save_json
from utils.upload_to_s3 import upload_file_to_s3

# Scopes nécessaires
SCOPE = "user-read-private user-top-read"

def get_top_artist(sp, time_range="short_term"):
    results = sp.current_user_top_artists(time_range=time_range, limit=1)
    if results["items"]:
        artist = results["items"][0]
        return {
            "name": artist["name"],
            "image_url": artist["images"][0]["url"] if artist["images"] else None
        }
    return {"name": None, "image_url": None}

def main():
    session_id = get_session_id(force_new=False)
    data_path = f"app/data/user/{session_id}/"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, show_dialog=True))

    profile = sp.current_user()
    display_name = profile.get("display_name", "Utilisateur")

    summary = {
        "display_name": display_name,
        "top_artist_short": get_top_artist(sp, "short_term"),
        "top_artist_medium": get_top_artist(sp, "medium_term"),
        "top_artist_long": get_top_artist(sp, "long_term")
    }

    save_json(summary, data_path, prefix="fetch_profile")

    # Trouver le fichier sauvegardé
    saved_files = [f for f in os.listdir(data_path) if f.startswith("fetch_profile") and f.endswith(".json")]
    if saved_files:
        upload_file_to_s3(
            os.path.join(data_path, saved_files[0]),
            "spotify-listening-intelligence",
            f"user/{session_id}/{saved_files[0]}"
        )
    print(f"✅ Profil résumé enregistré dans {data_path}")

if __name__ == "__main__":
    main()