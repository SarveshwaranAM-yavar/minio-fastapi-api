from datetime import timedelta
from io import BytesIO
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from minio import Minio, S3Error

from . import minio_client
from . import schemas
from . import routes
# from config.settings import (
#     MINIO_DOMAIN,
#     MINIO_PORT,
#     MINIO_USER_NAME,
#     MINIO_PASSWORD,
#     MINIO_BUCKET
# )

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()  

MINIO_DOMAIN = os.getenv("MINIO_DOMAIN")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_USER_NAME = os.getenv("MINIO_USER_NAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not minio_client.minio_client.bucket_exists(bucket_name=minio_client.bucket):
    minio_client.minio_client.make_bucket(minio_client.bucket)
    
app.include_router(routes.router)




