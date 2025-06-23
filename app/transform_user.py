import json
from utils.file_writer import save_json
from audio.mock_features import generate_mock_features_by_genre
import os
from utils.upload_to_s3 import upload_file_to_s3
from utils.session_manager import get_active_session

session_id = get_active_session()
if not session_id:
    raise ValueError("Aucune session active trouvée. Veuillez lancer une extraction d'abord.")
print(f"Session active détectée : {session_id}")
data_path = f"data/{session_id}/"

def main():
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Le dossier {data_path} n'existe pas. Vérifiez la session ou relancez une extraction.")
    files = [f for f in os.listdir(data_path) if f.endswith(".json")]
    input_file = None
    # mode = "user"

    for prefix in ["recently_played", "selected_artists"]:
        matching_files = [f for f in files if f.startswith(prefix)]
        if matching_files:
            input_file = os.path.join(data_path, matching_files[0])
            break

    if not input_file:
        raise FileNotFoundError(f"Aucun fichier d'entrée valide trouvé dans {data_path}")

    with open(input_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    print(f"Chargé : {input_file} – {len(tracks)} morceaux")

    #  Ajout des audio_features 
    enriched = []
    for track in tracks:
        genres = track.get("genres", [])
        if not genres:
            genres = ["pop"]  # valeur par défaut si aucun genre
        genre = genres[0]
        features = generate_mock_features_by_genre(genre)
        track.update(features)
        track["session_id"] = session_id
        enriched.append(track)

    save_json(enriched, data_path, prefix="enriched")
    enriched_filename = [f for f in os.listdir(data_path) if f == "enriched.json"]
    if enriched_filename:
        print(f"✅ Données sauvegardées dans : {os.path.join(data_path, enriched_filename[0])}")
        upload_file_to_s3(
            os.path.join(data_path, enriched_filename[0]),
            "spotify-listening-intelligence",
            f"{session_id}/{enriched_filename[0]}"
        )
    print(f"{len(enriched)} morceaux enrichis avec features simulés")

if __name__ == "__main__":
    main()