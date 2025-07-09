**MINIO SETUP IN LOCAL:** <br>
curl -O https://dl.min.io/server/minio/release/darwin-arm64/minio <br>
chmod +x ./minio <br>
sudo mv ./minio /usr/local/bin/  <br>

mkdir -p ~/minio-data  

MINIO_ROOT_USER=minioadmin \   
MINIO_ROOT_PASSWORD=minioadmin \
minio server ~/minio-data --console-address ":9001"

This will help to run the minio server. 
minio provides two kind of access which are GUI and API. <br>
For GUI purpose use localhost:9001 which will be useful in seeing the changes which are done in the bucket. Even we can create our own bucket using the GUI.

For API’s we can use the localhost:9000 to use in our python code part. 
To use the api in python we have to establish the connection using,
Client = Minio(‘localhost:9000’,access_key=’minioadmin’,secret_key=’minioadmin’,secure=False)
Note: secure= False -> setting up to http instead of https 

Note: make sure to keep the server on. Whenever doing operations.

**ENVIRONMENT CONFIGURATIONS:** <br>
MINIO_DOMAIN="localhost" <br>
MINIO_PORT=9000 <br>
MINIO_PASSWORD="minioadmin" <br>
MINIO_USER_NAME="minioadmin" <br>
MINIO_BUCKET="testbucket" <br>


**INSTALLATION SETUP:** <br>
1.	Python version (3.11) 

2.	Conda virtual environment <br>
create conda -n minio-env python=3.11 <br>
conda activate minio-env 

3.	Install dependencies <br>
pip install -r requirements.txt

4.	Make sure minio server is running in the background (refer minio setup in local)

5.	Start FastAPI:

python -m uvicorn app.main:app –reload

**API ENDPOINTS:**

http method 	Endpoint 	Description <br>
POST	-> /upload ->	Upload file to minio bucket. <br>
GET ->	/list ->	List all the files available in the bucket. <br>
GET ->	/get-url?filename=sample.txt -> Get the url for the file to access it in the web. <br>
PUT -> /update/{file_name} -> Update the already existing file. <br>
DELETE	-> /delete/{filename}	-> Delete a specific file <br>

**FILE STORAGE DESIGN:**
i.Objects are stored in the minio by their filename as a key.
ii.Stored in the defined bucket. 

**TESTING:**
i.Use swagger-UI localhost:8000/docs 
ii.POSTMAN for uploading the file and test the working. 
Note: Use the minio GUI (localhost:9001) for further checking the file is uploaded properly. 
