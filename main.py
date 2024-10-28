"""Main file"""

from flask import Flask
from car import Car
from car_blueprint import car_blueprint
from car_dao import CarDao

app = Flask(__name__)
app.secret_key = "my_secret_key"

app.register_blueprint(car_blueprint)


def generate_testdata():
    car_dao = CarDao('car.db')

    car_dao.create_table()

    car_dao.add_car(
        Car(
            vin_nr="11111",
            make="Nissan",
            model="Silvia S14",
            year=1998,
            description="2.0l turbocharged inline 4 producing 220 hp.",
            price=25000,
            features=("ABS", "Turbocharged", "5 speed manual", "Electronic seatbelts"),
        )
    )
    car_dao.add_car(
        Car(
            vin_nr="22222",
            make="Toyota",
            model="Supra Mk4",
            year=1994,
            description="3.0l twin-turbocharged inline 6 producing 328 hp.",
            price=35000,
            features=("ABS", "Twin-Turbocharged", "6 speed manual"),
        )
    )
    car_dao.add_car(
        Car(
            vin_nr="33333",
            make="Mazda",
            model="Eunos Roadster NA8",
            year=1992,
            description="1.8l naturally aspirated inline 4 producing 116 hp",
            price=15000,
            features=("5 speed manual", "Hardtop / Soft top"),
        )
    )

    car_dao.close()


if __name__ == "__main__":
    generate_testdata()
    app.run(debug=True)
