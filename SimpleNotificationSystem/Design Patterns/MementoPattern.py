# Graphic Editor Application Exercise
# You are designing a graphic editor application that enables users to create and manipulate various shapes, such as circles, squares, and rectangles. Each shape has attributes, including:

# Position (x, y)
# Color
# Size

# Users should be able to modify these attributes. Additionally, implement an undo feature that allows users to revert any changes made to a shape's attributes.


# Task:
# Implement the undo feature for shape attribute changes using the Memento Design Pattern ensuring that your solution is flexible enough to easily incorporate new shapes or attributes in the future while maintaining the ability to revert all changes.


# Output:
# After executing the code, you should save the shape's attributes to the editor three times using the specified values. Then, perform one undo operation to revert to the previous state. Finally, display the current shape attributes to confirm the changes made by the undo operation.

# Instructions:
# You only need to complete the TODOs mentioned in the code.
# Please do not modify any existing code outside of the specified TODO sections.

class ShapeMemento:
  def __init__(self, position = None, color = None, size = None):
    self.position = position
    self.size = size
    self.color = color

class HistoryManager:
  def __init__(self):
    self.history = []
  
  def push(self, position, color, size):
    self.history.append(ShapeMemento(position, color, size))
  
  def undo(self):
    if self.history:
      self.history.pop()
    return self.history[-1] if self.history else ShapeMemento()

class Shape:
  def __init__(self, position, color, size, historyManager):
    self.position = position
    self.color = color
    self.size = size
    self.historyManager = historyManager
    self.historyManager.push(self.position, self.color, self.size)
  
  def setColor(self, color):
    self.color = color
    self.historyManager.push(self.position, self.color, self.size)

  def setPosition(self, position):
    self.position = position
    self.historyManager.push(self.position, self.color, self.size)
  
  def setSize(self, size):
    self.size = size
    self.historyManager.push(self.position, self.color, self.size)
  
  def restore(self):
    memento = self.historyManager.undo()
    self.position, self.color, self.size = memento.position, memento.color, memento.size
  
  def __str__(self):
    return f"Position: {self.position}, Color: {self.color}, Size: {self.size}"



historyManager = HistoryManager()
circle = Shape((5,5), "Green", 10, historyManager)
circle.setColor("Blue")
circle.setSize(15)
print(circle)

circle.restore()
print(circle)

circle.setSize(12)
circle.setPosition((13,15))
circle.setColor("Green")
print(circle)

circle.restore()
circle.restore()
circle.restore()
circle.restore()
print(circle)