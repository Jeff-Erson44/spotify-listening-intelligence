import os
import json
from spotify_api.auth import get_spotify_client_oauth
from spotify_api.audio_features import get_audio_features_in_batches
from utils.file_writer import save_json

DATA_DIR = "app/data/user"
SCOPE = "user-read-recently-played"

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith("json")]
    files.sort(reverse=True)
    return os.path.join(directory, files[0]) if files else None 

def extract_track_id(data):
    return [
        item["track"]["id"]
        for item in data
        if item.get("track") and item["track"].get("id")
    ]
    
def main():
    latest_file = get_latest_file(DATA_DIR)
    if not latest_file:
        print("Aucun fichier trouvé")
        return
    print(f"Fichier chargé: {latest_file}")
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    track_id = extract_track_id(data)
    print(f"{len(track_id)} tracks à enrichir")
    
    sp = get_spotify_client_oauth(scope=SCOPE)
    audio_features = get_audio_features_in_batches(sp, track_id)
    
    #chaque morceau assoiver a ses features
    associate = []
    for item, features in zip(data, audio_features):
        if features:
            associate.append({
                "track_name" : item["track"]["name"],
                "artist_name": item["track"]["artists"][0]["name"],
                "played_at": item["played_at"],
                "id": item["track"]["id"],
                **features
            })
    
    save_json(associate, DATA_DIR, prefix="enriched_tracks")

if __name__ == "__main__":
    main()
