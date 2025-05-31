def search_artist(sp, name, market="FR", limit=5):
    """Recherche d'artistes par nom et retourne une liste de suggestions"""
    results = sp.search(q=name, type="artist", limit=limit, market=market)
    artists = results.get("artists", {}).get("items", [])
    return [
        {
            "name": a["name"],
            "id": a["id"],
            "genres": a.get("genres", []),
            "popularity": a.get("popularity"),
            "followers": a.get("followers", {}).get("total", 0)
        }
        for a in artists
    ]


def search_track_id(sp, track_name, artist_name, market="FR"):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type="track", limit=1, market=market)

    items = results.get("tracks", {}).get("items", [])
    if not items:
        return None
    return items[0]["id"]


# Fonction d'affichage et de sélection d'artiste par l'utilisateur
def prompt_user_to_select(artist_results, user_input=None):
    if not artist_results:
        return None

    # Sélection automatique si le premier résultat est très populaire et correspond bien
    if user_input:
        first = artist_results[0]
        if first["name"].lower() == user_input.lower() and first["followers"] > 1_000_000:
            print(f"Sélection automatique : {first['name']} (followers: {first['followers']})")
            return first["id"]

    print("\nArtistes trouvés :")
    for i, a in enumerate(artist_results):
        print(f"[{i}] {a['name']} – Genres: {', '.join(a['genres']) or 'Aucun genre'} – {a['followers']} followers")
    try:
        choice = int(input("Sélectionne l’artiste (index) : "))
        return artist_results[choice]["id"]
    except (IndexError, ValueError):
        print("Sélection invalide.")
        return None