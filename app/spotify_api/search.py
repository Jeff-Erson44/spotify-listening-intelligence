def search_artist(sp, name, market="FR"):
    "Recherche d'un artiste par son nom et retourner son ID Spotify"
    results = sp.search(q=name, type="artist", limit=1, market=market)
    items= results.get("artists", {}).get("items", [])
    
    if not items:
        print(f"Aucun artiste trouvé pour: {name}")
        return None
    
    artist = items[0]
    print(f"{name} → ID : {artist['id']} ({artist['name']})")
    return artist["id"]


