
# Flight Control System Application Exercise
# You are tasked with developing a Flight Control System for an airport. The system should manage communication between different components, such as airplanes and the control tower, to ensure safe takeoffs and landings. To improve interactions and decrease dependencies among components, utilize the Mediator Design Pattern with a centralized communication method that enables effective coordination among the various components within the system.

# Requirements:
# Airplane Class: Create an Airplane class representing different airplanes, with properties like ID, status (e.g., "waiting," "landing," "taking off"), and methods to request takeoff or landing.
# ControlTower Mediator: Implement a ControlTower class that serves as the mediator. It will manage the interactions between airplanes and handle their requests for takeoff and landing.
# Request Handling: Airplanes should be able to send requests to the control tower for takeoff or landing. The control tower should validate these requests based on the current air traffic.
# Notifications: The control tower should notify airplanes when their request is approved or denied.


# Implementation Steps:
# Define a Mediator interface with methods for registering airplanes and handling requests.
# Implement the ControlTower class that follows this interface.
# Implement the Airplane class with methods to request takeoff or landing and receive notifications from the control tower.
# Create a simple test case to demonstrate the functionality of the flight control system, including airplane registration and request handling.

# Output:
# After executing the code, it will simulate the following sequence of operations:
# Airplanes are registered with the control tower.
# An airplane requests to take off or land.
# The control tower processes the request and sends notifications to the airplane regarding its status.

from enum import Enum
from abc import ABC, abstractmethod

class Status(Enum):
  WAITING = 1
  LANDING = 2
  TAKING_OFF = 3

class Mediator(ABC):
  
  @abstractmethod
  def requestTakeOff(self, airplane):
    pass
  
  @abstractmethod
  def requestLanding(self, airplane):
    pass
  
  @abstractmethod
  def register(self, airplane):
    pass

class ControlTower(Mediator):

  def __init__(self):
    self.take_off_runways = 2
    self.landing_runways = 2
    self.airplanes = []

  def requestTakeOff(self, airplane):
    if airplane not in self.airplanes:
      return
    
    if self.take_off_runways > 0:
      self.take_off_runways -= 1
      airplane.receiveNotification("Request to Takeoff Granted")
      airplane.setStatus(Status.TAKING_OFF)
    else:
      airplane.receiveNotification("Request to Takeoff Denied")

  
  def requestLanding(self, airplane):
    if airplane not in self.airplanes:
      return
    
    if self.take_off_runways > 0:
      self.landing_runways -= 1
      airplane.receiveNotification("Request to Land Granted")
      airplane.setStatus(Status.LANDING)
    else:
      airplane.receiveNotification("Request to Land Denied")
  
  def register(self, airplane):
    self.airplanes.append(airplane)
    airplane.setMediator(self)



class Airplane:
  def __init__(self, id):
    self.id = id
    self.status = Status.WAITING
    self.mediator = None
  
  def setMediator(self, mediator):
    self.mediator = mediator
  
  def setStatus(self, status):
    self.status = status
  
  def requestTakeOff(self):
    self.mediator.requestTakeOff(self)
  
  def requestLanding(self):
    self.mediator.requestLanding(self)
  
  def receiveNotification(self, msg):
    print(msg)


control_tower = ControlTower()

airplane1 = Airplane(1)
airplane2 = Airplane(2)
airplane3 = Airplane(3)
airplane4 = Airplane(4)

control_tower.register(airplane1)
control_tower.register(airplane2)
control_tower.register(airplane3)
control_tower.register(airplane4)

airplane1.requestLanding()
airplane2.requestTakeOff()
airplane3.requestTakeOff()
airplane4.requestTakeOff()
