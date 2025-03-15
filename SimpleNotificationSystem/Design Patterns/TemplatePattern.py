# Report Generator Application Exercise
# You are designing a report generation application that allows users to create different types of reports, such as Sales Reports, Employee Reports, and Inventory Reports. Each report has a similar structure but varies in the details and the way data is processed. The application should enable users to generate reports using a template method that defines the skeleton of the report creation process while allowing subclasses to provide specific implementations for certain steps.


# Similarities:
# All reports follow the same overall structure: gathering data, processing data, formatting the report, and printing it.
# Each report type will use a similar method for outputting the final report.

# Differences:
# Each report type will have its own specific implementation for gathering and processing data, reflecting the unique characteristics of the report (e.g., sales figures for Sales Reports, attendance records for Employee Reports, and stock levels for Inventory Reports).

# Task:
# Implement the report generation functionality using the Template Design Pattern. Your solution should allow for the easy addition of new report types while maintaining the overall structure and flow of the report generation process.

# Output:
# Your program should generate three different reports: a Sales Report, an Employee Report, and an Inventory Report, displaying the structured output for each report type.


from abc import abstractmethod, ABC

class Report:
  def __init__(self, type_of_report):
    self.type_of_report = type_of_report

  @abstractmethod
  def gatherData(self):
    pass
  
  @abstractmethod
  def processData(self):
    pass
  
  def generateReport(self):
    self.gatherData()
    self.processData()
    self.formatReport()
    self.printReport()
  
  def formatReport(self):
    print(f"Formatting {self.type_of_report} Report")
  
  def printReport(self):
    print(f"Printing {self.type_of_report} Report")

class EmployeeReport(Report):

  def __init__(self):
    super().__init__("Employee")

  def gatherData(self):
    print("Gathering Employee Data")
  
  def processData(self):
    print("Processing Employee Data")

class SalesReport(Report):
  def __init__(self):
    super().__init__("Sales")

  def gatherData(self):
    print("Gathering Sales Data")
  
  def processData(self):
    print("Processing Sales Data")

class InventoryReport(Report):
  def __init__(self, type_of_report):
    super().__init__("Inventory")

  def gatherData(self):
    print("Gathering Inventory Data")
  
  def processData(self):
    print("Processing Inventory Data")


sales_report = SalesReport()
sales_report.generateReport()
employee_report = EmployeeReport()
employee_report.generateReport()