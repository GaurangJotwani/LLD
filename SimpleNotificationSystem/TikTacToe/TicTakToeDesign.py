from enum import Enum
from abc import ABC
from collections import defaultdict, deque

class PieceType(Enum):
  X = 1
  O = 2

class PlayingPiece(ABC):
  def __init__(self, piece_type: PieceType):
    self.piece_type = piece_type

  def get_type(self):
    return self.piece_type

class PlayingPieceX(PlayingPiece):
  def __init__(self):
    super().__init__(PieceType.X)
  def __str__(self):
    return "X"

class PlayingPieceO(PlayingPiece):
  def __init__(self):
    super().__init__(PieceType.O)
  def __str__(self):
    return "O"

class Player:
  def __init__(self, name, playing_piece: PlayingPiece):
    self.name = name
    self.playing_piece = playing_piece

class Board:
  def __init__(self, size:int):
    self.board: [[PlayingPiece]] = [[None] * size for i in range(size)]
    self.size = size
  
  def add_piece(self, r:int, c:int, playing_piece: PlayingPiece):
    if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] is None:
      self.board[r][c] = playing_piece
      return True
    else: return False
  
  def is_full(self):
    for r in range(self.size):
      for c in range(self.size):
        if self.board[r][c] is None:
          return False
    return True
  
  def print_board(self):
    for r in range(self.size):
      for c in range(self.size):
        if self.board[r][c]:
          print("   " + str(self.board[r][c]) + "  ", end = "")
        else:
          print("      ", end = "")
        print(" | ", end="")
      print()

class Game:

  PIECES = {PlayingPieceX(), PlayingPieceO()}

  def __init__(self, size: int, player_names: []):
    if len(player_names) > len(Game.PIECES) or len(player_names) < 2:
      raise ValueError("Not enough pieces or not enough number of players")

    self.q = deque()
    i = 0
    for piece in Game.PIECES:
      self.q.append(Player(player_names[i], piece))
      i += 1
      if i > len(player_names):
        break
    self.board = Board(size)
    self.size = size
  
  def playGame(self):
    found_winner = False

    while not found_winner:
      self.board.print_board()
      current_player = self.q.popleft()

      if self.board.is_full():
        found_winner = True
        continue
      
      print(f"Player: " + current_player.name + " Enter row, column in this format: r,c")
      response = input("")
      values = response.split(",")
      r,c = int(values[0]), int(values[1])

      if not self.board.add_piece(r,c,current_player.playing_piece):
        print("Try Again! Incorrect position chosen")
        self.q.appendleft(current_player)
        continue
      
      self.q.append(current_player)
      winner = self.isThereWinner(r,c,current_player.playing_piece.piece_type)
      if winner:
        print(self.board)
        print(f"winner is {current_player.name}")
        return current_player.name
    return "tie"

  def isThereWinner(self, r, c, piece_type: PieceType):
    rows = defaultdict(int)
    cols = defaultdict(int)
    pos_diags = defaultdict(int)
    neg_diags = defaultdict(int)
    game_board = self.board.print_board()

    for r in range(self.size):
      for c in range(self.size):
        if game_board[r][c] != None and game_board[r][c].piece_type == piece_type:
          rows[r] += 1
          cols[c] += 1
          pos_diags[r + c] += 1
          neg_diags[r - c] += 1
          if rows[r] == self.size or cols[c] == self.size or pos_diags[r + c] == self.size or neg_diags[r - c] == self.size:
            return True
    return False


game = Game(3, ["goti", "soni"])
game.playGame()
    


