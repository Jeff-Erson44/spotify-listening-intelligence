# Ce fichier définit le point d'entrée Lambda pour la recherche d'artistes Spotify via une requête HTTP.
import logging
import json
from utils.auth import get_spotify_client_credentials

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query")
        headers = {k.lower(): v for k, v in event.get("headers", {}).items()}
        session_id = headers.get("x-session-id")
        if not session_id:
            logger.warning("Header 'x-session-id' absent des en-têtes de la requête.")
            return {"statusCode": 400, "body": json.dumps({"error": "Header 'x-session-id' manquant."})}
        if not query:
            return {"statusCode": 400, "body": json.dumps({"error": "Paramètre 'query' requis."})}

        logger.info(f"Recherche d'artistes pour la requête : {query}")

        sp = get_spotify_client_credentials()
        search_results = sp.search(q=query, type="artist", limit=5)
        logger.info(json.dumps(search_results, indent=2))
        artists = []

        for item in search_results.get("artists", {}).get("items", []):
            try:
                images = item.get("images", [])
                image_url = images[0].get("url", "") if images and isinstance(images[0], dict) else ""
                artists.append({
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "genres": item.get("genres", []),
                    "image": image_url
                })
            except Exception as e:
                logger.warning(f"Artiste ignoré (erreur lors du parsing) : {e}")
                continue

        logger.info(f"{len(artists)} artistes trouvés pour la session {session_id}.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": session_id,
                "artists": artists
            })
        }

    except Exception as e:
        logger.exception("Erreur fatale dans lambda_handler :")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }