# Remote Control System Application Exercise
# You are tasked with designing a simple Remote Control System that can operate different household devices such as lights and fans. The system should follow the Command Design Pattern to encapsulate all requests as command objects, allowing for flexible execution of these commands. The system should be designed to support the easy addition of new device commands while maintaining a clear structure for command execution.

# Task:
# Implement a remote control system using the Command Design Pattern that can manage the following operations:
# Turn on and off a light.
# Turn on and off a fan.
# Your implementation should include a command interface that encapsulates the command execution methods.

# Output:
# Your program should allow users to:
# Turn on the light and print a message indicating that the light is on.
# Turn off the light and print a message indicating that the light is off.
# Turn on the fan and print a message indicating that the fan is on.
# Turn off the fan and print a message indicating that the fan is off.

from abc import ABC, abstractmethod

class TVRemoteCommand(ABC):
  @abstractmethod
  def execute(self):
    pass

class TVRemote:
  def turnOnLight(self):
    print("Light turned on!")
  
  def turnOffLight(self):
    print("Light turned off!")
  
  def turnOnFan(self):
    print("Fan turned on!")
  
  def turnOffFan(self):
    print("Fan turned off!")

class TurnOnLight(TVRemoteCommand):
  def __init__(self, tv_remote):
    self.tv_remote = tv_remote
  def execute(self):
    self.tv_remote.turnOnLight()

class TurnOffLight(TVRemoteCommand):
  def __init__(self, tv_remote):
    self.tv_remote = tv_remote
  def execute(self):
    self.tv_remote.turnOffLight()

class TurnOnFan(TVRemoteCommand):
  def __init__(self, tv_remote):
    self.tv_remote = tv_remote
  def execute(self):
    self.tv_remote.turnOnFan()

class TurnOffFan(TVRemoteCommand):
  def __init__(self, tv_remote):
    self.tv_remote = tv_remote
  def execute(self):
    self.tv_remote.turnOffFan()

class TVRemoteButton:
  def __init__(self, command = None):
    self.command = command

  def setCommand(self, command):
    self.command = command
  
  def clickButton(self):
    self.command.execute()

tv_remote = TVRemote()
turnOffFan = TurnOffFan(tv_remote)
turnOnFan = TurnOnFan(tv_remote)
turnOffLight = TurnOffLight(tv_remote)
turnOnLight = TurnOffLight(tv_remote)

remote_button_fan_off = TVRemoteButton(turnOffFan)
remote_button_fan_on = TVRemoteButton(turnOnFan)

print(remote_button_fan_off)

remote_button_fan_off.clickButton()
remote_button_fan_on.clickButton()

remote_button_fan_off.setCommand(turnOffLight)
remote_button_fan_off.clickButton()






