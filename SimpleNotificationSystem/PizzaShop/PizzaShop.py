from enum import Enum

class PizzaSize(Enum):
  SMALL = 1
  MEDIUM = 2
  LARGE = 3
  XL = 4

class Pizza:

  def __init__(self, size, crust, toppings,sauce):
    self.size = size
    self.crust = crust
    self.toppings = toppings
    self.sauce = sauce
  
  def __str__(self):
      toppings_str = ', '.join(self.toppings) if self.toppings else "no"
      return (f"{self.size} pizza with {self.crust} crust, "
              f"{toppings_str} toppings, and {self.sauce} sauce.")

class PizzaBuilder:
  def __init__(self):
    self.reset()
  
  def reset(self):
    self.size = None
    self.crust = None
    self.toppings = []
    self.sauce = None
    return self
  
  def set_crust(self, crust):
    self.crust = crust
    return self
  
  def set_toppings(self, topping):
    self.toppings.append(topping)
    return self
  
  def set_sauce(self, sauce):
    self.sauce = sauce
    return self
  
  def set_size(self, size):
    self.size = size
    return self
  
  def build(self):
    if not (self.size and self.crust and self.sauce):
      raise ValueError("Need crust and sauce")
    
    pizza = Pizza(self.size, self.crust, self.toppings, self.sauce)
    self.reset()
    return pizza

class PizzaStore:
  
  def order_pizza(self, size, crust, toppings, sauce):
    builder = PizzaBuilder()
    builder.set_size(size).set_crust(crust).set_sauce(sauce)
    for topping in toppings:
      builder.set_toppings(topping)
    pizza = builder.build()
    return pizza

if __name__ == "__main__":
    # Initialize the PizzaStore with the PizzaBuilder
    store = PizzaStore()

    
    # Order a pizza with specific properties
    my_pizza = store.order_pizza(
        size="Large",
        crust="Thin",
        toppings=["Pepperoni", "Mushrooms", "Olives"],
        sauce="Tomato"
    )
    
    print(my_pizza)