from abc import ABC
from enum import Enum
from datetime import datetime
import time

class VehicleType(Enum):
  CAR = 1
  TRUCK = 2
  BIKE = 3

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

    def get_type(self) -> VehicleType:
        return self.type

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(licence_plate, VehicleType.CAR)

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Truck(Vehicle):
  def __init__(self, licence_plate):
    super().__init__(licence_plate, VehicleType.TRUCK)

class ParkingSpot:
    def __init__(self, spot_number: int):
        self.spot_number = spot_number
        self.vehicle_type = VehicleType.CAR  # Default vehicle type is CAR
        self.parked_vehicle = None

    def is_available(self) -> bool:
        return self.parked_vehicle is None

    def park_vehicle(self, vehicle: Vehicle) -> None:
        if self.is_available() and vehicle.get_type() == self.vehicle_type:
            self.parked_vehicle = vehicle
        else:
            raise ValueError("Invalid vehicle type or spot already occupied.")

    def unpark_vehicle(self) -> None:
        self.parked_vehicle = None

class Level:
    def __init__(self, floor: int, num_spots: int):
        self.floor = floor
        self.parking_spots: List[ParkingSpot] = [ParkingSpot(i) for i in range(num_spots)]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if spot.is_available() and spot.get_vehicle_type() == vehicle.get_type():
                spot.park_vehicle(vehicle)
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                return True
        return False

    def display_availability(self) -> None:
        print(f"Level {self.floor} Availability:")
        for spot in self.parking_spots:
            print(f"Spot {spot.get_spot_number()}: {'Available' if spot.is_available() else 'Occupied'}")




class ParkingLot:

  _instance = None

  def __init__(self):
    if ParkingLot._instance is not None:
      raise ValueError("This is a singleton class which has already been initialized")
    ParkingLot._instance = self
    self.level = []  
  
  def get_instance():
    if ParkingLot._instance is None:
      ParkingLot()
    return ParkingLot._instance

  def add_level(self, level: Level):
    self.levels.append(level)
  
  def park_vehicle(self, vehicle: Vehicle)->bool:
    for level in self.levels:
      if level.park_vehicle(vehicle):
        return True
    return False
    
  def unpark_vehicle(self, vehicle: Vehicle) -> bool:
    for level in self.levels:
      if level.unpark_vehicle(vehicle):
        print(f"total_cost: {vehicle.ticket.calculate_cost(self.hourly_rate)}")
        return True
    return False
  
  def display_availability(self):
    for level in self.levels:
      level.display_availability()
      print("---------------------------------------")
  


parking_lot = ParkingLot.get_instance()
level3 = Level(1, 10)
level3.add_spot(ParkingSpot(10, VehicleType.BIKE))
parking_lot.add_level(Level(1, 10))
parking_lot.add_level(Level(2, 20))
parking_lot.add_level(level3)

car = Car("ABC123")
truck = Car("XYZ789")
bike = Bike("1235HH")

parking_lot.park_vehicle(car)
parking_lot.park_vehicle(truck)
parking_lot.park_vehicle(bike)

parking_lot.display_availability()

time.sleep(20)

parking_lot.unpark_vehicle(car)

parking_lot.display_availability()

      
