import os
import json
from utils.upload_to_s3 import upload_file_to_s3
from utils.session import get_spotify_client, get_session_id
from utils.session import reset_session
from spotify_api.search import search_artists
from spotify_api.top_tracks import get_artist_top_tracks

def simulate_artist_selection(market="US", session_id=None):
    reset_session()
    #On verifer que linstance spotify est OK / on vérife et recupere le numero de session / on crée le fichier dans le bon chemin
    sp = get_spotify_client()
    session_id = session_id or get_session_id()
    save_path = f"data/{session_id}"
    os.makedirs(save_path, exist_ok=True)
    
    selected_artists = []
    
    while len(selected_artists) < 10 :
        name = input (f"\n Entrez un nom d'artiste ({len(selected_artists)}/10) :").strip()
        if not name:
            print("Nom d'artiste vide. Réessayez")
            continue
        results = search_artists(sp, name)
        if not results:
            print("Aucun artiste trouvé.")
            continue
        
        print("\n Résultat de recherche :")
        for i, artist in enumerate(results):
            genres = artist['genres'] if artist['genres'] else ['pop']
            print(f"[{i}] {artist['name']} - Genre: {', '.join(genres)}")
            
        try:
            index = int(input("Sélectionnez l'artiste voulu (0-4) : "))
            if index < 0 or index >= len(results):
                raise IndexError
            selected = results[index]
        except (ValueError, IndexError):
            print("Sélection invalide.")
            continue

        selected_artists.append(selected)
        selected["top_tracks"] = get_artist_top_tracks(sp, selected["id"])
        print(f"Ajouté : {selected['name']}")

        if len(selected_artists) >= 5:
            again = input("Ajouter un autre artiste ? (y/n) ").strip().lower()
            if again != "y":
                break
            
    output_file = os.path.join(save_path, "selected_artists.json")
    with open(output_file, "w") as f:
        cleaned_artists = [
            {
                "name": artist["name"],
                "genres": artist["genres"] if artist["genres"] else ["pop"],
                "id": artist["id"],
                "top_tracks": artist.get("top_tracks", [])
            }
            for artist in selected_artists
        ]
        json.dump(cleaned_artists, f, indent=2)

    print(f"\n {len(selected_artists)} artistes sauvegardés dans {output_file}")
    
    
    # Enregistrement dans un bucket S3
    saved_files = [f for f in os.listdir(f"data/{session_id}/") if f.startswith("selected_artist") and f.endswith(".json")]
    if saved_files:
        file_path = os.path.join(f"data/{session_id}/", saved_files[0])
        upload_file_to_s3(
            file_path,
            "spotify-listening-intelligence",
            f"{session_id}/{saved_files[0]}"
        )
        print("Fichier utilisateur uploadé vers S3.")
if __name__ == "__main__":
    simulate_artist_selection()