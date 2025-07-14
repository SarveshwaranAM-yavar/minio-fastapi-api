<img width="468" height="337" alt="image" src="https://github.com/user-attachments/assets/71ec67ed-ca8a-4fda-8ba9-5b94c8158302" />**ARCHITECTURE DIAGRAM**




![MinIO + FastAPI Architecture](minio_architecture.jpg)

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

5.	Frontend Setup (React)
Create app
cd minio
npx create-react-app frontend
cd frontend
npm install axios

6.	Start FastAPI:

python -m uvicorn app.main:app --reload

7.	Run frontend: 

cd minio/frontend <br>
npm start



**API ENDPOINTS:**

http -> method	Endpoint ->	Description <br>
POST	-> /upload ->	Upload file to minio bucket. <br>
GET ->	/list ->	List all the files available in the bucket. <br>
GET ->	/get-url?filename=sample.txt -> Get the url for the file to access it in the web. <br>
PUT -> /update/{file_name} -> Update the already existing file. <br>
DELETE	-> /delete/{filename}	-> Delete a specific file <br>

**FILE STORAGE DESIGN:**<br>
i.Objects are stored in the minio by their filename as a key.<br>
ii.Stored in the defined bucket. 

**TESTING:** <br>
i.Use swagger-UI localhost:8000/docs <br>
ii.POSTMAN for uploading the file and test the working. <br>
Note: Use the minio GUI (localhost:9001) for further checking the file is uploaded properly. 


**Manual CLI for docker minIO**
Manual CLI for docker minIO : <br>
docker run -d \ <br>
  --name minio-server \ <br>
  -p 9000:9000 \ <br>
  -p 9001:9001 \ <br>
  -e "MINIO_ROOT_USER=minioadmin" \ <br>
  -e "MINIO_ROOT_PASSWORD=minioadmin123" \ <br>
  quay.io/minio/minio:RELEASE.2023-12-02T10-29-32Z \ <br>
  server /data --console-address ":9001" <br>
Note: this will create and run the minio-server in the docker and exposing it to our local via port localhost:9001 for the GUI and localhost:9000 for the api instances. This will create a storage volume inside the docker for storing the files which we are intended to upload. <br>


We can use the docker-compose.yml which is efficient instead of manually creating the docker container using the CLI. <br>
inorder to create a container: <br>
docker compose up -d <br>
Note: this will create a docker compose and start to run the server. You verify using the localhost:9001 with the username and password. <br>
docker ps : will list the containers in run. <br>

Whenever you finished your operation. You can either down(removing the container) or stop the container. <br>
docker compose stop – will stop the containers from working but still resist the information and all the containers details within. So you can start it again whenever needed it out. <br>
In order to start the container again use, docker compose start <br>

docker compose down – will entirely remove the containers. <br>
Note: still the data will be persist on the local which will not be deleted in this scenario. <br>


