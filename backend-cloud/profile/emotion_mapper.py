def map_emotion(valence, energy, danceability):
    scores = {
        "joie": 0,
        "détente": 0,
        "enthousiasme": 0,
        "motivation": 0,
        "envie de danser": 0,
        "excitation": 0,
        "tristesse": 0,
        "colère": 0,
        "mélancolie": 0,
        "nostalgie": 0,
        "confiance": 0,
        "neutre": 0
    }

    # Analyse des seuils individuels
    if valence >= 0.75:
        scores["joie"] += 2
        if energy < 0.5:
            scores["détente"] += 1
        if energy >= 0.75:
            scores["joie"] += 1
            scores["excitation"] += 1

    if 0.6 <= valence < 0.75:
        scores["enthousiasme"] += 1
        if energy >= 0.75:
            scores["enthousiasme"] += 1
        if energy >= 0.5:
            scores["motivation"] += 1

    # Ajout de confiance : valence modérée à haute, énergie modérée
    if 0.55 <= valence <= 0.75 and 0.4 <= energy <= 0.7:
        scores["confiance"] += 2

    if valence < 0.4:
        scores["tristesse"] += 1
        if energy >= 0.75:
            scores["colère"] += 2
        elif 0.4 <= energy < 0.75:
            scores["mélancolie"] += 2

    if 0.4 <= valence < 0.6 and 0.4 <= energy < 0.7:
        scores["nostalgie"] += 1

    if danceability >= 0.85 and energy >= 0.6 and valence >= 0.6:
        scores["envie de danser"] += 2
    if danceability >= 0.9 and energy >= 0.75:
        scores["excitation"] += 1

    if danceability >= 0.6 and valence >= 0.5:
        scores["motivation"] += 1

    best_emotion = max(scores, key=scores.get)
    if scores[best_emotion] == 0:
        return "neutre"
    return best_emotion