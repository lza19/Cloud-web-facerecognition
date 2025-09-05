
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
from mtcnn.mtcnn import MTCNN
from pinecone.grpc import PineconeGRPC as Pinecone

model_path = "model/modelmodify10000e15.h5"

try:
    facenet_model = load_model(model_path)
    print("1666 model compled")
except Exception as e:
    print(f"Error loading model: {e}")
    facenet_model = None

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
        
        embedding = facenet_model.predict(face_array, verbose=0)
        
        return embedding[0].tolist()
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

#TensorFlow
def getembeddingtf(image_data):
    try:
        img = Image.open(io.BytesIO(image_data)) 
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

        # Convert to TensorFlow Tensor
        face_tensor = tf.convert_to_tensor(np.array(face_img))

        # Resize the cropped face to 160x160 with TensorFlow
        face_tensor = tf.image.resize(face_tensor, (160, 160))
        
        # Add a dimension for batch size
        face_tensor = tf.expand_dims(face_tensor, axis=0)

        # Normalize the pixel values
        face_tensor = face_tensor / 255.0
         
        face_tensor = face_tensor.astype(np.float32)

        face_tensor = tf.clip_by_value(face_tensor, 0.0, 1.0)
        # Get the embedding
        embedding = facenet_model.predict(face_tensor) #(1, 128) ซึ่งหมายถึง "1 แถว, 128 คอลัมน์" # verbose=0
        
        return embedding[0].tolist() # ข้อมูล 1,128 คือ 2 มิติ เราจะทำให้เหลือแค่ 1 มิติ คือ 128 เลือก [] ออกมาจาก [[]] 
        # embedding[0] = รูปแบบ NumPy array
        # .tolist() จะแปลง NumPy array นั้นให้กลายเป็น Python list 

    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None
    
print("veg1")
from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Worldsss"}

@app.post("/register")
async def register(name: str, file: UploadFile = File(...)):
    image_data = await file.read() #await ทำงานตลอด .read อ่านข้อมูลดิบยังใช้ไม่ได้ที่รับมาและเก็บไว้ในตัวแปร
    embedding = getembeddingtf(image_data)
    return {"message": f"User {name} registered with embedding of size {len(embedding)}"}