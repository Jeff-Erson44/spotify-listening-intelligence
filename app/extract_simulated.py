from spotify_api.auth import get_spotify_client_credentials
from spotify_api.search import search_artist, prompt_user_to_select
from spotify_api.top_tracks import get_artist_top_tracks
from utils.file_writer import save_json
from utils.session import get_session_id
from utils.upload_to_s3 import upload_file_to_s3
import time
import os

session_id = get_session_id(force_new=True)
print(f"Session ID : {session_id}")

def main():
    sp = get_spotify_client_credentials()

    artist_names_input = input("Entrez 5 à 10 noms d'artistes séparés par des virgules :")
    artist_names = [name.strip() for name in artist_names_input.split(",") if name.strip()]

    all_tracks = []
    for name in artist_names:
        artist_results = search_artist(sp, name, market="US", limit=10)
        if not artist_results:
            print(f"Aucun résultat pour {name}")
            continue

        # Trier par popularité
        artist_results.sort(key=lambda artist: artist.get("popularity", 0), reverse=True)

        # Tenter de trouver un nom strictement égal, très populaire
        filtered = [a for a in artist_results if a["name"].lower() == name.lower() and a.get("popularity", 0) > 80]

        if filtered:
            top_artist = filtered[0]
        else:
            print(f"🔍 Aucun artiste populaire correspondant strictement à « {name} ». Sélection manuelle :")
            top_artist_id = prompt_user_to_select(artist_results, user_input=name)
            if not top_artist_id:
                continue
            top_artist = next((a for a in artist_results if a["id"] == top_artist_id), None)
            if not top_artist:
                print(f"Erreur : artiste non trouvé dans les résultats.")
                continue

        artist_id = top_artist["id"]

        artist_info = sp.artist(artist_id)
        genres = artist_info.get("genres", [])
        if not genres:
            genres = ["pop"]

        tracks = get_artist_top_tracks(sp, artist_id, limit=5)
        for track in tracks:
            if track.get("track_id"):
                track["artist_id"] = artist_id
                track["genres"] = genres
                all_tracks.append(track)
                time.sleep(0.15)

    print(f"{len(all_tracks)} morceaux récupérés depuis {len(artist_names)} artistes.")
    save_json(all_tracks, f"app/data/simulated/{session_id}/", prefix="simulated_tracks")

    # Récupération du nom du fichier créé
    filename = [f for f in os.listdir(f"app/data/simulated/{session_id}/") if f.startswith("simulated_tracks")][0]
    file_path = os.path.join(f"app/data/simulated/{session_id}/", filename)

    # Upload vers S3
    upload_file_to_s3(
        file_path,
        bucket_name="spotify-listening-intelligence",
        s3_key=f"simulated/{session_id}/{filename}"
    )
    print("Fichier simulé uploadé vers S3.")

if __name__ == "__main__":
    main()
