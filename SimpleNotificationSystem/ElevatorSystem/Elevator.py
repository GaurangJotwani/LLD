from enum import Enum
from threading import Lock, Condition, Thread
import time
from collections import deque

class Direction(Enum):
  UP = 1
  DOWN = 2

class Request:
  def __init__(self, source_floor, destination_floor):
    self.source_floor = source_floor
    self.destination_floor = destination_floor

class Elevator:
  def __init__(self, id, capacity):
    self.id = id
    self.capacity = capacity
    self.current_floor = 1
    self.current_direction = Direction.UP
    self.requests = deque()
    self.lock = Lock()
    self.condition = Condition(self.lock)
  
  def add_request(self, request):
    with self.lock:
      if len(self.requests) < self.capacity:
        self.requests.append(request)
        print(f"Elevator {self.id} added request: {request.source_floor} to {request.destination_floor}")
        self.condition.notify_all()
  
  def get_next_request(self):
    with self.lock:
      while not self.requests:
        self.condition.wait()
      return self.requests.popleft()
    
  def process_requests(self):
    while True:
      request = self.get_next_request()
      self.process_request(request)
  
  def process_request(self, request):
    start_floor = self.current_floor
    end_floor = request.destination_floor

    if start_floor < end_floor:
      self.current_direction = Direction.UP
      for i in range(start_floor, end_floor + 1):
        self.current_floor = i
        print(f"Elevator {self.id} reached floor {self.current_floor}")
        time.sleep(1)
    elif start_floor > end_floor:
      self.current_direction = Direction.DOWN
      for i in range(start_floor, end_floor - 1, -1):
        self.current_floor = i
        print(f"Elevator {self.id} reached floor {self.current_floor}")
        time.sleep(1)
  
  def run(self):
    self.process_requests()

class ElevatorController:
  def __init__(self, num_elevators, capacity):
    self.elevators = []
    for i in range(num_elevators):
      elevator = Elevator(i + 1, capacity)
      self.elevators.append(elevator)
      Thread(target=elevator.run).start()
  
  def request_elevator(self, source_floor, destination_floor):
    optimal_elevator = self.find_optimal_elvator(source_floor, destination_floor)
    optimal_elevator.add_request((Request(source_floor, destination_floor)))
  
  def find_optimal_elvator(self, source_floor, destination_floor):
    optimal_elevator = None
    min_dist = float("inf")

    for elevator in self.elevators:
      distance = abs(source_floor - elevator.current_floor)
      if distance < min_dist:
        min_dist = distance
        optimal_elevator = elevator
    
    return optimal_elevator



controller = ElevatorController(3, 5)
time.sleep(3)
controller.request_elevator(10, 12)
time.sleep(3)
controller.request_elevator(1, 7)
time.sleep(3)
controller.request_elevator(2, 5)
time.sleep(3)
controller.request_elevator(1, 9)

try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  print("Elevator stopped.")