from abc import ABC
from enum import Enum
from datetime import datetime
import time

class VehicleType(Enum):
  CAR = 1
  TRUCK = 2
  BIKE = 3

class Vehicle(ABC):
  def __init__(self, licence_plate, vehicle_type):
    self.vehicle_type = vehicle_type
  