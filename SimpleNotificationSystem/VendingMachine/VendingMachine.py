from enum import Enum
from abc import ABC, abstractmethod
from threading import Lock

class Coin(Enum):
  PENNY = 0.01
  NICKEL = 0.05
  DIME = 0.1
  QUARTER = 0.25

class Note(Enum):
  ONE = 1
  FIVE = 5
  TEN = 10
  TWENTY = 20

class Product:
  def __init__(self, name, price):
    self.name = name
    self.price = price

class Inventory:
  def __init__(self):
    self.products = {}
  
  def add_product(self, product, quantity):
    self.products[product] = quantity
  
  def remove_product(self, product):
    del self.products[product]
  
  def update_quantity(self, product, quantity):
    self.products[product] = quantity
  
  def get_quantity(self, product):
    return self.products.get(product, 0)
  
  def is_available(self, product):
    return product in self.products and self.products[product] > 0

class VendingMachine:
  _instance = None
  def __init__(self):
    if not VendingMachine._instance:
      VendingMachine._instance = self
      self.state = IdleState(self)
      self.inventory = Inventory()
      self.coins = []
      self.notes = []
      self.selected_product = None
    else:
      raise("Singleton Class. Call get_instance()")
  
  @staticmethod
  def get_instance():
    return _instance
  
  def set_state(self, state):
    self.state = state
  
  def select_product(self, product):
    self.state.select_product(product)
  
  def insert_coin(self, coin):
    self.state.insert_coin(coin)
  
  def insert_note(self, note):
    self.state.insert_coin(note)
  
  def get_total(self):
    return sum([coin.value for coin in self.coins]) + sum([note.value for note in self.notes]) 
  
  def dispense_product(self):
    self.state.dispense_product()
  
  def return_change(self):
    self.state.return_change()
  
  def reset_payment(self):
    self.coins = []
    self.notes = []
  
  def reset_selected_product(self):
    self.selected_product = None

class VendingMachineState(ABC):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine
  
  @abstractmethod
  def select_product(self, product):
    pass
  
  @abstractmethod
  def insert_coin(self,coin):
    pass
  
  @abstractmethod
  def insert_note(self, note):
    pass
  
  @abstractmethod
  def dispense_product(self):
    pass
  
  @abstractmethod
  def return_change(self):
    pass
  
class IdleState(VendingMachineState):
  def __init__(self, vending_machine):
    super().__init__(vending_machine)
  
  def select_product(self, product):
    if self.vending_machine.inventory.is_available(product):
      self.vending_machine.selected_product = product
      self.vending_machine.set_state(ReadyState(self.vending_machine))
    else:
      print("Product not available")

  def insert_coin(self, coin):
    print("Select Product First")
  
  def insert_note(self, note):
    print("Select Product First")
  
  def dispense_product(self):
    print("Select Product First")
  
  def return_change(self):
    print("No change to return")

class ReadyState(VendingMachineState):
  def __init__(self, vending_machine):
    super().__init__(vending_machine)
  
  def select_product(self, product):
    print("product already selected. Make payment")

  def insert_coin(self, coin):
    self.vending_machine.coins.append(coin)
    print(f"Coin inserted: {coin.name}")
    self.check_payment_status()
  
  def insert_note(self, note):
    self.vending_machine.note.append(note)
    print(f"Note Inserted: {note.name}")
    self.check_payment_status()
  
  def dispense_product(self):
    print("Make payment first")
  
  def return_change(self):
    print("First pay for the product")
  
  def check_payment_status(self):
    if self.vending_machine.get_total() >= self.vending_machine.selected_product.price:
      self.vending_machine.set_state(DispenseState(self.vending_machine))
    else:
      print("Not enough money")

class DispenseState(VendingMachineState):
  def __init__(self, vending_machine):
    super().__init__(vending_machine)
  
  def select_product(self, product):
    print("product already selected. Collect Product")

  def insert_coin(self, coin):
    print("Payment Made. Collect product")
  
  def insert_note(self, note):
    print("Payment Made. Collect product")
  
  def dispense_product(self):
    product = self.vending_machine.selected_product
    self.vending_machine.inventory.update_quantity(product, self.vending_machine.inventory.get_quantity(product) - 1)
    print(f"product dispenced: {product.name}")
    self.vending_machine.set_state(ReturnChangeState(self.vending_machine))
  
  def return_change(self):
    print("Please collect product first")

class ReturnChangeState(VendingMachineState):
  def __init__(self, vending_machine):
    super().__init__(vending_machine)
  
  def select_product(self, product: Product):
      print("Please collect the change first.")

  def insert_coin(self, coin: Coin):
      print("Please collect the change first.")

  def insert_note(self, note: Note):
      print("Please collect the change first.")

  def dispense_product(self):
      print("Product already dispensed. Please collect the change.")

  def return_change(self):
      change = self.vending_machine.get_total() - self.vending_machine.selected_product.price
      if change > 0:
          print(f"Change returned: ${change:.2f}")
          self.vending_machine.reset_payment()
      else:
          print("No change to return.")
      self.vending_machine.reset_selected_product()
      self.vending_machine.set_state(IdleState(self.vending_machine))

vending_machine = VendingMachine()
coke = Product("Coke", 1.5)
water = Product("Water", 2.5)
pepsi = Product("Pepsi", 1)
vending_machine.inventory.add_product(coke, 5)
vending_machine.inventory.add_product(water, 2)
vending_machine.inventory.add_product(pepsi, 3)

vending_machine.select_product(coke)

vending_machine.insert_note(Note.FIVE)
vending_machine.dispense_product()

vending_machine.return_change()