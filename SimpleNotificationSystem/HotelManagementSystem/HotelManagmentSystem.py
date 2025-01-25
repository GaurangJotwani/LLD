from enum import Enum
from abc import ABC, abstractmethod
from threading import Lock
from datetime import date, timedelta

class RoomType(Enum):
  SINGLE = 1
  DOUBLE = 2
  DELUXE = 3
  SUITE = 4

class RoomStatus(Enum):
  AVAILABLE = "AVAILABLE"
  BOOKED = "BOOKED"
  OCCUPIED = "OCCUPIED"

class Room:
  def __init__(self, room_type, price):
    self.id = id(self)
    self.type = room_type
    self.price = price
    self.status = RoomStatus.AVAILABLE
    self.lock = Lock()
  
  def book(self, dates = None):
    with self.lock:
      if self.status == RoomStatus.AVAILABLE:
        self.status = RoomStatus.BOOKED
      else:
        raise ValueError("Its already booked")

  def cancel(self):
    with self.lock:
      if self.status == RoomStatus.BOOKED:
        self.status = RoomStatus.AVAILABLE
      else:
        raise ValueError("Its not booked")
  
  def check_in(self):
    with self.lock:
      if self.status == RoomStatus.BOOKED:
        self.status = RoomStatus.OCCUPIED
      else:
        raise ValueError("Room is not booked")
  
  def check_out(self):
    with self.lock:
      if self.status == RoomStatus.OCCUPIED:
        self.status = RoomStatus.AVAILABLE
      else:
        raise ValueError("Room is not occupied")

class Guest:
  def __init__(self, name, email, phone):
    self.id = id(self)
    self.name = name
    self.email = email
    self.phone = phone

class ReservationStatus(Enum):
  CONFIRMED = "CONFIRMED"
  CANCELLED = "CANCELLED"

class Reservation:
  def __init__(self, reservation_id, guest, room, check_in_date, check_out_date):
    self.id = reservation_id
    self.guest = guest
    self.room = room
    self.check_in_date = check_in_date
    self.check_out_date = check_out_date
    self.status = ReservationStatus.CONFIRMED
    self.lock = Lock()
  
  def cancel(self):
    with self.lock:
      if self.status == ReservationStatus.CONFIRMED:
        self.status = ReservationStatus.CANCELLED
        self.room.cancel()
      else:
        raise ValueError("Reservation is not confirmed")

class Payment(ABC):
  @abstractmethod
  def process_payment(self, amount):
    pass

class CashPayment(Payment):
  def process_payment(self, amount):
    print("Processing payment")
    return True

class CreditCardPayment(Payment):
  def process_payment(self, amount):
    print("Processing payment")
    return True

class HotelManagementSystem:
  _instance = None
  def __init__(self):
    if not HotelManagementSystem._instance:
      self.guests = {}
      self.rooms = {}
      self.reservations = {}
      self.lock = Lock()
      HotelManagementSystem._instance = self
      self.cntr = 0
    else:
      raise Exception("Singleton class. Use get_instance method")
  
  @staticmethod
  def get_instance(self):
    return HotelManagementSystem._instance
  
  def add_guest(self,guest):
    self.guests[guest.id] = guest
  
  def get_guest(self, guest_id):
    return self.guests.get(guest_id)
  
  def add_room(self, room):
    self.rooms[room.id] = room
  
  def get_room(self, room_id):
    return self.rooms.get(room_id)
  
  def book_room(self, guest, room, check_in_date, check_out_date):
    with self.lock:
      if room.status == RoomStatus.AVAILABLE:
        room.book()
        reservation_id = self.cntr
        self.cntr += 1
        reservation = Reservation(reservation_id, guest, room, check_in_date, check_out_date)
        self.reservations[reservation_id] = reservation
        return reservation
      
      return None
  
  def cancel_reservation(self, reservation_id):
    with self.lock:
      reservation = self.reservations.get(reservation_id)
      if reservation:
        reservation.cancel()
        del self.reservations[reservation_id]
  
  def check_in(self, reservation_id):
    with self.lock:
      reservation = self.reservations.get(reservation_id)
      if reservation and reservation.status == ReservationStatus.CONFIRMED:
        reservation.room.check_in()
      else:
        raise ValueError("Invalid reservation id")
    
  def check_out(self, reservation_id, payment):
    with self.lock:
      reservation = self.reservations.get(reservation_id)
      if reservation and reservation.status == ReservationStatus.CONFIRMED:
        room = reservation.room
        amount = room.price * (reservation.check_out_date - reservation.check_in_date).days
        if payment.process_payment(amount):
          room.check_out()
          del self.reservations[reservation_id]
        else:
          raise ValueError("Payment failed")
      else:
        raise ValueError("Invalid reservation id")
    

hotel_management_system = HotelManagementSystem()

guest1 = Guest("John Doe", "g@example.com", "123456789")
guest2 = Guest("John Doe", "a@example.com", "123456789")

hotel_management_system.add_guest(guest1)
hotel_management_system.add_guest(guest2)

room1 = Room(RoomType.SINGLE, 100.0)
room2 = Room(RoomType.DOUBLE, 200.0)

hotel_management_system.add_room(room1)
hotel_management_system.add_room(room2)

check_in_date = date.today()
check_out_date = check_in_date + timedelta(days=3)
reservation1 = hotel_management_system.book_room(guest1, room1, check_in_date, check_out_date)

if reservation1:
  print(f"Reservation created: {reservation1.id}")
else:
  print("Room not available for booking.")

# Check-in
hotel_management_system.check_in(reservation1.id)
print(f"Checked in: {reservation1.id}")


payment = CreditCardPayment()
hotel_management_system.check_out(reservation1.id, payment)
print(f"Checked out: {reservation1.id}")


