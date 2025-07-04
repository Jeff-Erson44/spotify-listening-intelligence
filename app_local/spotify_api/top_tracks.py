def get_artist_top_tracks(sp, artist_id, limit=5):

    #Retourne les meilleurs morceaux d’un artiste donné .

    try:
        results = sp.artist_top_tracks(artist_id)
        tracks = results.get("tracks", [])[:limit]

        formatted = []
        for track in tracks:
            formatted.append({
                "track_name": track["name"],
                "track_id": track["id"],
                "artist_name": track["artists"][0]["name"]
            })
        return formatted

    except Exception as e:
        print(f" Erreur récupération top tracks pour l’artiste {artist_id} : {e}")
        return []