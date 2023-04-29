import cv2
import mediapipe as mp
import time
import keyboard
import mss
import mss.tools
import pyautogui
import numpy as np
import pyautogui

cap=cv2.VideoCapture(0)
mpFace = mp.solutions.face_detection
mpDraw=mp.solutions.drawing_utils
color = (255,0,255)
# OKRESLENIE MINIMALNEJ WARTOSCI OD KTOREJ BEDZIE ROZPOZNAWANA TWARZ 
s = pyautogui.screenshot()
face=mpFace.FaceDetection(0.7)
lista = [1,2,3,4,5,6,7,8,9,10]
macierz = []
sct = mss.mss()
space = []
# MAIN LOOP
iteracja = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_height = img.shape[0]
    img_width = img.shape[1]
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=face.process(imgRGB)
    if results.detections:
        #bez enumerate nie dziala 
        for id,detection in enumerate(results.detections):

            bboxC=detection.location_data.relative_bounding_box     
            # ZMIANA WARTOSCI NA PIKSELE      
            ih,iw,ic=img.shape

            x_min = bboxC.xmin
            y_min = bboxC.ymin
            width = bboxC.width
            height = bboxC.height
            bbox=int(x_min*iw-30),int(y_min*ih-50),\
                    int(width*iw+50),int(height*ih+63)
            # RYSOWANIE KWADRATUqqqqq
            #cv2.rectangle(img,bbox,(195,195,195),1)
            try:
                obj = pyautogui.locateOnScreen("mid_glass2.PNG", confidence = 0.5)
                # monitor =  {"top": bbox[1], "left": bbox[0], "width": bbox[2], "height": bbox[3]}
                monitor =  {"top": obj.top+20, "left": obj.left, "width": obj.width, "height": obj.height}
                    # height + 20 dla far 
                    # middle normalnie dla dupa0.png
                    # far-middle normalnie dla twarz_close1.png
                # print(obj)
                # ROBIENIE ZRZUTOW EKRANU WYKORZYSTUJAC PYAUTOGUI
                if obj:
                # ROBIENIE ZRZUTOW EKRANU RECZNIE
                #if keyboard.is_pressed('left'):qqqq
                    print("Wciasnales klawisz")
                    # TUTAJ TRZEBA ZROBIC ROBIENIE ZRZUTOW EKRANU I ZAPISYWANIE DO INNEGO PLIKU I TRZEBA OPISAC ZDJECIA 
                    
                    output = f"C:\\FaceDetection\\temp\\26_03{iteracja}.png".format(**monitor)
                    sct_img = sct.grab(monitor)
                    arr_img = np.array(sct_img)
                    space.append(1)
                    mss.tools.to_png(sct_img.rgb, sct_img.size, output = output)
                    iteracja +=1

                if iteracja <=10:
                    break
            except:
                pass
        # CLOSING WINDOW
        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

'''
Trenowanie modelu - należy wykorzystać bibliotekę cv2 do trenowania 
modelu rozpoznającego twarze. Do tego celu zaleca się wykorzystanie algorytmu LBPH, który dobrze sprawdza się w rozpoznawaniu twarzy.

'''