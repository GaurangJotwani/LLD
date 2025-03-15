from abc import ABC, abstractmethod
from enum import Enum


class FileSystemComponent(ABC):
  @abstractmethod
  def showDetails(self):
    pass

class File(FileSystemComponent):
  def __init__(self, name):
    self.name = name
  
  def showDetails(self):
    print(f"The name of the file is {self.name}")

class Folder(FileSystemComponent):
  def __init__(self, name):
    self.name = name
    self.components = []
  
  def add_file_component(self, fileComponent):
    self.components.append(fileComponent)
  
  def showDetails(self):
    print(f"The name of the Folder is {self.name}")

  def showFolderDetails(self):
    for fileComponent in self.components:
      fileComponent.showDetails()

file1 = File("File1.txt")
file2 = File("File2.txt")
folder = Folder("Documents")

folder.add_file_component(file1)
folder.add_file_component(file2)

subFolder = Folder("Subfolder")

folder.add_file_component(subFolder)

folder.showFolderDetails()
