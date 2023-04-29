import cv2
import mediapipe as mp
import time
import keyboard
import mss
import mss.tools
import pyautogui
import numpy as np
import pyautogui
from keras.models import load_model
import sqlite3
from baza import baza


bazka = baza()
classes = bazka.conn(r"C:\\SQLite\\baza.db")

class1 = classes[0][0]
class2 = classes[1][0]

camera=cv2.VideoCapture(0)
color = (255,0,255)
# OKRESLENIE MINIMALNEJ WARTOSCI OD KTOREJ BEDZIE ROZPOZNAWANA TWARZ 
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()
a = 5
b = 10

while True:
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    img = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    

    # Make the image a numpy array and reshape it to the models input shape.
    img = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    img = (img / 127.5) - 1


    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 2)
    for (x, y, w, h) in faces:
    # Predicts the model
        try:
            prediction = model.predict(img)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            #print(f"Klasa I: {class1}, Klasa2: {class2}, Predykcja: {class_name}")
            #print(f"ID KLASY1:{id(class11)}, ID KLASY2:{id(class22)}, ID PRED:{id(y_new)}")
            #print(index)
            # Z BAZY TRZEBA POBIERAC ID I PRZYROWNYWAC DO INDEKSOW ZEBY TO DZIALALO CHYBA 
            if index == class1:
                print("Access Authorized")
                
            else:
                print("User not detected")        

            #print(class_name)
            #print(confidence_score*100)
            
            # print(class2)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, class_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("Webcam Image", image)
        except:
            pass
            
    # CLOSING WINDOW

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

'''
Trenowanie modelu - należy wykorzystać bibliotekę cv2 do trenowania 
modelu rozpoznającego twarze. Do tego celu zaleca się wykorzystanie algorytmu LBPH, który dobrze sprawdza się w rozpoznawaniu twarzy.

'''