
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
from mtcnn.mtcnn import MTCNN
from pinecone import Pinecone
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pinecone
import os
from dotenv import load_dotenv
from mangum import Mangum


model_path = "model/modelR44.h5"
try:
    model = load_model(model_path)
    print("1666 model compled")
except Exception as e:
    print(f"Error loading model: {e}")
    facenet_model = None

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV") 
INDEX_NAME = os.getenv("INDEX_NAME")
#print("PINECONE_API_KEY:", PINECONE_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
'''embedding = np.random.rand(128).tolist()
user_id = "user1"
index.upsert(vectors=[(user_id, embedding)])'''


detector = MTCNN()
# PIL
def getembeddingpil(image_data):
    try:
        img = Image.open(io.BytesIO(image_data))
        img_array = np.asarray(img)

        faces = detector.detect_faces(img_array)

        if not faces:
            print("No face detected.")
            return None

        # Get the first detected face
        x, y, width, height = faces[0]['box']
        face_img = img.crop((x, y, x + width, y + height))

        # Resize the cropped face to 160x160 with PIL
        face_img = face_img.resize((160, 160))
        face_array = np.asarray(face_img)
        face_array = np.expand_dims(face_array, axis=0)
        
        face_array = (face_array / 255.0).astype(np.float32)
        
        embedding = model.predict(face_array, verbose=0)
        
        return embedding[0].tolist()
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

#TensorFlow
def getembeddingtf(image_data):
    try:
        img = Image.open(io.BytesIO(image_data)).convert("RGB")
        # ได้รับ byte มา 1 io.BytesIO สร้างไฟล์เสมือนโดยใช้ข้อมูลที่ได้รับมา เอาข้อมูลดิบมาสร้างทำให้อ่านได้

        img_array = np.asarray(img) #ตรวจว่าเป็น array ไหม ถ้าไม่ แปลงเป็นarray

        # Detect faces in the image
        faces = detector.detect_faces(img_array) #ตรวจหน้า สร้าง DIC

        if not faces:
            print("No face detected.")
            return None

        #detected face
        x, y, width, height = faces[0]['box'] # เลือกหน้า 0
        face_img = img.crop((x, y, x + width, y + height))

        # Convert to Tensor
        face_tensor = tf.convert_to_tensor(np.array(face_img))

        # 160x160 with TensorFlow
        face_tensor = tf.image.resize(face_tensor, (224, 224))
        
        face_tensor = tf.expand_dims(face_tensor, axis=0)
 
        face_tensor = face_tensor / 255.0
        
        face_tensor = tf.cast(face_tensor, tf.float32)

        face_tensor = tf.clip_by_value(face_tensor, 0.0, 1.0)
        # Get the embedding
        #embedding = model.predict(face_tensor) #(1, 128) ซึ่งหมายถึง "1 แถว, 128 คอลัมน์" # verbose=0
        
        return face_tensor #embedding[0].tolist() # ข้อมูล 1,128 คือ 2 มิติ เราจะทำให้เหลือแค่ 1 มิติ คือ 128 เลือก [] ออกมาจาก [[]] 
        # embedding[0] = รูปแบบ NumPy array
        # .tolist() จะแปลง NumPy array นั้นให้กลายเป็น Python list 

    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

@tf.function
def predict_embedding(face_tensor):
    em = model(face_tensor)
    em = em[0] #ตัดมิติ
    return em

print("veg1")
from fastapi import FastAPI, UploadFile, File
app = FastAPI()
handler = Mangum(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"], #http://127.0.0.1:5500
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "Worldsss"}

@app.post("/register")
async def register(name: str, file: UploadFile = File(...)):
    image_data = await file.read() #await ทำงานตลอด .read อ่านข้อมูลดิบยังใช้ไม่ได้ที่รับมาและเก็บไว้ในตัวแปร
    embedding = getembeddingtf(image_data)
    return {"message": f"User {name} registered with embedding of size {len(embedding)}"}

@app.post("/upload")
async def upload(name: str = Form(...), image: UploadFile = File(...)):
    image_data = await image.read()
    print(name)
    print(image.filename)
    a = getembeddingtf(image_data)
    print(a)
    print(a.shape)
    em = predict_embedding(a)
    em = em.numpy().tolist()
    user_id = name
    #index.upsert(vectors=[(user_id, em)])
    #print(em)
    #print(type(em))
    return {"name":user_id}

@app.post("/vertify")
async def upload( image: UploadFile = File(...)):
    image_data = await image.read()
    print(image.filename)
    a = getembeddingtf(image_data)
    print(a)
    print(a.shape)
    em = predict_embedding(a)
    em = em.numpy().tolist()
    #embedding = np.random.rand(128).tolist()
    print(image.filename)
    query_response = index.query(
    vector=em,
    top_k=3,       
    include_values=True,  
    include_metadata=True 
    )
    
    if query_response['matches']:
        match = query_response['matches'][0]
        result = {
            "id": match['id'],         # user_id
            "score": match['score'],   # ความใกล้เคียง
            "metadata": match.get('metadata', {})  # metadata ถ้ามี
        }
    else:
        result = {"id": None, "score": 9999, "metadata": {}}
    
    return result