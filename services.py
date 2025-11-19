from classInstall import Postgre_Install
from datetime import datetime as dt
from flask import request
import os
import pandas as pd
import json

def message_flash():
    pass


def danger(action, handle):
            uninstall = Postgre_Install()
            if action == "restore":
                config_list = {
                    'config_status': 'True',
                    'config_date': dt.now().strftime("%m-%d-%y"),
                    'webpage_title': 'Populus Numerus',
                    'company': 'Scanner',
                    'city': 'New York City',
                    'lon': '-74.0060152',
                    'lat': '40.7127281',
                    'weather_key': 'baeb0ce1961c460b651e6a3a91bfeac6',
                    'country': 'us',
                    'news_key': '04fbd2b9df7b49f6b6a626b4a4ae36be'
                }
                for key, value in config_list.items():
                    handle.update_database("config_database", "key", "value", key, value)
                handle.send_query("SELECT * FROM config_database;")
                msg = "Configuration restored to defaults"

            elif action == "clear":
                print("emails cleared")
                handle.send_command("DELETE FROM email_list;")
                handle.send_query("SELECT * FROM email_list;")
                msg = "Email list cleared"
            elif action == "delete_people":
                print("db reset")
                handle.send_command("DELETE FROM people_database;")
                handle.send_query("SELECT * FROM people_database;")
                msg = "Employee database deleted"
            elif action == "delete_timesheets":
                print("db reset")
                handle.send_command("DELETE FROM timesheet_database;")
                handle.send_query("SELECT * FROM timesheet_database;")
                msg = "Timesheet database deleted"
            elif action == "clean":
                uninstall.uninstall_psql()                                   
                msg = "System reinstalled from clean state"
            return msg


# Change a config database value from the keys list
def single_button(key, handle):
    if key in request.form:
        new_value = request.form.get(key)
        handle.update_database("config_database", "key", "value", key, new_value)
        return f"{key} updated to {new_value}"
    return None


def upload(file, handle):
            error = None
            message_list = []
            if file and file.filename:
                filename = file.filename
                allowed_extensions = {'.csv', '.xlsx', '.json'}
                ext = os.path.splitext(filename)[1].lower()
                if ext not in allowed_extensions:
                    error = "Unsupported file type. Please upload a CSV, XLSX, or JSON file."
                else:
                    try:
                        if ext == ".csv":
                            data = pd.read_csv(file)
                        elif ext == ".xlsx":
                            data = pd.read_excel(file)
                        elif ext == ".json":
                            jdata = json.load(file)
                            data = pd.DataFrame(jdata)
                        # Send DataFrame to database
                        for index, row in data.iterrows():
                            try:
                                handle.update_people(
                                    int(row['employee_id']),
                                    {'first_name': row['first_name'],
                                    'last_name': row['last_name'],
                                    'email': row['email'],
                                    'phone': row['phone'],
                                    'pic_path': row['pic_path'],
                                    'employee_role': row['employee_role'],
                                    'position': row['position'],
                                    'department': row['department']})
                                message_list.append(f"{row['first_name']} {row['last_name']} uploaded")
                            except Exception as e_row:
                                message_list.append(f"Skipped {row.get('first_name', 'Unknown')} {row.get('last_name', 'Unknown')} due to error: {e_row}")
                        message_list.insert(0, f"File {filename} uploaded")
                    except Exception as e:
                        error = [f"Failed to import data: {e}"]
                if error is not None:
                    return error
                return message_list
            

def manual_entry(action, req_dict, handle):
    key_list = ['fname', 'lname', 'email', 'pnumber', 'filename', 'role', 'position', 'department']
    variable_list = [first_name, last_name, email, phone, pic_path, employee_role, position, department ] = [None]*8
    try:
        employee_id = int(req_dict['idnumber'])
    except Exception as e:
        error = f"Invalid employee ID: {e}"
    index = 0
    for item in key_list:
        try:
            variable_list[index] = req_dict[item]
            
        except Exception as e:
            error = f"Error parsing {item}: {e}"
        index += 1
        # return redirect(url_for("frontend.settings"))

    if action == "remove":
        try:
            sql ="DELETE FROM people_database WHERE employee_id = %s;" %employee_id
            handle.send_command(sql)
            success = (f"Removed employee ID {employee_id} from the database")
        except Exception as e:
            error = f"Failed to remove entry: {e}"
    else:  # add/update
        try:
            handle.update_people(
                employee_id,
                {'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'pic_path': pic_path,
                'employee_role': employee_role,
                'position': position,
                'department': department})
            sucess = f"{action.title()} operation successful for employee ID {employee_id}"
        except Exception as e:
            error = f"{action.title()} failed: {e}", "error"


