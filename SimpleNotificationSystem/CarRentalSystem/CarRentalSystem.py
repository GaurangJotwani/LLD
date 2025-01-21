from abc import ABC, abstractmethod
from enum import Enum
from datetime import date, timedelta, time

class VehicleType(Enum):
  CAR = 1
  BIKE = 2

class Vehicle(ABC):
  def __init__(self, make, model, year, licence_plate, rental_price_per_day):
    self.make = make
    self.model = model
    self.year = year
    self.licence_plate = licence_plate
    self.rental_price_per_day = rental_price_per_day
    self.is_available = True

class Car(Vehicle):
  def __init__(self, make:str, model:str, year:int, licence_plate:str, rental_price_per_day:float, vehicle_type: VehicleType):
    super().__init__(make, model, year, licence_plate, rental_price_per_day)
    self.vehicle_type = VehicleType.CAR

class Customer:
  def __init__(self, name, email, phone, driving_license_number):
    self.name = name
    self.email = email
    self.phone = phone
    self.driving_license_number = driving_license_number

class PaymentProcessor(ABC):
  @abstractmethod
  def process_payment(self, amount):
    pass

class CreditCardPaymentProcessor(PaymentProcessor):
  def process_payment(self, amount):
    #Process the payment
    return True

class PaypalPaymentProcessor(PaymentProcessor):
  def process_payment(self, amount):
    #Process the payment
    return True

class ReservationStatus(Enum):
  BOOKED_UNPAID = 1
  CANCELLED = 2
  COMPLETED = 3
  IN_PROGRESS = 4
  BOOKED_PAID = 5

class Reservation:
  def __init__(self, reservation_id, customer, car, start_date, end_date, start_time = None, end_time = None):
    self.reservation_id = reservation_id
    self.customer = customer
    self.car = car
    self.start_date = start_date
    self.end_date = end_date
    self.start_time = start_time if start_time else time(hour=12, minute=0) 
    self.end_time = end_time if end_time else time(hour=12, minute=0)
    self.total_price = self.calculate_cost()
    self.status = ReservationStatus.BOOKED_UNPAID
  
  def calculate_cost(self):
    days_rented = (self.end_date - self.start_date).days + 1
    return self.car.rental_price_per_day * days_rented


class RentalSystem:
  _instance = None

  def __init__(self):
    if RentalSystem._instance is not None:
      raise ExceptioN("This class is singleton")
    else:
      RentalSystem._instance = self
      self.vehicles = {}
      self.reservations = {}
      self.reservation_counter = 0
  
  @staticmethod
  def get_instance():
    if RentalSystem._instance is None:
      RentalSystem()
    return RentalSystem._instance
  
  def add_vehicle(self, vehicle):
    self.vehicles[vehicle.licence_plate] = vehicle
  
  def remove_vehicle(self, vehicle):
    self.vehicles.pop(vehicle.licence_plate)
  
  def search_cars(self, make, model, start_date, end_date):
    available_cars = []
    for car in self.vehicles.values():
      if ((make is None or car.make.lower() == make.lower()) and 
          (model is None or car.model.lower() == model.lower()) and
          car.is_available):
          if self.is_car_available(car, start_date, end_date):
            available_cars.append(car)
    return available_cars
  
  def is_car_available(self, car, start_date, end_date):
    for reservation in self.reservations.values():
      if reservation.car == car:
        if not (start_date > reservation.end_date or end_date < reservation.start_date):
          return False
    return True
  
  def make_reservation(self, customer, car, start_date, end_date):
    if not car.is_available:
      return None
    
    if self.is_car_available(car, start_date, end_date):
      reservation_id = self.reservation_counter
      reservation = Reservation(reservation_id, customer, car, start_date, end_date)
      self.reservations[reservation_id] = reservation
      self.reservation_counter += 1
      return reservation
    return None
  
  def cancel_reservation(self, reservation_id):
    reservation = self.reservations.pop(reservation_id, None)
    if reservation is not None:
      reservation.status = ReservationStatus.CANCELLED
  
  def pickup_reservation(self, reservation_id):
    if reservation_id in self.reservations:
      reservation.status = ReservationStatus.IN_PROGRESS
  
  def process_payment(self, reservation, payment_processor: PaymentProcessor):
    return payment_processor.process_payment(reservation.total_price)


rental_system = RentalSystem.get_instance()

rental_system.add_vehicle(Car("Toyota", "Camry", 2022, "ABC123", 50, VehicleType.CAR))
rental_system.add_vehicle(Car("Honda", "Civic", 2022, "ABC867", 45, VehicleType.CAR))
rental_system.add_vehicle(Car("FORD", "Mustang", 2022, "947321", 70, VehicleType.CAR))

customer1 = Customer("John Doe", "john@example.com", "234234325", "DL1234")
customer2 = Customer("Jane Smith", "jane@example.com", "23423453" ,"DL5678")

start_date = date.today()
end_date = start_date + timedelta(days=3)
available_cars = rental_system.search_cars("Honda", "Civic", start_date, end_date)

if available_cars:
  selected_car = available_cars[0]
  reservation = rental_system.make_reservation(customer1, selected_car, start_date, end_date)
  if reservation is not None:
    payment_processor = PaypalPaymentProcessor()
    payment_success = rental_system.process_payment(reservation, payment_processor)
    if payment_success:
      print(f"Reservation Success! ID: {reservation.reservation_id}")
    else:
      rental_system.cancel_reservation(reservation.reservation_id)
  else:
    print("Selected car is not available for the given dates")
else:
  print("No available cars for the given dates")
