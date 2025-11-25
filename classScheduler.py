from classHandler import Handler
from datetime import datetime as dt, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class search_event():
    def __init__(self, search, field, num_entries = 10, autorun = True):
        self.search = search.title().strip().replace("'", "''")
        self.field = field
        self.num_entries = num_entries or 10
        self.search_handle = Handler("user")
        if autorun == True:
            self.assign()
    
    def field_parser(self):
        
        base_query = """SELECT employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department"""
        if self.field == "name":
            twoName = self.search.split()
            if len(twoName) >1:
                fname = twoName[0]
                lname = twoName[1]
            else:
                fname = lname = twoName[0]
            query = f"""
                {base_query},
                (CASE
                    WHEN first_name = '{fname}' AND last_name = '{lname}' THEN 4
                    WHEN first_name LIKE '{fname}%' AND last_name LIKE '{lname}%' THEN 3
                    WHEN first_name ILIKE '%{fname}%' OR last_name ILIKE '%{fname}%' THEN 2
                    WHEN first_name LIKE '{lname}%' AND last_name LIKE '{fname}%' THEN 1
                    ELSE 0
                END) AS score
                FROM people_database
                WHERE first_name ILIKE '%{fname}%' 
                OR last_name ILIKE '%{fname}%'
                OR first_name ILIKE '%{lname}%' 
                OR last_name ILIKE '%{lname}%'
                ORDER BY score DESC, last_name, first_name
            """
        elif self.field == "idnumber":
            query = f"""
                {base_query},
                (CASE WHEN employee_id = '{self.search}' THEN 1 ELSE 0 END) AS score
                FROM people_database
                WHERE employee_id = '{self.search}'
                ORDER BY score DESC"""
        elif self.field == "email":
            s_lower = self.search.lower()
            query = f"""
                {base_query},
                (CASE WHEN LOWER(email) = '{s_lower}' THEN 3
                      WHEN LOWER(email) LIKE '{s_lower}%' THEN 2
                      WHEN LOWER(email) LIKE '%{s_lower}%' THEN 1
                      ELSE 0 END) AS score
                FROM people_database
                WHERE LOWER(email) LIKE '%{s_lower}%'
                ORDER BY score DESC
            """
        elif self.field == "phone":
            query = f"""{base_query}
                FROM people_database WHERE phone = '{self.search}'"""
        elif self.field in ["role", "position", "department"]:
            query = f"""
                {base_query},
                (CASE WHEN {self.field} = '{self.search}' THEN 3
                      WHEN {self.field} LIKE '{self.search}%' THEN 2
                      WHEN {self.field} LIKE '%{self.search}%' THEN 1
                      ELSE 0 END) AS score
                FROM people_database
                WHERE {self.field} LIKE '%{self.search}%'
                ORDER BY score DESC"""
        else:
            print("Error classScheduler.fieldparser: Field not valid")

        try:
            result = self.search_handle.send_query(query)
        except Exception as e:
            print(f"Error classSchedule.field_parser: {e}")
            result=[("", "Error", "Field Parser", "", "", "", "", "", "", 0)]


        columns = ["employee_id", "first_name", "last_name", "email", "phone", "pic_path", "employee_role", "position", "department", "score"]
        result = [dict(zip(columns, row)) for row in result]
        return result
    
    def format_time(self, value):
        if value is None:
            return "-----"
        if isinstance(value, str):
            value = dt.fromisoformat(value)
        if isinstance(value, dt):
            return value.strftime("%I:%M %p")
        if isinstance(value, date):
            return value.strftime("%d-%m-%Y")
        return str(value)

    def time_parser(self, idnumber):
        try:
            query = f"""
                SELECT id, employee_id, clock_in, clock_out, work_date
                FROM timesheet_database
                WHERE employee_id = {idnumber}
                ORDER BY clock_in DESC
                LIMIT {self.num_entries}"""
            result = self.search_handle.send_query(query)
        except Exception as e:
            print(f"Error classSchedule.time_parser: {e}")
            return []

        time_list = []
        for item in result:
            # Keep original datetime objects for calculation
            clockin_dt = item[2] if isinstance(item[2], dt) else dt.fromisoformat(item[2]) if item[2] else None
            clockout_dt = item[3] if isinstance(item[3], dt) else dt.fromisoformat(item[3]) if item[3] else None
            
            # Format for display
            clockin = self.format_time(item[2])
            clockout = self.format_time(item[3])
            date_str = self.format_time(item[4])
            
            # Calculate duration using datetime objects
            if clockin_dt is not None and clockout_dt is not None:
                duration_delta = clockout_dt - clockin_dt
                # Format duration as hours:minutes
                total_seconds = int(duration_delta.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                duration = f"{hours}h {minutes}m"
            else: 
                duration = "-----"
                
            clock_row = {
                "clockin": clockin, 
                "clockout": clockout,
                "date": date_str,
                "duration": duration
            }
            time_list.append(clock_row)
        
        return time_list
    

    def assign(self):
        people_list = self.field_parser()
        index = 0
        for person in people_list: 
            ten_times = self.time_parser(person["employee_id"])
            people_list[index]["times"] = ten_times
            index +=1
        self.results = people_list
        return people_list
        

class mailer():
    def __init__(self):
        self.mail_handle = Handler("user")

    def send_now(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587) # Adjust for your email provider
            server.starttls() # Enable TLS encryption
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            server.quit() # Close the connection

    def compose_email(self):
        sender_email = "your_email@example.com"
        sender_password = "your_app_password" # Use an app password for security
        receiver_email = "recipient_email@example.com"
        subject = "Test Email from Python"
        body = "This is a test email sent using Python."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

    def get_emails(self):
        data = self.mail_handle.send_query("SELECT * FROM email_list")
        mailing_list = {}
        for item in data:
            email = item[0]
            freq = item[1]
            mailing_list[freq] = email
        return mailing_list


class present():
    def __init__(self):
        pass