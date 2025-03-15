from abc import ABC, abstractmethod


class Button(ABC):
  @abstractmethod
  def render(self):
    pass
  def onClick(self, event):
    pass
  
class WindowsButton(Button):
  def render(self, a,b):
    pass
  def onClick(self, event):
    print("on-windows:" + event)

class HTMLButton(Button):
  def render(self, a,b):
    pass
  def onClick(self, event):
    print("on-web:" + event)


class Dialog(ABC):
  @abstractmethod
  def createButton(self):
    pass
  
  def render(self):
    okButton = self.createButton()
    okButton.onClick("Clicked")


class WindowsDialog(Dialog):
  def createButton(self):
    return WindowsButton()

class WebDialog(Dialog):
  def createButton(self):
    return HTMLButton()


dialog = WebDialog()
dialog.render()