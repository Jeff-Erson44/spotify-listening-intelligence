import random

# Profils par genre Spotify
GENRE_PROFILES = {
    "choral":      {"danceability": (0.1, 0.3), "energy": (0.1, 0.4), "valence": (0.3, 0.6), "speechiness": (0.01, 0.03)},
    "brazilian":   {"danceability": (0.7, 0.95), "energy": (0.6, 0.85), "valence": (0.6, 0.9), "speechiness": (0.03, 0.1)},
    "grime":       {"danceability": (0.6, 0.8), "energy": (0.7, 0.95), "valence": (0.2, 0.5), "speechiness": (0.5, 0.9)},
    "german indie":{"danceability": (0.4, 0.75), "energy": (0.4, 0.7), "valence": (0.3, 0.7), "speechiness": (0.03, 0.08)},
    "amapiano":    {"danceability": (0.85, 0.97), "energy": (0.4, 0.65), "valence": (0.5, 0.75), "speechiness": (0.02, 0.05)},
    "hip-hop":     {"danceability": (0.6, 0.9), "energy": (0.6, 0.85), "valence": (0.2, 0.5), "speechiness": (0.6, 0.9)},
    "rap":         {"danceability": (0.6, 0.85), "energy": (0.6, 0.9), "valence": (0.2, 0.6), "speechiness": (0.5, 0.9)},
    "drill":       {"danceability": (0.5, 0.75), "energy": (0.7, 1.0), "valence": (0.1, 0.4), "speechiness": (0.6, 0.9)},
    "trap":        {"danceability": (0.65, 0.9), "energy": (0.5, 0.8), "valence": (0.3, 0.6), "speechiness": (0.4, 0.7)},
    "afrobeat":    {"danceability": (0.75, 0.95), "energy": (0.6, 0.85), "valence": (0.6, 0.9), "speechiness": (0.2, 0.5)},
    "afropop":     {"danceability": (0.7, 0.95), "energy": (0.5, 0.8), "valence": (0.6, 0.9), "speechiness": (0.2, 0.4)},
    "dance":       {"danceability": (0.7, 0.95), "energy": (0.7, 0.95), "valence": (0.6, 0.9), "speechiness": (0.03, 0.07)},
    "edm":         {"danceability": (0.65, 0.95), "energy": (0.8, 1.0), "valence": (0.5, 0.9), "speechiness": (0.03, 0.08)},
    "electronic":  {"danceability": (0.6, 0.9), "energy": (0.6, 0.9), "valence": (0.4, 0.7), "speechiness": (0.02, 0.06)},
    "house":       {"danceability": (0.7, 0.95), "energy": (0.75, 0.95), "valence": (0.5, 0.8), "speechiness": (0.03, 0.07)},
    "techno":      {"danceability": (0.6, 0.85), "energy": (0.8, 1.0), "valence": (0.2, 0.5), "speechiness": (0.02, 0.05)},
    "classical":   {"danceability": (0.1, 0.4), "energy": (0.1, 0.4), "valence": (0.3, 0.6), "speechiness": (0.01, 0.03)},
    "jazz":        {"danceability": (0.4, 0.7), "energy": (0.3, 0.6), "valence": (0.4, 0.7), "speechiness": (0.02, 0.05)},
    "r-n-b":       {"danceability": (0.6, 0.9), "energy": (0.4, 0.7), "valence": (0.4, 0.7), "speechiness": (0.1, 0.4)},
    "soul":        {"danceability": (0.6, 0.85), "energy": (0.4, 0.7), "valence": (0.5, 0.8), "speechiness": (0.05, 0.2)},
    "funk":        {"danceability": (0.7, 0.95), "energy": (0.6, 0.85), "valence": (0.5, 0.8), "speechiness": (0.04, 0.1)},
    "reggae":      {"danceability": (0.65, 0.9), "energy": (0.5, 0.7), "valence": (0.6, 0.9), "speechiness": (0.03, 0.07)},
    "reggaeton":   {"danceability": (0.75, 0.95), "energy": (0.7, 0.95), "valence": (0.6, 0.9), "speechiness": (0.1, 0.4)},
    "pop":         {"danceability": (0.6, 0.85), "energy": (0.6, 0.85), "valence": (0.5, 0.9), "speechiness": (0.03, 0.1)},
    "rock":        {"danceability": (0.4, 0.7), "energy": (0.6, 0.9), "valence": (0.3, 0.7), "speechiness": (0.05, 0.1)},
    "metal":       {"danceability": (0.3, 0.6), "energy": (0.8, 1.0), "valence": (0.1, 0.4), "speechiness": (0.05, 0.1)},
    "indie":       {"danceability": (0.4, 0.75), "energy": (0.4, 0.7), "valence": (0.3, 0.7), "speechiness": (0.03, 0.08)},
    "ambient":     {"danceability": (0.2, 0.5), "energy": (0.1, 0.4), "valence": (0.2, 0.5), "speechiness": (0.01, 0.03)},
    "chill":       {"danceability": (0.5, 0.8), "energy": (0.3, 0.6), "valence": (0.4, 0.7), "speechiness": (0.01, 0.05)},
    "k-pop":       {"danceability": (0.6, 0.85), "energy": (0.7, 0.95), "valence": (0.6, 0.9), "speechiness": (0.03, 0.08)},
    "phonk":       {"danceability": (0.5, 0.75), "energy": (0.6, 0.85), "valence": (0.2, 0.5), "speechiness": (0.4, 0.7)},
    "cloud rap":   {"danceability": (0.6, 0.85), "energy": (0.4, 0.7), "valence": (0.3, 0.6), "speechiness": (0.5, 0.8)},
    "gospel":      {"danceability": (0.5, 0.75), "energy": (0.3, 0.6), "valence": (0.7, 0.95), "speechiness": (0.05, 0.15)},
    "coupé-décalé":{"danceability": (0.8, 0.98), "energy": (0.6, 0.9), "valence": (0.7, 0.95), "speechiness": (0.05, 0.1)},
    "ndombolo":    {"danceability": (0.85, 0.99), "energy": (0.6, 0.85), "valence": (0.6, 0.95), "speechiness": (0.03, 0.08)},
    "afrohouse":   {"danceability": (0.8, 0.95), "energy": (0.7, 0.9), "valence": (0.5, 0.85), "speechiness": (0.03, 0.06)},
    "soft pop":    {"danceability": (0.6, 0.85), "energy": (0.4, 0.7), "valence": (0.5, 0.8), "speechiness": (0.03, 0.08)},
    "azonto":      {"danceability": (0.85, 0.98), "energy": (0.6, 0.85), "valence": (0.7, 0.95), "speechiness": (0.05, 0.15)},
    "jersey":      {"danceability": (0.85, 0.98), "energy": (0.7, 0.95), "valence": (0.5, 0.8), "speechiness": (0.04, 0.1)},
    "new wave":    {"danceability": (0.6, 0.85), "energy": (0.6, 0.9), "valence": (0.4, 0.7), "speechiness": (0.03, 0.07)},
    "rumba congolaise": {"danceability": (0.7, 0.9), "energy": (0.4, 0.65), "valence": (0.6, 0.9), "speechiness": (0.02, 0.05)},
    "soukous": {"danceability": (0.85, 0.98), "energy": (0.6, 0.85), "valence": (0.7, 0.95), "speechiness": (0.03, 0.06)},
    "ndombolo congolais": {"danceability": (0.85, 0.99), "energy": (0.6, 0.85), "valence": (0.6, 0.95), "speechiness": (0.03, 0.08)},
    "rumba": {"danceability": (0.6, 0.85), "energy": (0.4, 0.7), "valence": (0.6, 0.9), "speechiness": (0.02, 0.05)},
    "bongo flava": {"danceability": (0.75, 0.95), "energy": (0.6, 0.85), "valence": (0.6, 0.9), "speechiness": (0.05, 0.2)},
    "highlife": {"danceability": (0.8, 0.95), "energy": (0.5, 0.7), "valence": (0.7, 0.95), "speechiness": (0.02, 0.06)},
    "mbalax": {"danceability": (0.8, 0.98), "energy": (0.7, 0.9), "valence": (0.6, 0.85), "speechiness": (0.03, 0.06)},
    "gqom": {"danceability": (0.7, 0.9), "energy": (0.8, 1.0), "valence": (0.3, 0.6), "speechiness": (0.02, 0.05)},
    "kwaito": {"danceability": (0.75, 0.95), "energy": (0.6, 0.85), "valence": (0.5, 0.8), "speechiness": (0.03, 0.06)},
    "ethio-jazz": {"danceability": (0.6, 0.85), "energy": (0.4, 0.6), "valence": (0.5, 0.8), "speechiness": (0.03, 0.07)},
    "sertanejo": {"danceability": (0.6, 0.85), "energy": (0.4, 0.7), "valence": (0.5, 0.85), "speechiness": (0.03, 0.07)},
    "forró": {"danceability": (0.7, 0.9), "energy": (0.6, 0.85), "valence": (0.6, 0.9), "speechiness": (0.02, 0.05)},
    "cumbia": {"danceability": (0.75, 0.95), "energy": (0.6, 0.85), "valence": (0.7, 0.95), "speechiness": (0.02, 0.06)},
    "shoegaze": {"danceability": (0.3, 0.5), "energy": (0.3, 0.6), "valence": (0.2, 0.5), "speechiness": (0.02, 0.05)},
    "dream pop": {"danceability": (0.4, 0.6), "energy": (0.3, 0.5), "valence": (0.3, 0.6), "speechiness": (0.02, 0.05)},
    "math rock": {"danceability": (0.4, 0.6), "energy": (0.5, 0.75), "valence": (0.3, 0.6), "speechiness": (0.03, 0.06)},
    "city pop": {"danceability": (0.6, 0.85), "energy": (0.5, 0.75), "valence": (0.6, 0.9), "speechiness": (0.03, 0.06)},
    "j-pop": {"danceability": (0.6, 0.85), "energy": (0.6, 0.9), "valence": (0.5, 0.85), "speechiness": (0.02, 0.06)},
    "j-rock": {"danceability": (0.5, 0.75), "energy": (0.7, 0.95), "valence": (0.4, 0.7), "speechiness": (0.02, 0.06)},
    "bhangra": {"danceability": (0.75, 0.95), "energy": (0.7, 0.95), "valence": (0.6, 0.9), "speechiness": (0.03, 0.06)},
    "carnatic": {"danceability": (0.2, 0.4), "energy": (0.3, 0.6), "valence": (0.3, 0.6), "speechiness": (0.01, 0.04)},
    "bollywood": {"danceability": (0.6, 0.85), "energy": (0.5, 0.75), "valence": (0.6, 0.9), "speechiness": (0.03, 0.07)},
    "trance": {"danceability": (0.7, 0.9), "energy": (0.8, 1.0), "valence": (0.6, 0.9), "speechiness": (0.02, 0.05)},
    "vaporwave": {"danceability": (0.4, 0.7), "energy": (0.3, 0.6), "valence": (0.3, 0.6), "speechiness": (0.02, 0.05)},
    "ska": {"danceability": (0.7, 0.9), "energy": (0.6, 0.85), "valence": (0.6, 0.9), "speechiness": (0.03, 0.07)},
    "tango": {"danceability": (0.5, 0.75), "energy": (0.4, 0.7), "valence": (0.4, 0.7), "speechiness": (0.02, 0.06)},
    "fado": {"danceability": (0.2, 0.4), "energy": (0.3, 0.5), "valence": (0.2, 0.5), "speechiness": (0.01, 0.03)},
    "klezmer": {"danceability": (0.6, 0.85), "energy": (0.5, 0.75), "valence": (0.5, 0.8), "speechiness": (0.02, 0.06)},
    "shatta": {"danceability": (0.8, 0.95), "energy": (0.6, 0.85), "valence": (0.4, 0.7), "speechiness": (0.02, 0.06)},
    "laïko": {"danceability": (0.6, 0.8), "energy": (0.5, 0.75), "valence": (0.3, 0.6), "speechiness": (0.02, 0.06)},
    "rap québécois": {"danceability": (0.7, 0.9), "energy": (0.7, 0.95), "valence": (0.3, 0.6), "speechiness": (0.02, 0.06)},
}


# Mapping secondaire pour rediriger les genres inconnus
GENRE_FALLBACKS = {
    "brazilian trap": "trap",
    "brazilian funk": "funk",
    "german rap": "rap",
    "german hip hop": "hip-hop",
    "german pop": "pop",
    "german rock": "rock",
    "french rap": "rap",
    "boom bap": "hip-hop",
    "synthpop": "pop",
    "urban": "r-n-b",
    "bass music": "edm",
    "deep house": "house",
    "emo rap": "rap",
    "lo-fi": "chill",
    "latin": "reggaeton",
    "melodic rap": "trap",
    "electropop": "pop",
    "softpop": "soft pop",
    "azonto": "azonto",
    "fun rock": "rock",
    "jersey club": "jersey",
    "baltimore club": "jersey",
    "philly club": "jersey",
    "newwave": "new wave",
    "synthwave": "new wave",
    "post-punk": "new wave",
    "congolese rumba": "rumba congolaise",
    "ndombolo": "ndombolo congolais",
    "rumba zairoise": "rumba congolaise",
    "afrotrap": "rap",
    "afrodrill": "drill",
    "pagode": "brazilian",
    "axé": "brazilian",
    "nueva canción": "latin",
    "musica andina": "latin",
    "bluegrass": "folk",
    "alt-country": "folk",
    "enka": "j-pop",
    "hindustani": "classical",
    "desi hip hop": "rap",
    "breakbeat": "edm",
    "psytrance": "trance",
    "electro swing": "edm",
    "neoclassical": "classical",
    "vapor trap": "trap",
    "zydeco": "folk",
    "punk": "rock",
    "industrial": "electronic",
    "citypop": "city pop",
    "french hip hop": "hip hop",
    "canadian hip hop": "hip hop"
}


def generate_mock_features_by_genre(genre_or_artist):
    key = genre_or_artist.lower()

    # 1. Fallback explicite
    genre = GENRE_FALLBACKS.get(key)

    # 2. Matching partiel par mot-clé uniquement si le genre n’est pas connu
    if not genre:
        if "drill" in key and not genre and "drill" in GENRE_PROFILES:
            genre = "drill"
        elif "trap" in key and not genre and "trap" in GENRE_PROFILES:
            genre = "trap"
        elif "pop" in key and not genre and "pop" in GENRE_PROFILES:
            genre = "pop"
        elif "house" in key and not genre and "house" in GENRE_PROFILES:
            genre = "house"
        elif "funk" in key and not genre and "funk" in GENRE_PROFILES:
            genre = "funk"
        elif "rock" in key and not genre and "rock" in GENRE_PROFILES:
            genre = "rock"
        elif "soul" in key and not genre and "soul" in GENRE_PROFILES:
            genre = "soul"
        elif (("rnb" in key or "r&b" in key) and not genre and "r-n-b" in GENRE_PROFILES):
            genre = "r-n-b"
        elif "edm" in key and not genre and "edm" in GENRE_PROFILES:
            genre = "edm"
        elif "afro" in key and not genre and "afrobeat" in GENRE_PROFILES:
            genre = "afrobeat"
        elif "electro" in key and not genre and "electronic" in GENRE_PROFILES:
            genre = "electronic"
        elif (("lofi" in key or "lo-fi" in key) and not genre and "chill" in GENRE_PROFILES):
            genre = "chill"
        elif (("classical" in key or "baroque" in key) and not genre and "classical" in GENRE_PROFILES):
            genre = "classical"
        elif "jazz" in key and not genre and "jazz" in GENRE_PROFILES:
            genre = "jazz"
        else:
            genre = key  # fallback final

    # 3. Vérifie si le genre est maintenant dans les profils
    if genre not in GENRE_PROFILES:
        raise ValueError(f"Genre inconnu : {genre}")

    # 4. Génère les features
    profile = GENRE_PROFILES[genre]
    return {
        "danceability": round(random.uniform(*profile["danceability"]), 3),
        "energy": round(random.uniform(*profile["energy"]), 3),
        "valence": round(random.uniform(*profile["valence"]), 3),
        "speechiness": round(random.uniform(*profile["speechiness"]), 3),
    }
