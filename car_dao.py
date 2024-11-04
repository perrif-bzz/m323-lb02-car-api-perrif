"""Car data access object"""

import sqlite3
from car import Car

class CarDao:
    """Data Access Object for interacting with the car database."""

    def __init__(self, db_file):
        """Initialize the CarDao with a database connection."""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create the car table in the database."""
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
        """Add a car record to the database."""
        self.cursor.execute(
            "INSERT INTO cars (vin_nr, make, model, year, description, price, features)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (car.vin_nr, car.make, car.model, car.year, car.description, car.price,
             ",".join(car.features))
        )
        self.conn.commit()

    def get_car(self, vin_nr: str):
        """Retrieve a car by its VIN number."""
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
        """Retrieve all cars from the database."""
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
        """Update a car record in the database."""
        self.cursor.execute(
            "UPDATE cars SET"
            " make = ?, model = ?, year = ?, description = ?, price = ?, features = ?"
            "WHERE vin_nr = ?",
            (car.make, car.model, car.year, car.description, car.price,
             ",".join(car.features), car.vin_nr)
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_car(self, vin_nr: str):
        """Delete a car record from the database by VIN number."""
        self.cursor.execute("DELETE FROM cars WHERE vin_nr = ?", (vin_nr,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        """Close the database connection."""
        self.conn.close()
