from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

print(tf.__version__)

arr = np.array([1, 2, 3, 4, 5])
print(arr)

#modela = load_model("modelmodify10000e15.h5")
#modela.summary()
image = cv2.imread(r'C:\InceptionNet\T1\T1.jpg')
def preprocess_image(image_path):
    image = cv2.imread(image_path) 
    image = cv2.resize(image, (160, 160))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype("float32") / 255.0
    return np.expand_dims(image, axis=0)

a = preprocess_image(image)
print(a)
#tf.io.read_file(image_path)
#cv2.imread(image_path)

# load the input image and convert it to grayscale
#image = cv2.imread(r'C:\InceptionNet\T1\T1.jpg') #เก็บภาพในตัวแปร ,OpenCV จะโหลดภาพมาในรูปแบบ BGR (สีน้ำเงิน, เขียว, แดง) #แสดงภาพต้นฉบับ 
def cap(image): 
    imageM = cv2.imread(image) 
    rgb_image = cv2.cvtColor(imageM, cv2.COLOR_BGR2RGB) #แปลงสีภาพจาก BGR เป็น RGB
    results = detector.detect_faces(rgb_image) #box  confidence keypoints
    for face in results:
        x, y, width, height = face['box'] #face['box'] = [100, 150, 60, 60]  x = 100, y = 150, width = 60, height = 60
        x2, y2 = x + width, y + height #  2 จุด 
        """ดึงตำแหน่งกรอบใบหน้าจาก dictionary ที่ key box
        (x, y) คือพิกัดมุมซ้ายบนของใบหน้า
        width คือความกว้างของกรอบใบหน้า
        height คือความสูงของกรอบใบหน้า"""
        # วาดกรอบสีเขียวรอบใบหน้า
        #cv2.rectangle(imageM, (x, y), (x2, y2), (0, 255, 0), 2) #cv2.rectangle(image, pt1, pt2, color, thickness)
        i = rgb_image[y:y2, x:x2]

        return i
