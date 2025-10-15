from time import dt

class Person():
    def __init__(self):
        self.name = name
        self.id = idnumber
        self.group = group
    def welcome_message(self):
        current = dt.now()
        print(f"[Welcome,\n{self.name.title()} your clock in time is {current}. \nHave a wonderful day.")
