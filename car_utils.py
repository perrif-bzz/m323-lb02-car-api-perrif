"""Car utilities for filtering, processing, and formatting car data"""

def filter_by_price_higher_than(car, price):
    """Filter function to check if car price is higher than specified value."""
    return car.price > price

def filter_by_year(car, year):
    """Filter function to check if car's manufacturing year is newer or equal to specified year."""
    return car.year >= year

def process_car_data(cars, filter_func):
    """Process cars list and return those that match the filter function criteria."""
    return [car for car in cars if filter_func(car)]

def aggregate_car_data(cars, aggregation_func):
    """Aggregate car data using specified aggregation function on car prices."""
    return aggregation_func([car.price for car in cars])

def format_car_description(car):
    """Format car's description for display."""
    return f"{car.year} {car.make} {car.model} - {car.description} ({car.price}CHF)"

def create_price_filter(price_threshold):
    """Create a filter function to filter cars with prices above a threshold."""
    def filter_by_price(car):
        return car.price > price_threshold
    return filter_by_price
