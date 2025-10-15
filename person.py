import datetime as dt

# Person class is created with each scan to temporaily hold DB infromation before sending it to flask.
class Person():
    # Upon init idnumber is passed to object and name_look_up method is called. 
    def __init__(self, idnumber):
        self.name, self.id, self.group, self.picture = self.name_look_up(idnumber) #uses a tuple for now postgre may return different datatype
    # welcome message is a none user facing method to help check object functionality
    def welcome_message(self):
        current = dt.now().strftime("%m-%d-%y")
        print(f"[Welcome,\n{self.name.title()} your clock in time is {current}. \nHave a wonderful day.")
    # name look up will access postgre server and retrieve name group and picture filename.
    def name_look_up(self, scanned_id):
        scanned_id = "42"
        name = "Jojo"
        group = "Nightshift"
        filename = "default.jpg"
        return name, scanned_id, group, filename

