import os
import json
from collections import Counter
from statistics import mean
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.session_manager import get_active_session
from app.analyze.emotion_mapper import map_emotion
from app.utils.upload_to_s3 import upload_file_to_s3

EMOTION_COLORS = {
    "joie": "#FDD835",
    "détente": "#A3D5FF",
    "enthousiasme": "#FFB74D",
    "motivation": "#FF7043",
    "envie de danser": "#4DB6AC",
    "excitation": "#D81B90",
    "tristesse": "#7986CB",
    "colère": "#EF5350",
    "mélancolie": "#B39DDB",
    "nostalgie": "#F3C6F1",
    "neutre": "#B0BEC5",
    "confiance": "#81C784",
}


def generate_profile_summary() -> dict:
    session_id = get_active_session()
    base_dir = f"data/{session_id}"
    session_path = base_dir

    files = [f for f in os.listdir(session_path) if f.endswith(".json") and ("transform_tracks" in f or "selected_artists" in f)]
    files.sort(reverse=True)

    if not files:
        raise FileNotFoundError(f"Aucun fichier enrichi trouvé pour la session {session_id} dans {session_path}")
    
    file_path = os.path.join(session_path, files[0])
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    emotion_counter = Counter()
    genre_counter = Counter()
    valences, energies, dances = [], [], []

    for track in data:
        valence = track.get("valence", 0)
        energy = track.get("energy", 0)
        dance = track.get("danceability", 0)
        genre = track.get("genres", ["pop"])[0] if track.get("genres") else "pop"

        emotion = map_emotion(valence, energy, dance)

        emotion_counter[emotion] += 1
        genre_counter[genre] += 1

        valences.append(valence)
        energies.append(energy)
        dances.append(dance)

    top_genres = [g for g, _ in genre_counter.most_common(3)]
    top_emotions = [e for e, _ in emotion_counter.most_common(3)]
    dominant_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else None
    dominant_genre = genre_counter.most_common(1)[0][0] if genre_counter else None

    summary = {
        "session_id": session_id,
        "genre_dominant": dominant_genre,
        "top_3_genres": top_genres,
        "danse_moyenne": round(mean(dances), 3) if dances else 0,
        "energie_moyenne": round(mean(energies), 3) if energies else 0,
        "emotion_globale": dominant_emotion,
        "emotions_principales": top_emotions,
        "emotions_dominantes": [e for e, _ in emotion_counter.most_common(4)],
        "couleur_dominante": EMOTION_COLORS.get(dominant_emotion, "#CCCCCC"),
        "emotions_details": [
            {
                "emotion": emotion,
                "color": EMOTION_COLORS.get(emotion, "#CCCCCC")
            }
            for emotion in top_emotions
        ],
    }

    # Génération automatique de description à partir des émotions principales
    def generate_emotion_description(emotions):
        if not emotions or len(emotions) < 3:
            return "Ton univers musical est varié et nuancé, révélant une palette émotionnelle difficile à cerner."
        
        e1, e2, e3 = emotions[0], emotions[1], emotions[2]
        templates = [
            f"Ton paysage sonore oscille entre {e1} et {e2}, avec une touche persistante de {e3}.",
            f"On sent une énergie marquée par {e1}, enrichie par des élans de {e2} et des nuances de {e3}.",
            f"Entre {e1} et {e2}, ta musique trace un chemin intime, ponctué de moments teintés de {e3}.",
            f"Comme une brise émotionnelle, ta playlist parcourt {e1}, frôle {e2} et s’attarde sur {e3}.",
            f"Ton univers musical mélange subtilement {e1}, {e2} et {e3}, créant une atmosphère unique et évocatrice."
        ]
        return templates[hash(e1 + e2 + e3) % len(templates)]

    summary["description_auto"] = generate_emotion_description(top_emotions)

    output_path = os.path.join(session_path, f"profile_summary_{session_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
        
    # Enregistrement dans un bucket S3
    saved_files = [f for f in os.listdir(f"data/{session_id}/") if f.startswith("profile") and f.endswith(".json")]
    if saved_files:
        file_path = os.path.join(f"data/{session_id}/", saved_files[0])
        upload_file_to_s3(
            file_path,
            "spotify-listening-intelligence",
            f"{session_id}/{saved_files[0]}"
        )
        print("Fichier utilisateur uploadé vers S3.")

    return summary
if __name__ == "__main__":
    summary = generate_profile_summary()
    print(json.dumps(summary, indent=4, ensure_ascii=False))        