




import os
from dotenv import load_dotenv
from minio import Minio


load_dotenv()  # Looks for a .env file in current dir

MINIO_DOMAIN = os.getenv("MINIO_DOMAIN")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_USER_NAME = os.getenv("MINIO_USER_NAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

minio_client = Minio(f'{MINIO_DOMAIN}:{MINIO_PORT}',
                     access_key=MINIO_USER_NAME,
                     secret_key=MINIO_PASSWORD,
                     secure= False)

bucket = MINIO_BUCKET