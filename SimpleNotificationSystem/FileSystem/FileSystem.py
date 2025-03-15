from abc import ABC, abstractmethod
from collections import deque

class Entry(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def isDirectory(self):
        pass

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

class File(Entry):
    def __init__(self, name, size, content):
        super().__init__(name)
        self.content = content
        self.size = size

    def isDirectory(self):
        return False

    def getSize(self):
        return self.size

    def getExtension(self):
        return self.name.split(".")[-1]

    def __str__(self):
        return f"File: {self.name}"

class Directory(Entry):
    def __init__(self, name):
        super().__init__(name)
        self.entries = []

    def isDirectory(self):
        return True

    def getSize(self):
        return sum(entry.getSize() for entry in self.entries)

    def addEntry(self, entry):
        self.entries.append(entry)

    def __str__(self):
        return f"Directory: {self.name}"

# Filters now take values in their constructors
class IFilter(ABC):
    @abstractmethod
    def isValid(self, file):
        pass

class ExtensionFilter(IFilter):
    def __init__(self, extension):
        self.extension = extension

    def isValid(self, file):
        return file.getExtension() == self.extension

class MinSizeFilter(IFilter):
    def __init__(self, min_size):
        self.min_size = min_size

    def isValid(self, file):
        return file.getSize() >= self.min_size

class MaxSizeFilter(IFilter):
    def __init__(self, max_size):
        self.max_size = max_size

    def isValid(self, file):
        return file.getSize() <= self.max_size

class NameFilter(IFilter):
    def __init__(self, name):
        self.name = name

    def isValid(self, file):
        return file.getName() == self.name

# Combining filters using AND and OR
class AndFilter(IFilter):
    def __init__(self, *filters):
        self.filters = filters

    def isValid(self, file):
        return all(f.isValid(file) for f in self.filters)

class OrFilter(IFilter):
    def __init__(self, *filters):
        self.filters = filters

    def isValid(self, file):
        return any(f.isValid(file) for f in self.filters)

class FileSearcher:
    def __init__(self, filter_strategy: IFilter):
        self.file_filter = filter_strategy

    def search(self, dr):
        files = []
        q = deque([dr])

        while q:
            folder = q.popleft()
            for entry in folder.entries:
                if entry.isDirectory():
                    q.append(entry)
                else:
                    if self.file_filter.isValid(entry):
                        files.append(entry)

        return files

# Test setup
xml_file = File("aaa.xml", 5, "<hey!>")
text_file = File("aaa.txt", 5, "aaaaa")
json_file = File("aaa.json", 20, '"hey": {hey!}')
large_file = File("large.bin", 500, "binary data")

dir1 = Directory("dir1")
dir1.addEntry(text_file)
dir1.addEntry(xml_file)

dir0 = Directory("dir0")
dir0.addEntry(json_file)
dir0.addEntry(large_file)
dir0.addEntry(dir1)

# Define OR filter for XML or JSON files
or_filter = OrFilter(ExtensionFilter("xml"), ExtensionFilter("json"), MinSizeFilter(5))

# Define AND filter for files with size >= 10 and name "large.bin"
and_filter = AndFilter(MinSizeFilter(10), NameFilter("large.bin"))

# Create a searcher using the OR filter (find XML or JSON files)
searcher_or = FileSearcher(or_filter)
files_or = searcher_or.search(dir0)

# Print results for OR filter
print("\nFiles matching OR filter (XML or JSON):")
for file in files_or:
    print(file)

# Create a searcher using the AND filter (find large.bin if it's >= 10 bytes)
searcher_and = FileSearcher(and_filter)
files_and = searcher_and.search(dir0)

# Print results for AND filter
print("\nFiles matching AND filter (MinSize >= 10 and Name = 'large.bin'):")
for file in files_and:
    print(file)
