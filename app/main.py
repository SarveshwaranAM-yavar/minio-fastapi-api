from datetime import timedelta
from io import BytesIO
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from minio import Minio, S3Error
# from config.settings import (
#     MINIO_DOMAIN,
#     MINIO_PORT,
#     MINIO_USER_NAME,
#     MINIO_PASSWORD,
#     MINIO_BUCKET
# )




load_dotenv()  # Looks for a .env file in current dir

MINIO_DOMAIN = os.getenv("MINIO_DOMAIN")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_USER_NAME = os.getenv("MINIO_USER_NAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

app = FastAPI()

minio_client = Minio(f'{MINIO_DOMAIN}:{MINIO_PORT}',
                     access_key=MINIO_USER_NAME,
                     secret_key=MINIO_PASSWORD,
                     secure= False)

bucket = MINIO_BUCKET

if not minio_client.bucket_exists(bucket_name=bucket):
    minio_client.make_bucket(bucket)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        stream = BytesIO(content)  # 👈 wrap bytes in a file-like stream
        minio_client.put_object(
            bucket_name=bucket,
            object_name=file.filename,
            data=stream,
            length=len(content),
            content_type=file.content_type
        )
        return {"message": f"'{file.filename}' uploaded to bucket '{bucket}' successfully."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list")
def list_files():
    try:
        objects = minio_client.list_objects(bucket)
        file_list = [obj.object_name for obj in objects]
        return {"files": file_list}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        minio_client.remove_object(bucket, filename)
        return {"message": f"'{filename}' deleted from bucket '{bucket}'."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/get-url")
def generate_file_url(filename: str = Query(...)):
    try:
        url = minio_client.presigned_get_object(
            bucket_name=bucket,
            object_name=filename,
            expires=timedelta(seconds=3600) # URL is valid for 1 hour (3600 seconds)
        )
        return {"url": url}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/url/{file_name}')
def generate_url(file_name : str):
    try:
        url = minio_client.get_presigned_url('GET',bucket_name=bucket,object_name=file_name,expires=timedelta(seconds=3600))
        return {'url':url}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/update/{file_name}")
async def update_file(file_name: str, newfile: UploadFile = File(...)):
    try:
        minio_client.remove_object(bucket_name=bucket,object_name=file_name)
        content = await newfile.read()
        stream = BytesIO(content)
        minio_client.put_object(bucket_name=bucket,object_name=file_name,data=
                                stream, length= len(content),content_type= newfile.content_type)
        return {"message": f"'{file_name}' updated to bucket '{bucket}' successfully.",
                "file_details": file_name,
                "content_type": newfile.content_type,
                "size": len(content)}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
