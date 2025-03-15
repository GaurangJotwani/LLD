# FlexiText Formatter Application Exercise
# You are designing a text editor application that enables users to format their documents using different styles, such as Plain Text, HTML, and Markdown. Each formatting style transforms the document’s content in its own unique way. The application should allow users to switch between these formatting styles at runtime, with the ability to easily incorporate new formatting styles in the future.


# Formatting Specifications:
# Plain Text: Return the text as it is.
# HTML Formatting: Return the text enclosed between <html><body> and </body></html>.
# Markdown Formatting: Return the text enclosed between ** and **.

# Task:

# Implement the formatting functionality using the Strategy Design Pattern to ensure flexibility and maintainability. Your solution should allow users to apply various text formatting strategies while making it easy to add new formats without changing the existing logic.

# Output:
# Your application should apply three different formatting strategies: Plain Text, HTML, and Markdown to the same document. The formatted output should be displayed for each strategy.

from abc import ABC, abstractmethod

class FormatStrategy(ABC):
  def format(self, content: str) -> str:
    pass

class PlainText(FormatStrategy):
  def format(self, content):
    return content

class HTML(FormatStrategy):
  def format(self, content):
    return "<html><body>" + content + "</body></html>"

class Markdown(FormatStrategy):
  def format(self, content):
    return "**" + content + "**"

class FlexiText:
  def __init__(self, content):
    self.format_strategy = PlainText()
    self.content = content
  
  def setFormatStrategy(self, format_strategy):
    self.format_strategy = format_strategy
  
  def setContent(self, content):
    self.content = content
  
  def display(self):
    print(self.format_strategy.format(self.content))

flexi_text = FlexiText("ABC")
flexi_text.display()

flexi_text.setFormatStrategy(Markdown())
flexi_text.display()

flexi_text.setFormatStrategy(HTML())
flexi_text.display()
