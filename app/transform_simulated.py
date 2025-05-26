import json
import os
from utils.file_writer import save_json
from audio.mock_features import generate_mock_features_by_genre

def main():
    # Charge le dernier fichier simulé
    data_dir = "app/data/simulated/"
    files = [f for f in os.listdir(data_dir) if f.startswith("simulated_tracks") and f.endswith(".json")]
    files.sort(reverse=True)
    latest_file = os.path.join(data_dir, files[0])

    with open(latest_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    print(f"✅ Chargé : {latest_file} – {len(tracks)} morceaux")

    # 🔧 Ajout des audio_features simulés
    enriched = []
    for track in tracks:
        genres = track.get("genres", [])
        genre = genres[0] if genres else "rap"
        features = generate_mock_features_by_genre(genre)
        enriched.append({**track, **features})

    save_json(enriched, "app/data/simulated/", prefix="enriched_simulated")
    print(f"✨ {len(enriched)} morceaux enrichis avec features simulés")

if __name__ == "__main__":
    main()
