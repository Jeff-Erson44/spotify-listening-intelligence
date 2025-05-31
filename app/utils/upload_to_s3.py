import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os


def upload_file_to_s3(local_file_path, bucket_name, s3_key):
    try: 
        session = boto3.Session()
        s3 = session.client("s3")
        
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uplaod réuss : {s3_key}")
        return True
    except FileNotFoundError:
        print("Fichier local introuvable.")
    except NoCredentialsError:
        print("Identifiants AWS manquants.")
    except ClientError as e:
        print(f"Erreur S3 : {e}")
    return False