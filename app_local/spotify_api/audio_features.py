def get_audio_features_in_batches(sp, track_id, batch_size=50):
    #Récupère les audios_features poir une liste via Spotipy en batchs
    
    features = []
    for i in range(0, len(track_id), batch_size):
        batch = track_id[i:i + batch_size]
        batch_features = sp.audio_features(batch)
        features.extend(batch_features)
    return features
        