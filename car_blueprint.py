"""Car blueprint for handling car-related API routes"""

from functools import reduce
from flask import Blueprint, jsonify, request
from car_dao import CarDao
from car import Car
from car_utils import format_car_description

car_blueprint = Blueprint("car_blueprint", __name__)
car_dao = CarDao("car.db")

@car_blueprint.route("/cars", methods=["GET"])
def get_all_cars():
    """Retrieve all cars with model names in uppercase."""
    cars = car_dao.get_all_cars()
    cars_uppercase = [
        {"vin_nr": car.vin_nr, "model_upper": car.model.upper()}
        for car in cars
    ]
    return jsonify(cars_uppercase), 200

@car_blueprint.route("/cars/<string:vin_nr>", methods=["GET"])
def get_car(vin_nr):
    """Retrieve a single car by its VIN number."""
    car = car_dao.get_car(vin_nr)
    if car:
        formatted_description = format_car_description(car)
        car_data = car.__dict__
        car_data['formatted_description'] = formatted_description
        return jsonify(car_data), 200
    return jsonify({"message": "Car not found"}), 404

@car_blueprint.route("/cars", methods=["POST"])
def add_car():
    """Add a new car to the database."""
    data = request.get_json()
    new_car = Car(
        vin_nr=data["vin_nr"],
        make=data["make"],
        model=data["model"],
        year=data["year"],
        description=data["description"],
        price=data["price"],
        features=data["features"],
    )
    car_dao.add_car(new_car)
    return jsonify({"message": "Car created"}), 201

@car_blueprint.route("/cars/<string:vin_nr>", methods=["PUT"])
def update_car(vin_nr):
    """Update an existing car in the database."""
    data = request.get_json()
    updated_car = Car(
        vin_nr=vin_nr,
        make=data["make"],
        model=data["model"],
        year=data["year"],
        description=data["description"],
        price=data["price"],
        features=data["features"],
    )
    if car_dao.update_car(updated_car):
        return jsonify({"message": "Car updated"}), 200
    return jsonify({"message": "Car not found or not updated"}), 404

@car_blueprint.route("/cars/<string:vin_nr>", methods=["DELETE"])
def delete_car(vin_nr):
    """Delete a car from the database by VIN number."""
    if car_dao.delete_car(vin_nr):
        return jsonify({"message": "Car deleted"}), 200
    return jsonify({"message": "Car not found or not deleted"}), 404

@car_blueprint.route("/cars/converted_prices/<float:conversion_rate>/<int:decimals>",
                     methods=["GET"])
def get_converted_prices(conversion_rate, decimals):
    """Convert car prices based on conversion rate and specified decimal places."""
    cars = car_dao.get_all_cars()
    converted_prices = [
        {
            "vin_nr": car.vin_nr,
            "price_adjusted": round(car.price * conversion_rate, decimals)
        }
        for car in cars
    ]
    return jsonify(converted_prices), 200

@car_blueprint.route("/cars/sorted/<string:sort_by>", methods=["GET"])
def get_sorted_cars(sort_by):
    """Retrieve cars sorted by the specified attribute."""
    cars = car_dao.get_all_cars()
    if sort_by == "price":
        sorted_cars = sorted(cars, key=lambda car: car.price)
    elif sort_by == "year":
        sorted_cars = sorted(cars, key=lambda car: car.year)
    else:
        return jsonify({"message": "Invalid sort criterion"}), 400
    return jsonify([car.__dict__ for car in sorted_cars]), 200

@car_blueprint.route("/cars/mapped_prices", methods=["GET"])
def get_mapped_prices():
    """Apply a 10% discount to car prices and return the adjusted list."""
    cars = car_dao.get_all_cars()
    mapped_prices = [
        {"vin_nr": car.vin_nr, "price_discounted": round(car.price * 0.9, 2)}
        for car in cars
    ]
    return jsonify(mapped_prices), 200

@car_blueprint.route("/cars/filtered_cars/<int:year>", methods=["GET"])
def get_filtered_cars(year):
    """Filter and return cars from a specific year or newer."""
    cars = car_dao.get_all_cars()
    filtered_cars = [car.__dict__ for car in cars if car.year >= year]
    return jsonify(filtered_cars), 200

@car_blueprint.route("/cars/total_price", methods=["GET"])
def get_total_price():
    """Calculate and return the total price of all cars."""
    cars = car_dao.get_all_cars()
    total_price = reduce(lambda acc, car: acc + car.price, cars, 0)
    return jsonify({"total_price": total_price}), 200

@car_blueprint.route("/cars/processed_price_summary/<int:min_year>/<float:price_increase>",
                     methods=["GET"])
def get_processed_price_summary(min_year, price_increase):
    """Calculate the total adjusted price for cars newer than min_year."""
    cars = car_dao.get_all_cars()
    filtered_cars = filter(lambda car: car.year >= min_year, cars)
    mapped_prices = map(lambda car: car.price * price_increase, filtered_cars)
    total_adjusted_price = reduce(lambda acc, price: acc + price, mapped_prices, 0)
    return jsonify({"total_adjusted_price": round(total_adjusted_price, 2)}), 200
