import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# Inisialisasi dictionary untuk menyimpan id dan nama
id_names = {}

# Mendapatkan daftar file dalam direktori dataset
dataset_dir = 'dataset/'
files = os.listdir(dataset_dir)

# Memproses setiap file dalam direktori dataset
for file in files:
    if file.endswith('.jpg'):
        # Membagi nama file untuk mendapatkan id dan nama
        parts = file.split('.')
        id = int(parts[1])  # Mengambil id dari nama file
        name = parts[0]     # Mengambil nama dari nama file (tanpa id)

        # Menambahkan id dan nama ke dalam dictionary
        if id not in id_names:
            id_names[id] = name

# Mengurutkan id_names berdasarkan id
id_names = dict(sorted(id_names.items()))

# Membuat array names berdasarkan id_names
names = ['None'] + [id_names[i] for i in range(1, len(id_names) + 1)]
#names = ['None'] + [id_names.get(i, 'Unknown') for i in range(1, len(id_names) + 1)]


# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Check if confidence is less than 100 ==> "0" is perfect match 
        if confidence < 100:
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)  
    
    cv2.imshow('camera', img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
