from classHandler import Handler
from datetime import datetime as dt

class Reports():
    def __init__(self):
        self.user_handle = Handler("user")


    def get_clocked_in(self):
        query_data = self.user_handle.send_query("""
            SELECT t.work_date, t.clock_in, p.first_name, p.last_name
            FROM people_database p JOIN timesheet_database t
            ON p.employee_id = t.employee_id WHERE t.clock_out IS NULL
            ORDER BY t.work_date DESC , t.clock_in DESC;""")

        data = []
        for row in query_data:
            work_date = row[0].strftime("%m/%d/%Y")
            clock_in = row[1].strftime("%I:%M %p").lstrip("0")
            fname = row[2]
            lname = row[3]

            entry = {work_date: {"clock_in": clock_in, "fname": fname, "lname": lname}}
            data.append(entry)
        #print(data)
        grouped_data = {}
        for item in data:
            for date, person in item.items():
                if date not in grouped_data:
                    grouped_data[date] = []
                grouped_data[date].append(person)

        grouped_list = []
        for date in sorted(grouped_data.keys(), reverse=True):
            grouped_list.append((date, grouped_data[date]))
        #print(grouped_list)
        return grouped_list

    def get_report(self):
        data = self.user_handle.send_query("""
            SELECT t.work_date,t.clock_in, t.clock_out, p.employee_id, p.first_name, p.last_name, p.employee_role, p.position, p.department
            FROM people_database p JOIN timesheet_database t
            ON p.employee_id = t.employee_id
            ORDER BY t.work_date DESC, t.clock_in DESC
            LIMIT 300;""")
        report = []
        for row in data:
            date, clock_in, clock_out, employee_id, first_name, last_name, employee_role, position, department = row

            if clock_out is not None:
                timemath = clock_out - clock_in
                total_seconds = int(timemath.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                duration = f"{hours}:{minutes:02d}"
            else:
                duration = "Clocked In"

            date = date.strftime("%m/%d/%Y")
            clock_in = clock_in.strftime("%I:%M %p").lstrip("0") if clock_in else None
            clock_out = clock_out.strftime("%I:%M %p").lstrip("0") if clock_out else None

            entry = {
                "date": date,
                "clock_in": clock_in,
                "clock_out": clock_out,
                "duration": duration,
                "employee_id": employee_id,
                "fname": first_name,
                "lname": last_name,
                "role": employee_role,
                "position": position,
                "department": department
            }

            report.append(entry)
        print(report)
        return report

        


#r=Reports()
#r.get_clocked_in()
#r.get_report()