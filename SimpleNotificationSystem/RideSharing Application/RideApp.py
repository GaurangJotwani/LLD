from enum import Enum

class RideStatus(Enum):
  IDLE = 1
  CREATED = 2
  WITHDRAWN = 3
  COMPLETED = 4

class Ride:
  AMT_PER_KM = 20

  def __init__(self, id, origin, dest, seats):
    self.rideStatus = RideStatus.IDLE
    self.id = id
    self.origin = origin
    self.dest = dest
    self.seats = seats
  
  def calculateFare(isPriorityRider):
    dist = self.dest - self.origin
    disc = 0.75 if isPriorityRider else 1
    if seats < 2:
      return dist * AMT_PER_KM * disc
    else:
      return dist * seats * AMT_PER_KM * disc

class Person:
  def __init__(self, name):
    self.name = name

class Driver(Person):
  def __init__(self, name):
    super().__init__(name)

class Rider(Person):
  def __init__(self, name, id):
    super().__init__(name)
    self.id = id
    self._completed_rides = []
    self.current_ride = None
  
  def createRide(self, id, origin, dest, seats):
    if origin >= dest:
      print("Wrong values of Origin and Destination provided. Cant create ride!")
      return
    self.current_ride = Ride(id, origin, dest, seats)
    self.current_ride.rideStatus = RideStatus.CREATED
      
  def updateRide(self, id, origin, dest, seats):
    if self.current_ride.rideStatus in (RideStatus.WITHDRAWN, RideStatus.COMPLETED) :
      print("Cant update ride that is withdrawn or completed!")
      return
    self.createRide(id, origin, dest, seats)
  
  def withdrawRide(self, id):
    if self.current_ride.rideStatus != RideStatus.CREATED:
      print("Ride wasnt in progress so cannot be withdrawn")
      return
    current_ride.rideStatus = RideStatus.withdrawn
    
  def closeRide(self):
    if self.current_ride.rideStatus != RideStatus.CREATED:
      print("Ride wasnt in progress so cannot be closed")
      return
    
    self.current_ride.RideStatus(RideStatus.COMPLETED)
    self._completed_rides.append(current_ride)
    return current_ride.calculateFare(len(_completed_rides) >= 10)
  
class System:
  def __init__(self, drivers, riders: [Rider]):
    self.drivers = drivers
    self.riders = riders
  
  def createRide(self, riderId, rideId, origin, dest, seats):
    if self.drivers == 0:
      print("No drivers around")
    
    for rider in self.riders:
      if rider.id == riderId:
        rider.createRide(rideId, origin, dest, seats)
        self.drivers -= 1
        break
  
  def updateRide(self, riderId, rideId, origin, dest, seats):
    
    for rider in self.riders:
      if rider.id == riderId:
        rider.updateRide(rideId, origin, dest, seats)
        self.drivers -= 1
        break
  
  def withdrawRide(self, riderId, rideId):
    
    for rider in self.riders:
      if rider.id == riderId:
        rider.withdrawRide(rideId)
        self.drivers += 1
        break
  
  def closeRide(self, riderId):
    
    for rider in self.riders:
      if rider.id == riderId:
        rider.closeRide()
        self.drivers += 1
        break
    


rider = Rider(1, "Lucifer")
driver = Driver("Amenadiel")
rider1 = Rider(2, "Chloe")
rider2 = Rider(3, "Maze")

riders = []
riders.append(rider)
riders.append(rider1)
riders.append(rider2)
system = System(3, riders)

rider.createRide(1, 50, 60, 1)
rider.updateRide(1, 50, 60, 2)


system.createRide(1, 1, 50, 60, 1)
system.withdrawRide(1, 1)
system.updateRide(1, 1, 50, 60, 2)



system.createRide(1, 1, 50, 60, 1);
system.updateRide(1, 1, 50, 60, 2);
