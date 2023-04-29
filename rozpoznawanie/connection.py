#!C:/Users/patry/AppData/Local/Programs/Python/Python310/python.exe
import mysql.connector

db = mysql.connector.connect(host = "localhost", port ="3306", user = "root", database = "wdp")
cursor = db.cursor()
# BEZ TEJ LINIJKI NIE DZIALA XD 
print("Content-type: text/html\n\n")

cursor.execute(
    'SELECT * FROM pracownicy'
)
wynik = cursor.fetchall()
print(f"<br>Ilosc wierszy w tabeli dostep {cursor.rowcount}</br>")

for row in wynik:
    print(f"<br>ID: {row[0]}, Imie: {row[1]}, Nazwisko: {row[2]}, Email: {row[3]}</br>")

cursor.close()
db.close()