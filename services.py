from classInstall import Postgre_Install
from datetime import datetime as dt
from flask import request
import os, json, re, pandas as pd


def danger(action, handle):
    messages = {"error": [], "warning": [], "info": [], "success": []}
    if action == "restore":
        print("restoring default config")
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
            try:
                handle.update_database("config_database", "key", "value", key, value)
                messages["success"].append(f"{key} reset to {value}")
            except Exception as e:
                messages["error"].append(f"Failed to reset {key}\n{e}")
        return messages

    elif action == "clear":
        try:
            print("clearing email list")
            handle.send_command("DELETE FROM email_list;")
            messages["success"].append("Email list deleted")
        except Exception as e:
            messages["error"].append(f"Failed to clear email list.\n{e}")
        return messages
    
    elif action == "delete_people":
        try:
            print("db reset")
            handle.send_command("DELETE FROM people_database;")
            messages["success"].append("Employee database deleted")
        except Exception as e:
            messages["error"].append(f"Failed to delete people database.\n{e}")
        return messages
    
    elif action == "delete_timesheets":
        try:
            print("db reset")
            handle.send_command("DELETE FROM timesheet_database;")
            handle.send_query("SELECT * FROM timesheet_database;")
            messages["success"].append("Timesheet database deleted")
        except Exception as e:
            messages["error"].append(f"Failed to delete timesheet database.\n{e}")
        return messages
    
    elif action == "clean":
        try:
            print("!!! System Reinstall !!!")
            uninstall = Postgre_Install()
            uninstall.uninstall_psql()
            return
        except Exception as e:
            print(f"Failed to uninstall PostgreSQL\n\n{e}")                              
            messages["error"].append(f"Failed to uninstall PostgreSQL\n{e}")
            return messages


# Change a config database value from the keys list
def single_button(key, handle):
    messages = {"error": [], "warning": [], "info": [], "success": []}
    if key in request.form:
        try:
            new_value = request.form.get(key)
            handle.update_database("config_database", "key", "value", key, new_value)
            messages["success"].append(f"{key} updated to {new_value}")
        except Exception as e:
            messages["error"].append(f"Failed to update {key}: {e}")
    return messages


def upload(file, handle):
    messages = {"error": [], "warning": [], "info": [], "success": []}
    if file and file.filename:
        filename = file.filename
        allowed_extensions = {'.csv', '.xlsx', '.json'}
        ext = os.path.splitext(filename)[1].lower()
        if ext not in allowed_extensions:
            messages['error'].append("Unsupported file type. Please upload a CSV, XLSX, or JSON file.")
        else:
            try:
                if ext == ".csv":
                    data = pd.read_csv(file)
                    messages['info'].append(f"CSV file {filename} loaded.")
                elif ext == ".xlsx":
                    data = pd.read_excel(file)
                    messages['info'].append(f"Excel file {filename} loaded.")
                elif ext == ".json":
                    jdata = json.load(file)
                    data = pd.DataFrame(jdata)
                    messages['info'].append(f"JSON file {filename} loaded.")
                # Send DataFrame to database
                for index, row in data.iterrows():
                    print(f"Processing row {index+1}")
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
                        messages['success'].append(f"{row['first_name']} {row['last_name']} added to database.")
                    except Exception as e:
                        messages['error'].append(f"Skipped {row['employee_id']} = {row.get('first_name', 'Unknown')} {row.get('last_name', 'Unknown')} due to error\n{e}")
            except Exception as e:
                messages['error'].append(f"Failed to import data\n{e}")
        return messages
    else:
        messages['error'].append("No file selected for upload.")
        return messages
            

def manual_entry(action, req_dict, handle):
    messages = {"error": [], "warning": [], "info": [], "success": []}
    try:
        employee_id = int(req_dict.get('idnumber'))
        messages['info'].append(f"Processing employee ID {employee_id}")
    except (ValueError, TypeError) as e:
        messages['error'].append(f"Invalid employee ID\n{e}")
        return messages
    first_name = req_dict.get('fname', '').strip().title()
    last_name = req_dict.get('lname', '').strip().title()
    email = req_dict.get('email', '').strip().lower()
    phone = req_dict.get('pnumber', '').strip()
    pic_path = req_dict.get('filename', '').strip()
    employee_role = req_dict.get('role', '').strip().title()
    position = req_dict.get('position', '').strip().title()
    department = req_dict.get('department', '').strip().title()
    
    print(f"Manual entry data: fname={first_name}, lname={last_name}")

    if action == "remove":
        try:
            handle.send_command(f"DELETE FROM people_database WHERE employee_id = {employee_id};")
            handle.send_query(f"SELECT * FROM people_database WHERE employee_id = {employee_id};") 
            messages['warning'].append(f"Removed employee ID {employee_id} from the database")
        except Exception as e:
            messages['error'].append(f"Failed to remove entry {employee_id}\n{e}")
    else:  # add/update
        try:
            msg = handle.update_people(
                employee_id,
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'pic_path': pic_path,
                    'employee_role': employee_role,
                    'position': position,
                    'department': department
                })
            messages = {k: messages[k] + msg[k] for k in messages}
        except Exception as e:
            messages['error'].append(f"Failed to update employee ID {employee_id}\n{e}")
    return messages

def hex_check(value):
    if re.match (r'^#[A-Fa-f0-9]{6}$'):
        return True
    else:
        return False
