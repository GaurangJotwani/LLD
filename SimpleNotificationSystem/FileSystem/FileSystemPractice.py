from abc import ABC, abstractmethod
from collections import deque

class Entry(ABC):
  def __init__(self, name):
    self.name = name
  
  def getName(self):
    return self.name
  
  @abstractmethod
  def isDirectory(self):
    pass
  
  @abstractmethod
  def getSize(self):
    pass

class Directory(Entry):
  def __init__(self, name):
    super().__init__(name)
    self.components : [Entry] = [] #
    self.directories = []

  def isDirectory(self):
    return True
  
  def getSize(self):
    total_size = 0
    for component in self.components:
      total_size += component.getSize()
    for directory in self.directories:
      total_size += directory.getSize()
    return total_size
  
  def addEntry(self, entry):
    if entry.isDirectory():
      self.directories.append(entry)
    else:
      self.components.append(entry)
  
  def __str__(self):
    return f"Directory: {self.name}"
  
class File(Entry):
  def __init__(self, name, size, content):
    super().__init__(name)
    self.ext = name.split(".")[-1]
    self.content = content
    self.size = size

  def isDirectory(self):
    return False
  
  def getSize(self):
    return self.size
  
  def __str__(self):
    return f"File: {self.name}"


class IFilter(ABC):
  @abstractmethod
  def isValid(self, file):
    pass

class ExtensionFilter(IFilter):
  def __init__(self,ext):
    self.ext = ext

  def isValid(self, file):
    return file.ext == self.ext

class NameFilter(IFilter):
  def __init__(self,name):
    self.name = name

  def isValid(self, file):
    return file.ext == self.name

class MaxSizeFilter(IFilter):
  def __init__(self,max_size):
    self.max_size = size

  def isValid(self, file):
    return file.size <= self.max_size

class MinSizeFilter(IFilter):
  def __init__(self,min_size):
    self.min_size = min_size

  def isValid(self, file):
    return file.size >= self.min_size

class Search:
  def __init__(self, filter_list:[IFilter]):
    self.filter_list = filter_list
  
  def search(self, root_dir):
    res = []
    q = deque()
    q.append(root_dir)

    while q:
      c_dir = q.popleft()
      for dr in c_dir.directories:
        q.append(dr)
      
      for file in c_dir.components:
        all_valid = True
        for fltr in self.filter_list:
          if not fltr.isValid(file):
            all_valid = False
            break
        if all_valid:
          res.append(file)
    return res

xml_file = File("aaa.xml", 5, "<hey!>")
text_file = File("aaab.xml", 1, "aaaaa")
json_file = File("aaa.json", 20, '"hey": {hey!}')
large_file = File("large.bin", 500, "binary data")

dir1 = Directory("dir1")
dir1.addEntry(text_file)
dir1.addEntry(xml_file)

dir0 = Directory("dir0")
dir0.addEntry(json_file)
dir0.addEntry(large_file)
dir0.addEntry(dir1)

xml_filter = ExtensionFilter("xml")
json_filter = ExtensionFilter("json")
min_size_filter = MinSizeFilter(5)

search_xml_above_5 = Search([json_filter])
for file in search_xml_above_5.search(dir0):
  print(file)