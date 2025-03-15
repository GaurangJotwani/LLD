# Stock Price Monitoring System Application Exercise
# You are developing a stock price monitoring system that implements the Observer Design Pattern to notify investors (observers) whenever there is a significant change in stock prices (subject). The system should allow multiple investors to track different stocks and get notified about price fluctuations.

# Requirements:
# Subject (Stock Market):
# The stock market should maintain a list of observers (investors).
# It should have methods to register, remove, and notify observers.
# The setStockPrice method should update the stock price for a specific stock and notify all registered observers only if the price change exceeds a predefined threshold.

# Observers:
# Create two observer classes (e.g., InvestorA and InvestorB) that implement a common Observer interface.
# Each observer should implement an update method to receive notifications about stock price changes
# Data Representation:
# Each stock can have attributes like stock symbol, current price, and a threshold for notification (e.g., a percentage change).

# Output:
# The program will register two observers (InvestorA and InvestorB).
# It will notify both observers of significant stock price changes that exceed the predefined threshold.
# If an observer is removed, they will no longer receive notifications for subsequent price changes.
# The output will confirm which investors received notifications, showcasing the observer design pattern in action.

from abc import abstractmethod, ABC

class StockObserver(ABC):
  def update(self, stock_name, data):
    pass

class Observable(ABC):
  @abstractmethod
  def attach(self, observer):
    pass
  @abstractmethod
  def detach(self, observer):
    pass
  @abstractmethod
  def notify(self):
    pass

class Stock(Observable):
  def __init__(self, current_price, symbol, threshold):
    self.current_price = current_price
    self.symbol = symbol
    self.threshold = threshold
    self.subscribers = []
  
  def setCurrentPrice(self, price):
    diff = abs(price - self.current_price)
    self.current_price = price
    if diff > self.threshold:
      self.notify()
  
  def attach(self, observer):
    self.subscribers.append(observer)
  
  def detach(self, observer):
    self.subscribers.remove(observer)
  
  def notify(self):
    for subscriber in self.subscribers:
        subscriber.update(self.symbol, self.current_price)


class Investor(StockObserver):
  def __init__(self, name):
    self.name = name
  
  def update(self, stock_name, price):
    print(f"Message sent to {self.name}: {stock_name} has had a price fluctuation. Current Price: {price}")
  


AmazonStock = Stock(500, "AMZN", 5)
AppleStock = Stock(300, "APPL", 6)

InvestorA = Investor("A")
InvestorB = Investor("B")

AmazonStock.attach(InvestorA)
AmazonStock.attach(InvestorB)

AppleStock.attach(InvestorB)

AmazonStock.setCurrentPrice(498)
AmazonStock.setCurrentPrice(504)

AppleStock.setCurrentPrice(307)

AmazonStock.detach(InvestorB)
AmazonStock.setCurrentPrice(510)