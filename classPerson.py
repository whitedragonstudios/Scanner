import datetime as dt
from datetime import datetime as dt
from classHandler import Handler
import databaseConfig
db = databaseConfig. databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]

class Person():
    def __init__(self, idnumber, recent_list):
        self.id = int(idnumber)
        self.recent = recent_list
        self.handle = Handler(user=user, password=password, dbname=db_name, port=port, host=host)
        #self.insert_test()
        data = self.look_up()
        if data:
            self.assign(data)
            #self.update_DB()
        else:
            # fallback to default person
            data = Default_Person(self.recent)
            self.assign([data.idnumber, data.fname, data.lname, data.email, data.phone, data.pic, data.role, data.position, data.department])



    def look_up(self):
        employee = self.handle.send_query(f"""
            SELECT employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department
            FROM people_database
            WHERE employee_id = {self.id}
        """)
        if not employee:
            return None
        return employee[0]


    def assign(self, data):
        self.idnumber = data[0]
        self.fname = data[1]
        self.lname = data[2]
        self.email = data[3]
        self.phone = data[4]
        self.pic = data[5]
        self.role = data[6]
        self.position = data[7]
        self.department = data[8]
        self.date=dt.now().strftime("%m-%d-%y")
        self.time=dt.now().strftime("%H:%M")
        return data

    def recent_list(self, length):
        person_string = f"{self.time} ==> {self.fname} {self.lname}"
        self.recent.insert(0, person_string)
        while len(self.recent) > length:
            self.recent.pop(-1)
        return self.recent
    

    def update_DB(self):
        self.handle.send_query(f"""WITH updated AS (UPDATE timesheet_database SET clock_out = NOW() WHERE employee_id = {self.id} AND clock_out IS NULL RETURNING *)
            INSERT INTO timesheet_database (employee_id) SELECT {self.id} WHERE NOT EXISTS (SELECT 1 FROM updated);""")
        #self.handle.send_command(f"INSERT INTO timesheet_database employee_id) VALUES {self.idnumber};")


    def insert_test(self):
        self.handler.send_command("""INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES
(1111, 'Han', 'Solo', 'hsolo@scanner.com', '100-555-1976', '1111.jpg', 'Scoundrel', 'Pilot', 'Only in it for the money'),
(1112, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '1112.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice');""")


class Default_Person:
    def __init__(self, recent_list):
        self.idnumber = "0000"
        self.fname = "Error"
        self.lname = "Invalid ID"
        self.email = " "
        self.phone = " "
        self.pic = "default.jpg"
        self.role = " "
        self.position = " "
        self.department = " "
        self.recent = recent_list
        self.time=dt.now().strftime("%H:%M")
    def recent_list(self, length):
        person_string = f"{self.time} ==> {self.fname} {self.lname}"
        self.recent.insert(0, person_string)
        while len(self.recent) > length:
            self.recent.pop(-1)
        return self.recent