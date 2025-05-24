import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime

#Charger les variables d'environnement
load_dotenv () 

# Créer un client Spotipy avec authentification OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-recently-played user-top-read",
    show_dialog=True
))

print("Authentifcation réussie")


###PROFIL#####

# #Afficher les infos d'un user
user = sp.current_user()
print(user["display_name"])

if user["images"]:
    print("Photo de profil URL:", user["images"][0]["url"])
else : 
    print("Pas de photo")


# #Afficher les artites préféres d'un user

# ## Top artiste 
artist_short = sp.current_user_top_artists(time_range='short_term')
artist_medium = sp.current_user_top_artists(time_range='medium_term')
artist_long = sp.current_user_top_artists(time_range='long_term')

print("Top short-term:", artist_short["items"][0]["name"])
print("Top medium-term:", artist_medium["items"][0]["name"])
print("Top long-term:", artist_long["items"][0]["name"])

#Afficher les sons préféres d'un user

## Top sons
song_short=sp.current_user_top_tracks(time_range='short_term')
song_medium=sp.current_user_top_tracks(time_range='medium_term')
song_long=sp.current_user_top_tracks(time_range='long_term')

print("Song short-term;", song_short["items"][0]["name"])
print("Song medium-term;", song_medium["items"][0]["name"])
print("Song long-term;", song_long["items"][0]["name"])

## FETCH les 50 DERNIERS SONS

#Récupérer les dernières ecoutes via Spotipy qui simule la requete API 
results = sp.current_user_recently_played(limit=50)

#Crée un fichier
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/recently_played_{timestamp}.json"

#Sauvegarde du fichier
with open(filename, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)
    
print(f"Données sauvegardé dans : {filename}")





