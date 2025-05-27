import json
import os
from utils.file_writer import save_json
from audio.mock_features import generate_mock_features_by_genre
from utils.session import get_session_id

session_id = get_session_id()
data_path = f"app/data/simulated/{session_id}/"

def main():
    # Charge le dernier fichier simulé pour la session
    files = [f for f in os.listdir(data_path) if f.startswith("simulated_tracks") and f.endswith(".json")]
    files.sort(reverse=True)
    latest_file = os.path.join(data_path, files[0])

    with open(latest_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    print(f"Chargé : {latest_file} – {len(tracks)} morceaux")

    # 🔧 Ajout des audio_features simulés
    enriched = []
    for track in tracks:
        genres = track.get("genres", [])
        genre = genres[0] if genres else "rap"
        features = generate_mock_features_by_genre(genre)
        track.update(features)
        track["session_id"] = session_id
        enriched.append(track)

    save_json(enriched, data_path, prefix="enriched_simulated")
    print(f"{len(enriched)} morceaux enrichis avec features simulés")

if __name__ == "__main__":
    main()
