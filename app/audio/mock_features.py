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
    "new wave":    {"danceability": (0.6, 0.85), "energy": (0.6, 0.9), "valence": (0.4, 0.7), "speechiness": (0.03, 0.07)}
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
    "post-punk": "new wave"
}

DEFAULT_GENRE = "pop"

def generate_mock_features_by_genre(genre_or_artist):
    key = genre_or_artist.lower()
    genre = GENRE_FALLBACKS.get(key, key)
    profile = GENRE_PROFILES.get(genre, GENRE_PROFILES[DEFAULT_GENRE])
    return {
        "danceability": round(random.uniform(*profile["danceability"]), 3),
        "energy": round(random.uniform(*profile["energy"]), 3),
        "valence": round(random.uniform(*profile["valence"]), 3),
        "speechiness": round(random.uniform(*profile["speechiness"]), 3),
        "tempo": round(random.uniform(70, 160), 2),
        "acousticness": round(random.uniform(0.0, 0.3), 3),
        "instrumentalness": round(random.uniform(0.0, 0.2), 3),
        "liveness": round(random.uniform(0.1, 0.6), 3)
    }
