import os
import json
import boto3
from botocore.exceptions import ClientError
from collections import Counter
from statistics import mean
from emotion_mapper import map_emotion

# Couleurs associées aux émotions
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

s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME", "")

def lambda_handler(event, context):
    print("Lambda generate_profile démarrée.")
    print("Événement S3 reçu pour analyse.")

    if not BUCKET_NAME:  
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "BUCKET_NAME environment variable is not set."})
        }

    try:
        session_id = event["Records"][0]["s3"]["object"]["key"].split("/")[1]
        print(f"Session ID extrait : {session_id}")
        key = f"data/{session_id}/enriched_tracks.json"
        print(f"Chemin du fichier enrichi construit : {key}")
    except (KeyError, IndexError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Impossible de récupérer le session_id depuis le chemin S3."})
        }
    
    try:
        print("Récupération du fichier enriched_tracks.json depuis S3...")
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        print("Fichier enriched_tracks.json récupéré avec succès.")
        data = json.loads(response['Body'].read().decode('utf-8'))
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Fichier enriched_tracks.json non trouvé pour cette session."})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    try:
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

        top_emotions = [e for e, _ in emotion_counter.most_common(3)]
        dominant_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else None
        dominant_genre = genre_counter.most_common(1)[0][0] if genre_counter else None
        top_genres = [g for g, _ in genre_counter.most_common(3)]

        # Ajout couleurs 
        emotion_colors = {emotion: EMOTION_COLORS.get(emotion, "#000000") for emotion in top_emotions}

        profile_data = {
            "nb_tracks": len(data),
            "danse_moyenne": round(mean(dances), 3) if dances else 0,
            "energie_moyenne": round(mean(energies), 3) if energies else 0,
            "emotion_globale": dominant_emotion,
            "top_3_emotions": top_emotions,
            "top_4_emotions": [e for e, _ in emotion_counter.most_common(4)],
            "genre_dominant": dominant_genre,
            "top_3_genres": top_genres,
            "description_auto": generate_emotion_description(top_emotions),
            "emotion_colors": emotion_colors,
        }

        print("Enregistrement du profil utilisateur dans S3...")
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"data/{session_id}/profile.json",
            Body=json.dumps(profile_data),
            ContentType="application/json"
        )
        print(f"Profil enregistré avec succès dans S3 à l'emplacement : data/{session_id}/profile.json")

        return {
            "statusCode": 200,
            "body": json.dumps(profile_data)
        }

    except Exception as e:
        print(f"Erreur inattendue : {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }