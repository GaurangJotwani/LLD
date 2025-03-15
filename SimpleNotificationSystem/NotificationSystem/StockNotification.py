from abc import ABC, abstractmethod

class StocksObservable(ABC):
    @abstractmethod
    def add(self, observer: NotificationAlertObserver):
        pass
    @abstractmethod
    def remove(self, observer: NotificationAlertObserver):
        pass
    @abstractmethod
    def notify(self):
        pass
    @abstractmethod
    def setStockCount(self):
        pass
    @abstractmethod
    def getStockCount(self):
        pass

class NotificationAlertObserver(ABC):
    @abstractmethod
    def update(self):
        pass

class EmailNotificationObserver(NotificationAlertObserver):
    def __init__(self, email: str, observable: StocksObservable):
        self.email = email
        self.observable  = observable

    def update(self):
        self.sendEmail(self.observable.getStockCount())

    def sendEmail(self, stock):
        print(f"Sending email to {self.email}. Current Stock: {stock}")

class PhoneNotificationObserver(NotificationAlertObserver):
    
    def __init__(self, phoneNumber: str, observable: StocksObservable):
        self.phone = phoneNumber
        self.observable  = observable

    def update(self):
        self.sendSMS(self.observable.getStockCount())

    def sendSMS(self, stock):
        print(f"Sending SMS to {self.phone}. Current Stock: {stock}")

class IphoneObervableImpl(StocksObservable):
    def __init__(self):
        self.notificationObservers = []
        self.stock = 0

    def add(self, observer: NotificationAlertObserver):
        self.notificationObservers.append(observer)

    def remove(self):
        self.notificationObservers.remove(observer)
    
    def notify(self):
        for observer in self.notificationObservers:
            observer.update()
    
    def setStockCount(self, newStock: int):
        if self.stock == 0:
            self.stock += newStock
            self.notify()
        else:
            self.stock += newStock

    def getStockCount(self):
        return self.stock

iphone_observable = IphoneObervableImpl()

email_notification1 = EmailNotificationObserver("gaurangjotwani@gmail.com", iphone_observable)
email_notification2 = EmailNotificationObserver("xyz@gmail.com", iphone_observable)
phone_notification1 = PhoneNotificationObserver("2176488657", iphone_observable)

iphone_observable.add(email_notification1)
iphone_observable.add(email_notification2)
iphone_observable.add(phone_notification1)

iphone_observable.setStockCount(5)
iphone_observable.setStockCount(10)