from pydantic import BaseModel


class UploadFiles(BaseModel):
    filename: str
    bucketname: str
    size: int
    meta_data : str 
    presigned_url : str
    message : str
    
    

    