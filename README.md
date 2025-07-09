**MINIO SETUP IN LOCAL:**
curl -O https://dl.min.io/server/minio/release/darwin-arm64/minio
chmod +x ./minio
sudo mv ./minio /usr/local/bin/

mkdir -p ~/minio-data  

MINIO_ROOT_USER=minioadmin \   

MINIO_ROOT_PASSWORD=minioadmin \

minio server ~/minio-data --console-address ":9001"

This will help to run the minio server. 
minio provides two kind of access which are GUI and API 
For GUI purpose use localhost:9001 which will be useful in seeing the changes which are done in the bucket. Even we can create our own bucket using the GUI.

For API’s we can use the localhost:9000 to use in our python code part. 
To use the api in python we have to establish the connection using,
Client = Minio(‘localhost:9000’,access_key=’minioadmin’,secret_key=’minioadmin’,secure=False)
Note: secure= False -> setting up to http instead of https 

Note: make sure to keep the server on. Whenever doing operations.

**ENVIRONMENT CONFIGURATIONS:**
MINIO_DOMAIN="localhost"
MINIO_PORT=9000
MINIO_PASSWORD="minioadmin"
MINIO_USER_NAME="minioadmin"
MINIO_BUCKET="testbucket"


**INSTALLATION SETUP:**
1.	Python version (3.11) 

2.	Conda virtual environment 
create conda -n minio-env python=3.11
conda activate minio-env 

3.	Install dependencies
pip install -r requirements.txt

4.	Make sure minio server is running in the background (refer minio setup in local)

5.	Start FastAPI:

python -m uvicorn app.main:app –reload

**API ENDPOINTS:**

http method 	Endpoint 	Description
POST	/upload	Upload file to minio bucket.
GET 	/list 	List all the files available in the bucket.
GET 	/get-url?filename=sample.txt	Get the url for the file to access it in the web. 
PUT 	/update/{file_name}	Update the already existing file. 
DELETE	/delete/{filename}	Delete a specific file 

**FILE STORAGE DESIGN:**
Objects are stored in the minio by their filename as a key.
Stored in the defined bucket. 

**TESTING:**
Use swagger-UI localhost:8000/docs 
POSTMAN for uploading the file and test the working. 
Note: Use the minio GUI (localhost:9001) for further checking the file is uploaded properly. 
