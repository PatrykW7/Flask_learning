import sqlite3
class baza:
    def __init__(self) -> None:
        pass

    def conn(self, path):
        self.path = path
        try:
            db = sqlite3.connect(self.path)
            cursor = db.cursor()

            cursor.execute('''
                SELECT id FROM dostep;

            ''')

            wynik = cursor.fetchall()
            return wynik
        except Exception as e:
            print("COS SIE WYJEBALO")

# path = C:\\SQLite\\baza.db

bazka = baza()
print(bazka.conn(r"C:\\SQLite\\baza.db"))