def map_emotion(valence, energy, danceability):
    if valence >= 0.7 and energy >= 0.7:
        return "euphorie / joie"
    elif valence >= 0.7 and energy < 0.5:
        return "sérénité / détente"
    elif 0.5 <= valence < 0.7 and energy >= 0.7:
        return "enthousiasme / dynamisme"
    elif 0.5 <= valence < 0.7 and 0.5 <= energy < 0.7:
        return "confiance / motivation"
    elif valence >= 0.6 and danceability >= 0.85:
        return "envie de danser / groove"
    elif valence < 0.4 and energy < 0.4:
        return "tristesse / solitude"
    elif valence < 0.4 and energy >= 0.7:
        return "colère / tension"
    elif valence < 0.4 and 0.4 <= energy < 0.7:
        return "mélancolie / introspection"
    elif 0.4 <= valence < 0.6 and danceability >= 0.75:
        return "nostalgie / douceur"
    elif danceability >= 0.85 and energy >= 0.6:
        return "fête / excitation"
    else:
        return "neutre / équilibré"