from abc import ABC
from enum import Enum
from datetime import datetime
import time


class Ticket:
  def __init__(self):
    self.entry_time = datetime.now()
  
  def calculate_cost(self, hourly_rate):
    time_diff = datetime.now() - self.entry_time
    hour_diff = time_diff.total_seconds() / 3600
    return hour_diff * hourly_rate


class VehicleType(Enum):
  CAR = 1
  TRUCK = 2
  BIKE = 3

class Vehicle(ABC):

  def __init__(self, licence_plate: str, vehicle_type: VehicleType, ticket: Ticket = None):
    self.licence_plate = licence_plate
    self.vehicle_type = vehicle_type
    self.ticket = ticket
  
  def get_type(self)-> VehicleType:
    return self.vehicle_type
  

class Car(Vehicle):
  def __init__(self, licence_plate: str):
    super().__init__(licence_plate, VehicleType.CAR)
  
class Truck(Vehicle):
  def __init__(self, licence_plate: str):
    super().__init__(licence_plate, VehicleType.TRUCK)
  
class Bike(Vehicle):
  def __init__(self, licence_plate: str):
    super().__init__(licence_plate, VehicleType.BIKE)


class ParkingSpot:
  def __init__(self, spot_number:int, vehicle_type:VehicleType = VehicleType.CAR):
    self.spot_number = spot_number
    self.vehicle_type = vehicle_type
    self.parked_vehicle = None
  
  def is_available(self):
    return not self.parked_vehicle
  
  def park_vehicle(self, vehicle: Vehicle):
    if self.is_available() and vehicle.get_type() == self.vehicle_type:
      self.parked_vehicle = vehicle
    else:
      raise ValueError("Invalid vehicle type or spot is already booked")
  
  def unpark_vehicle(self):
    if self.is_available():
      return ValueErr("Parking Spot is free")
    self.parked_vehicle = None
  
  def get_vehicle_type(self):
    return self.vehicle_type
  
  def get_parked_vehicle(self):
    return self.parked_vehicle
  
  def get_spot_number(self):
    return self.spot_number


class Level:
  def __init__(self, floor:int, num_spots: int):
    self.floor = floor
    self.parking_spots = [ParkingSpot(i) for i in range(num_spots)]
  
  def park_vehicle(self, vehicle: Vehicle)->bool:
    for spot in self.parking_spots:
      if spot.is_available() and spot.get_vehicle_type() == vehicle.get_type():
        spot.park_vehicle(vehicle)
        return True
    return False
  
  def unpark_vehicle(self, vehicle:Vehicle)->bool:
    for spot in self.parking_spots:
      if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
        spot.unpark_vehicle()
        return True
    return False
  
  def add_spot(self, spot: ParkingSpot):
    self.parking_spots.append(spot)
  
  def display_availability(self)->None:
    print(f"Level {self.floor} Availability:")
    for spot in self.parking_spots:
      print(f"Spot {spot.get_spot_number()}: {'Available' if spot.is_available() else 'Occupied'}")

class ParkingLot:
  _instance = None

  def __init__(self):
    if ParkingLot._instance is not None:
      raise Exception("This class is singleton")
    ParkingLot._instance = self
    self.levels = []
    self.hourly_rate = 20
  
  @staticmethod
  def get_instance():
    if ParkingLot._instance is None:
      ParkingLot()
    return ParkingLot._instance
  
  def add_level(self, level: Level):
    self.levels.append(level)
  
  def park_vehicle(self, vehicle: Vehicle)->bool:
    for level in self.levels:
      if level.park_vehicle(vehicle):
        vehicle.ticket = Ticket()
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

      
