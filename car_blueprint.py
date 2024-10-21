"""Car blueprint"""

from flask import Blueprint, jsonify, request
from car_dao import CarDao
from car import Car

car_blueprint = Blueprint("car_blueprint", __name__)
car_dao = CarDao("car.db")


@car_blueprint.route("/cars", methods=["GET"])
def get_all_cars():
    cars = car_dao.get_all_cars()
    return jsonify([car.__dict__ for car in cars]), 200


@car_blueprint.route("/cars/<string:vin_nr>", methods=["GET"])
def get_car(vin_nr):
    car = car_dao.get_car(vin_nr)
    if car:
        return jsonify(car.__dict__), 200
    else:
        return jsonify({"message": "Car not found"}), 404


@car_blueprint.route("/cars", methods=["POST"])
def add_car():
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
    data = request.get_json()
    updated_car = Car(
        vin_nr=data["vin_nr"],
        make=data["make"],
        model=data["model"],
        year=data["year"],
        description=data["description"],
        price=data["price"],
        features=data["features"],
    )
    if car_dao.update_car(updated_car):
        return jsonify({"message": "Car updated"}), 200
    else:
        return jsonify({"message": "Car not found or not updated"}), 404


@car_blueprint.route("/cars/<string:vin_nr>", methods=["DELETE"])
def delete_car(vin_nr):
    if car_dao.delete_car(vin_nr):
        return jsonify({"message": "Car deleted"}), 200
    else:
        return jsonify({"message": "Car not found or not deleted"}), 404