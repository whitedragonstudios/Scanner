import datetime as dt

from classHandler import Handler
import databaseConfig
db = databaseConfig. databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]

class Person():
    def __init__(self, idnumber):
        self.id = idnumber
        self.handler = Handler(user=user, password=password, dbname=db_name, port=port, host=host)
        #self.insert_test()
        data = self.look_up()
        self.assign(data)
    def look_up(self):
        employee = self.handler.send_query(f"""
            SELECT employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department
            FROM people_database
            WHERE employee_id = {self.id}
        """)
        employee = employee[0]
        return employee


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
        return data


    def insert_test(self):
        self.handler.send_command("""INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES
(1111, 'Han', 'Solo', 'hsolo@scanner.com', '100-555-1976', '1111.jpg', 'Scoundrel', 'Pilot', 'Only in it for the money'),
(1112, 'Luke', 'Skywalker', 'lskywalker@scanner.com', '100-555-1978', '1112.jpg', 'Jedi Master', 'Like his father', 'Peace and Justice');""")


class Default_Person:
    def __init__(self):
        self.idnumber = "0001"
        self.fname = "Marcus"
        self.lname = "Aurelius"
        self.email = "marcus.aurelius@scanner.com"
        self.phone = "800-555-0001"
        self.pic = "default.jpg"
        self.role = "Emperor of Rome"
        self.position = "Stoic"
        self.department = "Being Betrayed"