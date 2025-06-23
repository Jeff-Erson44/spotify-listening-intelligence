from spotipy import Spotify
from typing import List, Dict

def search_artists(sp: Spotify, artist_name: str) -> List[Dict]:
    #Recherche les 5 artistes les plus pertinents sur Spotify pour un artiste recherché.
    
    results = sp.search(q=artist_name, type="artist", limit=5)
    artists = results.get("artists", {}).get("items", [])
    
    artist_data = []
    for artist in artists:
        artist_data.append({
            "id": artist.get("id"),
            "name": artist.get("name"),
            "genres": artist.get("genres") if artist.get("genres") else ["pop"],
            "image_url": artist.get("images")[0]["url"] if artist.get("images") else None
        })
    
    return artist_data