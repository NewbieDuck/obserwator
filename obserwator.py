import threading
import customtkinter
from main import downloadValue as dowValue
import random
import time
import customtkinter as ct


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


class Price(Subject):
    def __init__(self, name=''):
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


def set():
    obj1 = Price('Stolik')
    obj2 = Price('Komputer')
    obj1.price = 5
    obj2.price = 10
    app.create_show_observer_button(obj1)
    app.create_show_observer_button(obj2)

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
    table_of_obj = [obj2, obj1]

    return table_of_obj


class CustomTkApp(ct.CTk):
    def __init__(self):
        super().__init__()

    def monitor_changes(self, table):
        old = dowValue()
        while True:
            random_number = round(random.uniform(4.00, 5.00), 2)
            # rates = dowValue()

            if random_number != old:
                for i in table:
                    i.set_currency_rate(random_number)
                old = random_number

            time.sleep(10)

    def start_monitor_thread(self, table):
        monitor_thread = threading.Thread(target=self.monitor_changes, args=(table))
        monitor_thread.start()

    def create_toggle_button(self, obj, viewer):
        basic_text = f"Detach/Attach {viewer.viewer_name} {viewer.viewer_surname} to {obj.name}"
        if viewer in obj._observers:
            var = customtkinter.StringVar(value="on")
        else:
            var = customtkinter.StringVar(value="off")

        switch_button = ct.CTkSwitch(self, text=basic_text, variable=var, onvalue="on", offvalue="off",
                                     command=lambda: self.toggle_observer(obj, viewer))
        switch_button.pack()

    def toggle_observer(self, obj, viewer):
        if viewer in obj._observers:
            obj.detach(viewer)
            print(f"{viewer.viewer_name} {viewer.viewer_surname} detached from {obj.name}")
        else:
            obj.attach(viewer)
            print(f"{viewer.viewer_name} {viewer.viewer_surname} attached to {obj.name}")

    def create_show_observer_button(self, obj):
        show_observer_button = ct.CTkButton(self, text=f"Show observers: {obj.name}  ",
                                            command=lambda: self.show_observers(obj))
        show_observer_button.pack()

    def show_observers(self, obj):
        list_of_observers = obj._observers
        print(f"Observers for item {obj.name}")
        for i in list_of_observers:
            print(i.viewer_name, i.viewer_surname)


if __name__ == "__main__":
    app = CustomTkApp()
    app.geometry("600x500")
    app.title("Observer")
    table = set()
    app.start_monitor_thread(table)

    for i in table:
        viewer = Viewer()
        viewer.set_name("John", "Doe")
        i.attach(viewer)
        app.create_toggle_button(i, viewer)

    app.mainloop()
