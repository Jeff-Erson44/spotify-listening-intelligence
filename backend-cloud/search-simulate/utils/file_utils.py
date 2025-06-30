import boto3
import json

def upload_json_to_s3(data, bucket_name, key):
    """
    Convertit les données en JSON et upload sur S3.
    """
    if not bucket_name:
        raise ValueError("Le nom du bucket S3 est vide ou None.")
    s3 = boto3.client("s3")
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')  # conversion en bytes
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=json_data)
        print(f"Fichier uploadé sur s3://{bucket_name}/{key}")
    except Exception as e:
        print(f"Erreur lors de l'upload sur S3 : {e}")
        raise