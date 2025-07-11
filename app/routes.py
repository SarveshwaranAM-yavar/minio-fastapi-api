from datetime import timedelta
from io import BytesIO
from fastapi import APIRouter, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from minio import S3Error

from . import minio_client
import time
from . import schemas


router = APIRouter(tags=['Services'])
@router.post("/upload", response_model=schemas.UploadFiles)
async def upload_file(file: UploadFile = File(...)):
    MAX_SIZE_MB = 20
    ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png", "video/mp4", "audio/mpeg","text/plain","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/vnd.ms-excel"]

    try:
        content = await file.read()
        size = len(content)
        size_mb = size / (1024 * 1024)

        if size_mb > MAX_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"File too large. Limit is {MAX_SIZE_MB} MB.")

        mime_type = file.content_type
        if mime_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {mime_type}")

        stream = BytesIO(content)
        minio_client.minio_client.put_object(
            bucket_name=minio_client.bucket,
            object_name=file.filename,
            data=stream,
            length=size,
            content_type=mime_type
        )

        url = minio_client.minio_client.presigned_get_object(
            bucket_name=minio_client.bucket,
            object_name=file.filename,
            expires=timedelta(hours=1)
        )
        print(f"""filename={file.filename},
            bucketname={minio_client.bucket},
            size={size},
            meta_data={mime_type},
            presigned_url={url},
            message=f"'{file.filename}' uploaded successfully." """)
        return schemas.UploadFiles(
            filename=file.filename,
            bucketname=minio_client.bucket,
            size=size,
            meta_data=mime_type,
            presigned_url=url,
            message=f"'{file.filename}' uploaded successfully."
        )

    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
def list_files():
    try:
        objects = minio_client.minio_client.list_objects(minio_client.bucket)
        file_list = [obj.object_name for obj in objects]
        return {"files": file_list}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        minio_client.minio_client.remove_object(minio_client.bucket, filename)
        return {"message": f"'{filename}' deleted from bucket '{minio_client.bucket}'."}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/get-url")
def generate_file_url(filename: str = Query(...)):
    try:
        url = minio_client.minio_client.presigned_get_object(
            bucket_name=minio_client.bucket,
            object_name=filename,
            expires=timedelta(seconds=3600) # URL is valid for 1 hour (3600 seconds)
        )
        print(f"url: {url}")
        return {"url": url}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.get('/url/{file_name}')
# def generate_url(file_name : str):
#     try:
#         url = minio_client.minio_client.get_presigned_url('GET',bucket_name=minio_client.bucket,object_name=file_name,expires=timedelta(seconds=3600))
#         return {'url':url}
#     except S3Error as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{file_name}")
async def update_file(file_name: str, newfile: UploadFile = File(...)):
    try:
        minio_client.minio_client.remove_object(bucket_name=minio_client.bucket,object_name=file_name)
        content = await newfile.read()
        stream = BytesIO(content)
        minio_client.put_object(bucket_name=minio_client.bucket,object_name=file_name,data=
                                stream, length= len(content),content_type= newfile.content_type)
        return {"message": f"'{file_name}' updated to bucket '{minio_client.bucket}' successfully.",
                "file_details": file_name,
                "content_type": newfile.content_type,
                "size": len(content)}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/files")
def get_file_info(filename: str = Query(...)):
    try:
        stat = minio_client.minio_client.stat_object(bucket_name=minio_client.bucket, object_name=filename)
        return {
            "filename": filename,
            "size": stat.size,
            "content_type": stat.content_type,
            "last_modified": stat.last_modified.isoformat(),
            "etag": stat.etag,
            "metadata": stat.metadata,
            
        }
    except S3Error as e:
        return JSONResponse(status_code=404, content={"error": str(e)})

# @router.get("/files")
# def get_file_info(filename: str = Query(...)):
#     try:
#         # Get metadata info about the object
#         obj_stat = minio_client.minio_client.stat_object(bucket_name=minio_client.bucket, object_name=filename)
        
#         return {
#             "filename": filename,
#             "size_bytes": obj_stat.size,
#             "content_type": obj_stat.content_type,
#             "last_modified": obj_stat.last_modified.isoformat(),
#             "etag": obj_stat.etag,
#             "metadata": obj_stat.metadata,
#         }

#     except S3Error as e:
#         raise HTTPException(status_code=404, detail=f"File '{filename}' not found or error: {str(e)}")