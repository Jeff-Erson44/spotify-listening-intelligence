import os
import json
from collections import Counter
from statistics import mean
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.session import get_session_id
from app.analyze.emotion_mapper import map_emotion
from app.utils.upload_to_s3 import upload_file_to_s3

EMOTION_COLORS = {
    "euphorie / joie": "#FFD700",
    "sérénité / détente": "#ADD8E6",
    "enthousiasme / dynamisme": "#FFA500",
    "confiance / motivation": "#FF8C00",
    "envie de danser / groove": "#00FF7F",
    "tristesse / solitude": "#00008B",
    "colère / tension": "#FF0000",
    "mélancolie / introspection": "#800080",
    "nostalgie / douceur": "#FFC0CB",
    "fête / excitation": "#FF69B4",
    "neutre / équilibré": "#C0C0C0"
}

def generate_profile_summary(session_id: str, mode: str = "user") -> dict:
    base_dir = f"app/data/{mode}"
    prefix = "enriched_user" if mode == "user" else "enriched_simulated"
    session_path = os.path.join(base_dir, session_id)
    
    files = [f for f in os.listdir(session_path) if f.startswith(prefix) and f.endswith(".json")]
    files.sort(reverse=True)
    
    if not files:
        raise FileNotFoundError(f"Aucun fichier enrichi trouvé pour la session {session_id} dans {mode}")
    
    file_path = os.path.join(session_path, files[0])
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    from collections import defaultdict

    genre_stats = defaultdict(lambda: {"valence": [], "energy": [], "danceability": []})

    for track in data:
        genre = track.get("genres", ["pop"])
        genre = genre[0] if genre else "pop"

        genre_stats[genre]["valence"].append(track.get("valence", 0))
        genre_stats[genre]["energy"].append(track.get("energy", 0))
        genre_stats[genre]["danceability"].append(track.get("danceability", 0))

    summary = {
        "session_id": session_id,
        "genres": []
    }

    unique_genres = {}
    for genre, stats in genre_stats.items():
        genre_key = genre.lower()
        if genre_key not in unique_genres:
            avg_valence = round(mean(stats["valence"]), 3)
            avg_energy = round(mean(stats["energy"]), 3)
            avg_dance = round(mean(stats["danceability"]), 3)
            emotion = map_emotion(avg_valence, avg_energy, avg_dance)
            unique_genres[genre_key] = {
                "genre": genre,
                "average_valence": avg_valence,
                "average_energy": avg_energy,
                "average_danceability": avg_dance,
                "emotion": emotion
            }

    summary["genres"] = list(unique_genres.values())

     # Sauvegarde en local
    output_path = os.path.join(session_path, f"profile_summary_{session_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)

    # Upload vers S3
    s3_key = f"{mode}/{session_id}/profile_summary_{session_id}.json"
    upload_file_to_s3(output_path, "spotify-listening-intelligence", s3_key)

    return summary
if __name__ == "__main__":
    session_id = get_session_id()
    user_path = os.path.join("app/data/user", session_id)
    simulated_path = os.path.join("app/data/simulated", session_id)

    if os.path.exists(user_path):
        mode = "user"
    elif os.path.exists(simulated_path):
        mode = "simulated"
    else:
        raise FileNotFoundError(f"Aucun dossier trouvé pour la session {session_id} dans 'user' ou 'simulated'.")

    summary = generate_profile_summary(session_id, mode)
    print(json.dumps(summary, indent=4))

    # Affichage des émotions détectées
    print(" Émotions détectées :")
    printed_emotions = set()
    for genre_summary in summary["genres"]:
        emotion = genre_summary["emotion"]
        if emotion not in printed_emotions:
            print(f"• {emotion}")
            color = EMOTION_COLORS.get(emotion, "#CCCCCC")
            print(f"  → Couleur associée : {color}")
            printed_emotions.add(emotion)