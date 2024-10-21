"""Car Data Access Object"""

import sqlite3
from car import Car

class CarDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS cars""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS cars (
                vin_nr TEXT PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                description TEXT,
                price REAL,
                features TEXT
            )"""
        )
        self.conn.commit()

    def add_car(self, car: Car):
        self.cursor.execute(
            "INSERT INTO cars (vin_nr, make, model, year, description, price, features) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (car.vin_nr, car.make, car.model, car.year, car.description, car.price, ",".join(car.features))
        )
        self.conn.commit()

    def get_car(self, vin_nr: str):
        self.cursor.execute("SELECT * FROM cars WHERE vin_nr = ?", (vin_nr,))
        row = self.cursor.fetchone()
        if row:
            return Car(
                vin_nr=row[0],
                make=row[1],
                model=row[2],
                year=row[3],
                description=row[4],
                price=row[5],
                features=row[6].split(',')
            )
        return None

    def get_all_cars(self):
        self.cursor.execute("SELECT * FROM cars")
        rows = self.cursor.fetchall()
        return [
            Car(
                vin_nr=row[0],
                make=row[1],
                model=row[2],
                year=row[3],
                description=row[4],
                price=row[5],
                features=row[6].split(',')
            )
            for row in rows
        ]

    def update_car(self, car: Car):
        self.cursor.execute(
            "UPDATE cars SET make = ?, model = ?, year = ?, description = ?, price = ?, features = ? WHERE isbn = ?",
            (car.make, car.model, car.year, car.description, car.price, ",".join(car.features), car.vin_nr)
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_car(self, vin_nr: str):
        self.cursor.execute("DELETE FROM cars WHERE vin_nr = ?", (vin_nr,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
