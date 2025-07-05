def get_recent_tracks(sp, limit=50):
    #Récupère les derniers morceaux écoutés par l'utilisateur
    results = sp.current_user_recently_played(limit=50)
    return results.get('items', [])