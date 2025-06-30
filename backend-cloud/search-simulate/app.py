import boto3
import logging
import json
import os
from utils.auth import get_spotify_client_credentials

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query")
        session_id = body.get("x-session-id") or event.get("headers", {}).get("x-session-id")

        if not query:
            return {"statusCode": 400, "body": json.dumps({"error": "Paramètre 'query' requis."})}
        if not session_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Paramètre 'x-session-id' requis."})}

        logger.info(f"Recherche d'artistes pour la requête : {query}")

        sp = get_spotify_client_credentials()
        search_results = sp.search(q=query, type="artist", limit=5)
        artists = []

        for item in search_results.get("artists", {}).get("items", []):
            artists.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "genres": item.get("genres", []),
                "image": item.get("images", [{}])[0].get("url", "")
            })

        logger.info(f"{len(artists)} artistes trouvés pour la session : {session_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": session_id,
                "artists": artists
            })
        }

    except Exception as e:
        logger.error(f"Erreur dans search-simulate : {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }