from enum import Enum
import random
import math

# Enum for package sizes
class PackageSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Locker class representing individual lockers
class Locker:
    def __init__(self, locker_id: int, size: PackageSize):
        self.locker_id = locker_id
        self.size = size
        self.is_assigned = False
        self.pin = None
        self.observers = set()

    def assign(self, pin: int):
        self.is_assigned = True
        self.pin = pin
        self.notify_observers()

    def free(self):
        self.is_assigned = False
        self.pin = None

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.locker_id, self.pin)

    def check_pin(self, pin: int) -> bool:
        return self.is_assigned and self.pin == pin

# Customer class representing a customer
class Customer:
    def __init__(self, customer_id: int, latitude: float, longitude: float):
        self.customer_id = customer_id
        self.latitude = latitude
        self.longitude = longitude
        self.assigned_locker = None
        self.pin = None

    # Observer method to receive notification when locker is assigned
    def update(self, locker_id: int, pin: int):
        self.assigned_locker = locker_id
        self.pin = pin
        print(f"Customer {self.customer_id}: Assigned locker ID - {locker_id}, PIN - {pin}")

    # Method to order a package and assign locker
    def order_package(self, package: PackageSize, amazon_locker_system):
        amazon_locker_system.assign_locker(self, package)

    def unassign_locker(self, pin: int) -> bool:
        if self.assigned_locker and self.assigned_locker.check_pin(pin):
            self.assigned_locker.free()
            self.assigned_locker = None
            self.pin = None
            print(f"Customer {self.customer_id}: Locker unassigned successfully")
            return True
        else:
            print(f"Customer {self.customer_id}: Invalid PIN or no assigned locker")
            return False

# Strategy Interface for distance calculation
class DistanceCalculationStrategy:
    def calculate_distance(self, loc1_latitude: float, loc1_longitude: float, loc2_latitude: float, loc2_longitude: float) -> float:
        pass

# Concrete Strategy for Euclidean distance calculation
class EuclideanDistanceStrategy(DistanceCalculationStrategy):
    def calculate_distance(self, loc1_latitude: float, loc1_longitude: float, loc2_latitude: float, loc2_longitude: float) -> float:
        return math.sqrt((loc1_latitude - loc2_latitude) ** 2 + (loc1_longitude - loc2_longitude) ** 2)

# Amazon Locker Management System class using Singleton pattern
class AmazonLockerSystem:
    _instance = None

    def __new__(cls, strategy: DistanceCalculationStrategy):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.locations = []
            cls._instance.strategy = strategy
        return cls._instance

    def add_location(self, location):
        self.locations.append(location)

    # Method to find the closest location to the customer
    def find_closest_location(self, customer_latitude: float, customer_longitude: float):
        closest_location = None
        min_distance = float('inf')

        for location in self.locations:
            distance = self.strategy.calculate_distance(location.latitude, location.longitude, customer_latitude, customer_longitude)
            if distance < min_distance:
                min_distance = distance
                closest_location = location

        return closest_location

    # Method to assign a locker to the customer for a given package
    def assign_locker(self, customer, package_size: PackageSize) -> bool:
        closest_location = self.find_closest_location(customer.latitude, customer.longitude)
        if closest_location:
            for locker in closest_location.lockers:
                if not locker.is_assigned and locker.size == package_size:
                    pin = random.randint(100000, 999999)
                    locker.assign(pin)
                    customer.assigned_locker = locker
                    customer.pin = pin
                    locker.add_observer(customer)
                    return True
        return False

# Location class representing a location with multiple lockers
class Location:
    def __init__(self, latitude: float, longitude: float, lockers: list):
        self.latitude = latitude
        self.longitude = longitude
        self.lockers = lockers

# Example usage
if __name__ == "__main__":
    # Create locker instances
    locker1 = Locker(1, PackageSize.SMALL)
    locker2 = Locker(2, PackageSize.MEDIUM)
    locker3 = Locker(3, PackageSize.LARGE)

    # Create location with lockers
    location1 = Location(37.7749, -122.4194, [locker1, locker2, locker3])

    # Create customer
    customer1 = Customer(1, 37.7749, -122.4194)

    # Create Amazon Locker System with Euclidean distance strategy
    euclidean_strategy = EuclideanDistanceStrategy()
    amazon_locker_system = AmazonLockerSystem(euclidean_strategy)
    amazon_locker_system.add_location(location1)

    # Order package and assign locker
    customer1.order_package(PackageSize.SMALL, amazon_locker_system)

    # Unassign locker with invalid PIN
    customer1.unassign_locker(123456)

    # Unassign locker with valid PIN
    customer1.unassign_locker(customer1.pin)