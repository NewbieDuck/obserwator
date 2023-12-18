from main import downloadValue as dowValue
import random
import time
class Subject:
    def __init__(self):
        self._observers = []

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass


class price(Subject):
    def __init__(self, name='', ):
        Subject.__init__(self)
        self.name = name
        self._price = 0
        self._currency_rate = 1


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        self.notify()

    def set_currency_rate(self, rate):
        self._currency_rate = rate
        self.notify()


class Viewer:
    def set_name(self, name, surname):
        self.viewer_name = name
        self.viewer_surname = surname

    def update(self, subject):
        print(f'Viewer: {self.viewer_name} {self.viewer_surname} - {subject.name} '
              f'currency exchange rate was changed to {subject._currency_rate}. '
              f'New price of the item is {subject.price} EUR or {round((subject.price * subject._currency_rate), 2)} PLN')



if __name__ == "__main__":
    obj1 = price('Stolik')
    obj2 = price('Komputer')
    obj1.price = 5
    obj2.price = 10

    viewer1 = Viewer()
    viewer2 = Viewer()
    viewer3 = Viewer()
    viewer4 = Viewer()

    viewer1.set_name("Adam", "Małysz")
    viewer2.set_name("Robert", "Kubica")
    viewer3.set_name("Robert", "Lewandowski")
    viewer4.set_name("Kamil", "Stoch")

    obj1.attach(viewer1)
    obj1.attach(viewer2)
    obj1.attach(viewer3)

    obj2.attach(viewer1)
    obj2.attach(viewer2)
    obj2.attach(viewer3)
    obj2.attach(viewer4)

    rates = dowValue()
    old = rates


    while True:

        # random_number = round(random.uniform(4.00, 5.00), 2)
        rates = dowValue()
        if rates != old:
            obj1.set_currency_rate(rates)
            obj2.set_currency_rate(rates)
            old = rates

        time.sleep(5)
        print("mineło 5 sekund")





