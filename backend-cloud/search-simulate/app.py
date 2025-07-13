import logging
import json
from utils.auth import get_spotify_client_credentials

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query")
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

        logger.info(f"{len(artists)} artistes trouvés.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "artists": artists
            })
        }

    except Exception as e:
        logger.exception("Erreur fatale dans lambda_handler :")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }