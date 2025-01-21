from abc import ABC, abstractmethod
from enum import Enum

class LoggerLevel(Enum):
  INFO = 1
  DEBUG = 2
  ERROR = 3
  SYSTEM = 4

class LogProcessor(ABC):
  def __init__(self, next_log_processor):
    self.next_log_processor = next_log_processor
  
  def log(self, log_level: LoggerLevel, message: str):
    if self.next_log_processor is not None:
      self.next_log_processor.log(log_level, message)

class InfoLogger(LogProcessor):
  def __init__(self, next_log_processor):
    super().__init__(next_log_processor)
  
  def log(self, log_level, message):
    if log_level == LoggerLevel.INFO:
      print("INFO: " + message)
    else:
      super().log(log_level, message)

class ErrorLogger(LogProcessor):
  def __init__(self, next_log_processor):
    super().__init__(next_log_processor)
  
  def log(self, log_level, message):
    if log_level == LoggerLevel.ERROR:
      print("ERROR: " + message)
    else:
      super().log(log_level, message)

class DebugLogger(LogProcessor):
  def __init__(self, next_log_processor):
    super().__init__(next_log_processor)
  
  def log(self, log_level, message):
    if log_level == LoggerLevel.DEBUG:
      print("DEBUG: " + message)
    else:
      super().log(log_level, message)


logger = InfoLogger(ErrorLogger(DebugLogger(None)))

logger.log(LoggerLevel.SYSTEM, "Api latency: 5ms")