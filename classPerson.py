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
        data = self.look_up()
        if data:
            self.assign(data)
            self.update_DB()
            self.recent_list(20)
        else:
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
        self.recent.insert(0, self.return_data)
        while len(self.recent) > length:
            self.recent.pop(-1)
        return self.recent
    

    def update_DB(self):
        latest = self.handle.send_query(f"""
            SELECT clock_in, clock_out
            FROM timesheet_database
            WHERE employee_id = {self.id}
            ORDER BY clock_in DESC
            LIMIT 1;
        """)
        if not latest:
            self.handle.send_command(f"""
                INSERT INTO timesheet_database (employee_id, clock_in)
                VALUES ({self.id}, NOW());
            """)
            action = "Clock In"
        elif latest[0][1] is None:
            self.handle.send_command(f"""
                UPDATE timesheet_database
                SET clock_out = NOW()
                WHERE employee_id = {self.id}
                AND clock_out IS NULL;
            """)
            action = "Clock Out"
        else:
            self.handle.send_command(f"""
                INSERT INTO timesheet_database (employee_id, clock_in)
                VALUES ({self.id}, NOW());
            """)
            action = "Clock In"
        data = self.handle.send_query(f"""
            SELECT 
                p.first_name,
                p.last_name,
                CASE 
                    WHEN t.clock_out IS NULL THEN t.clock_in 
                    ELSE t.clock_out 
                END AS event_time,
                CASE 
                    WHEN t.clock_out IS NULL THEN 'Clock In' 
                    ELSE 'Clock Out' 
                END AS event_type
            FROM people_database p
            JOIN timesheet_database t ON p.employee_id = t.employee_id
            WHERE p.employee_id = {self.id}
            ORDER BY t.clock_in DESC
            LIMIT 2;
        """)
        if not data:
            self.return_data = f"No time records found for ID {self.id}"
        else:
            time = data[0][2]
            if isinstance(time, str):
                from datetime import datetime
                time = datetime.fromisoformat(time)
            time_str = time.strftime("%I:%M %p %d-%m")
            direction = "==>" if action == "Clock In" else "<=="
            io = "IN"if action == "Clock In" else "OUT"
            self.return_data = f"{io} {time_str} {direction} {data[0][0]} {data[0][1]}"
        print(self.return_data)
        return self.return_data



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