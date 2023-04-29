from flask import Flask, request, session, redirect, url_for, Response
import mysql.connector
from flask import render_template
import cv2
import time
# Stworzenie instancji obiektu flask
app = Flask(__name__)
#app.config['SECRET_KEY'] = '1qazXSW@3edcVFR$'
app.secret_key = 'jakis tam klucz'

camera = cv2.VideoCapture(0)

def gen_frames():
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    prev_frame_time = 0
    new_frame_time = 0
    while True:
        success, frame = camera.read()
        
        if not success:
            break
        else:
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(frame, fps, org, font, fontScale, color, thickness, cv2.LINE_AA)
            ret, buffer = cv2.imencode('.jpg', frame)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "CHUJDUHSGSGSGSGSGSGSGSGSGSGSGSGSGSG", (100, 100), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# RESZTA
db = mysql.connector.connect(host = "localhost", port ="3306", user = "root", database = "wdp")
cursor = db.cursor()

# znak / oznacza podstawowy adres witryny
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/home")
def home():
    return render_template("home.html", username = session['username'])


@app.route("/manager")
def manager():
    cursor.execute("SELECT imie, nazwisko, login, pensja FROM pracownicy WHERE stanowisko LIKE 'kierownik'")
    result = cursor.fetchall()
    return render_template("registration.html", data = result, name = "Manager")

@app.route("/sprzedawca")
def sprzedawca():
    cursor.execute("SELECT imie, nazwisko, login, pensja FROM pracownicy WHERE stanowisko LIKE 'sprzedawca'")
    result = cursor.fetchall()
    return render_template("registration.html", data = result, name = "sprzedawca")

# methods = ['GET','POST'] zeby uzytkownicy mogli wyslac login do autoryzacji
@app.route("/login", methods = ['GET','POST'])
def login():
    # msg- error message
    if request.method == 'POST':
        # Pobranie wartosci zmiennych z formularza, z pliku index.html
        username = request.form["username"]
        password = request.form["password"]
        #???
        msg =''
        # TO MUSI BYC TAK ZAPISANE, INACZEJ SIE WYKRZACZA
        cursor.execute(f'SELECT * FROM dostep WHERE name =%s AND haslo =%s',(username,password))
        # FETCHONE ZWRACA JEDEN WIERSZ Z TABELI, KTORY SPELNIA OKRESLONE WYMAGANIA
        result = cursor.fetchone()
        # JAK SIE POLECENIE MOZE WYKONAC TO ZNACZY ZE W BAZIE DANYCH SA TAKIE DANE, INACZEJ POLECENIE SQL SIE NIE WYKONUJE, CZYLI W BAZIE DANYCH NIE MA TAKICH WARTOSCI
        if result:
            session['loggedin'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            msg='Incorrect username/passowrd'
    return render_template("index.html", msg = msg)

if __name__ == "__main__":
    app.run(debug = True)