import os
import json
from spotify_api.auth import get_spotify_client_oauth
from spotify_api.audio_features import get_audio_features_in_batches
from utils.file_writer import save_json
from utils.session import get_session_id

SCOPE = "user-read-recently-played"

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".json")]
    files.sort(reverse=True)
    return os.path.join(directory, files[0]) if files else None 

def extract_track_id(data):
    return [
        item["track"]["id"]
        for item in data
        if item.get("track") and item["track"].get("id")
    ]
    
def main():
    session_id = get_session_id()
    data_path = f"app/data/user/{session_id}/"

    latest_file = get_latest_file(data_path)
    if not latest_file:
        print("Aucun fichier trouvé dans la session.")
        return
    
    print(f"Fichier chargé: {latest_file}")
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    track_ids = extract_track_id(data)
    print(f"{len(track_ids)} morceaux à enrichir")
    
    sp = get_spotify_client_oauth(scope=SCOPE)
    audio_features = get_audio_features_in_batches(sp, track_ids)
    
    associate = []
    for item, features in zip(data, audio_features):
        if features:
            associate.append({
                "track_name" : item["track"]["name"],
                "artist_name": item["track"]["artists"][0]["name"],
                "played_at": item["played_at"],
                "id": item["track"]["id"],
                **features,
                "session_id": session_id
            })
    
    save_json(associate, directory=data_path, prefix="enriched_user")
    print(f"{len(associate)} morceaux enrichis avec succès")

if __name__ == "__main__":
    main()
