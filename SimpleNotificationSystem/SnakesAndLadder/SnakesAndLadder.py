from abc import ABC, abstractmethod
from enum import Enum
import random
from collections import deque
import time

class Dice:
  def __init__(self, dice_cnt):
    self.dice_cnt = dice_cnt
  
  def roll_dice(self):
    total_sum = 0
    for dice in range(self.dice_cnt):
      total_sum += random.randint(1, 6)
    return total_sum

class Jump:
  def __init__(self, start, end):
    self.start = start
    self.end = end

class Cell:
  def __init__(self):
    self.jmp = None

class Player:
  def __init__(self, name, position):
    self.name = name
    self.position = position

class Board:
  def __init__(self, size):
    self.size = size
    self.board = [[Cell() for j in range(size)] for _ in range(size)]
  
  def add_ladders(self, cnt):
    while cnt > 0:
      start = random.randint(1, self.size * self.size)
      end = random.randint(1, self.size * self.size)
      if end > start:
        jmp = Jump(start, end)
        cell = self.get_cell(start)
        cell.jmp = jmp
        cnt -= 1
  
  def add_snakes(self, cnt):
    while cnt > 0:
      start = random.randint(1, self.size * self.size)
      end = random.randint(1, self.size * self.size)
      if end < start:
        jmp = Jump(start, end)
        cell = self.get_cell(start)
        cell.jmp = jmp
        cnt -= 1
  
  def get_cell(self, position):
    row = position // self.size
    col = position % self.size
    return self.board[row][col]
  

class Game:
  def __init__(self, dice_cnt, size, number_of_ladders, number_of_snakes, player_names):
    self.dice = Dice(dice_cnt)
    self.size = size
    self.board = Board(self.size)
    self.board.add_ladders(number_of_ladders)
    self.board.add_snakes(number_of_snakes)
    self.q = deque()
    for player_name in player_names:
      self.q.append(Player(player_name, 1))
  
  def play_game(self):
    winner_found = False
    while not winner_found:
      current_player = self.q.popleft()
      print(f"{current_player.name}'s turn. Current Position: {current_player.position}")
      self.q.append(current_player)
      #Roll the dice
      dice_roll = self.dice.roll_dice()
      print(f"{current_player.name}'s threw {dice_roll}")
      new_position = dice_roll + current_player.position
      if new_position > self.size * self.size: 
        print(f"Went overboard! Stays in the same place")
        continue
      new_position = self.get_new_position(new_position)
      current_player.position = new_position
      print(f"{current_player.name}'s turn. Current Position: {current_player.position}")
      if current_player.position == self.size * self.size:
        print(f"{current_player.name} Wins!")
        winner_found = True

  def get_new_position(self, position):
    if position == self.size * self.size:
      return position
    cell = self.board.get_cell(position)
    if cell.jmp:
      if cell.jmp.start < cell.jmp.end:
        print("Sweet! Found a Ladder")
      else:
        print("Tough Luck! Got bitten by a snake")
      return cell.jmp.end
    return position
      

game = Game(1, 10, 4, 4, ["Goti", "Soni"])
game.play_game()