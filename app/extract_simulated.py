from spotify_api.auth import get_spotify_credentials
from spotify_api.search import search_artist
from spotify_api.top_tracks import get_artist_top_tracks
from utils.file_writer import save_json

def main():
    sp = get_spotify_credentials()

    artist_names_input = input("Entrez 5 à 10 noms d'artistes séparés par des virgules :")
    artist_names = [name.strip() for name in artist_names_input.split(",") if name.strip()]

    all_tracks = []
    for name in artist_names:
        artist_id = search_artist(sp, name)
        if artist_id:
            artist_info = sp.artist(artist_id)
            genres = artist_info.get("genres", [])

            tracks = get_artist_top_tracks(sp, artist_id, limit=5)
            for track in tracks:
                if track.get("track_id"):
                    track["artist_id"] = artist_id
                    track["genres"] = genres
                    all_tracks.append(track)

    print(f"✅ {len(all_tracks)} morceaux récupérés depuis {len(artist_names)} artistes.")
    save_json(all_tracks, "app/data/simulated/", prefix="simulated_tracks")

if __name__ == "__main__":
    main()
