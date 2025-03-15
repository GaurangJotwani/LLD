# Media Player Application Exercise
# You are designing a Media Player Application that allows users to play, pause, and stop audio tracks. The media player transitions between different states (e.g., Playing, Paused, Stopped), and each state dictates how the player behaves when the user interacts with the play, pause, or stop buttons.

# For example:
# In the Playing state, pressing the pause button will pause the track, while pressing the stop button will stop it.
# In the Paused state, pressing the play button will resume the track, and pressing the stop button will stop it.
# In the Stopped state, pressing the play button will start the track from the beginning.

# Task:
# Implement the Media Player using the State Design Pattern. Ensure that each state (Playing, Paused, Stopped) is handled by a separate class, and that transitioning between states is done without modifying the behavior of the individual states. Your implementation should allow for easy extension in the future, where more states (e.g., Fast-Forward, Rewind) can be added.

# Output:
# After executing the code, it will simulate the following sequence of state transitions:
# Start playing the track.
# Pause the track.
# Stop the track.
# Each state transition should be clearly reflected in the output, showing how the media player responds to these predefined transitions.

from abc import ABC, abstractmethod

class MediaPlayerState:
  @abstractmethod
  def play(self, media_player):
    pass
  @abstractmethod
  def pause(self, media_player):
    pass
  @abstractmethod
  def stop(self, media_player):
    pass

class StopPlayerState(MediaPlayerState):
  def play(self, media_player):
    print("Music Started to play!")
    media_player.setState(PlayPlayerState())
  
  def pause(self, media_player):
    print("Cant paause while player is stopped!")
  
  def stop(self, media_player):
    print("Player already stopped!")

class PlayPlayerState(MediaPlayerState):
  def play(self, media_player):
    print("Player is already playing music!")
  
  def pause(self, media_player):
    print("Music paused!")
    media_player.setState(PausePlayerState())

  def stop(self, media_player):
    print("Player Stopped!")
    media_player.setState(StopPlayerState())

class PausePlayerState(MediaPlayerState):
  def play(self, media_player):
    print("Player has resumed playing music!")
    media_player.setState(PlayPlayerState())
  
  def pause(self, media_player):
    print("Music already paused!")

  def stop(self, media_player):
    print("Player Stopped!")
    media_player.setState(StopPlayerState())



class MediaPlayer:
  def __init__(self):
    self.player_state = StopPlayerState()
  
  def setState(self, player_state):
    self.player_state = player_state
  
  def play(self):
    self.player_state.play(self)
  
  def pause(self):
    self.player_state.pause(self)

  def stop(self):
    self.player_state.stop(self)

media_player = MediaPlayer()


media_player.play()
media_player.pause()
media_player.pause()
media_player.play()
media_player.stop()



