"""Car dataclass"""

from dataclasses import dataclass

@dataclass
class Car:
    """Data class representing a car with attributes like vin number, make, model, etc."""
    vin_nr: str
    make: str
    model: str
    year: int
    description: str
    price: float
    features: tuple
