"""Car dataclass"""

from dataclasses import dataclass


@dataclass
class Car:
    vin_nr: str
    make: str
    model: str
    year: int
    description: str
    price: float
    features: tuple
