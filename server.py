from flask import Flask, render_template, request, redirect, Blueprint, flash, url_for
from datetime import datetime as dt
import json
import os
from classSettings import Setting
from classNews import News_Report
from classQuotes import quote_generator
from classWeather import weather_report
from classHandler import Handler
from classPerson import Person, Default_Person
from classInstall import Postgre_Install
import pandas as pd

import databaseConfig
db = databaseConfig. databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]


config = Setting(user, password, db_name, port, host)
weather_data = weather_report(config.city, config.weather_key)
news = News_Report(config.country, config.news_key)
quoteOTDay = quote_generator().QotD


# Intialize flask server
app = Flask(__name__)
app.secret_key = password
frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')
recent_list = []


# Set default and index route
@frontend.route ('/')
def index():
    return redirect('/home')


# Render updates from person to webpage
@frontend.route ('/home', methods=['GET', 'POST'])
def home():
    global recent_list
    employee = None
    idscan = None
    if request.method == 'POST':
        idscan = request.form.get('idscan')
        if not idscan:
            employee = Default_Person(recent_list, idscan)
        else:
            try:
                employee = Person(idscan, recent_list)
            except Exception as e:
                print(f"Error: home Person failed to find mathcing ID {e}")
                employee = Default_Person(recent_list, idscan)
        recent_list = employee.recent

    # Pass idnumber to person object. Person object returns name, group, time, and image (if availible)
    return render_template("home.html", 
                           recent_people = recent_list,
                           scan = employee or Default_Person(recent_list, idscan),
                           cf = config,
                           quote = quoteOTDay[0],
                           author = quoteOTDay[1],
                           wd = weather_data,
                           news_articles = news.articles
                           )


@frontend.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "POST":
        global config, weather_data, news
        admin = Handler(password=password)
        user_handle = Handler(user, password, db_name)
        #user_handle.send_query("SELECT current_database(), current_schema();")
        # Danger Zone
        action = request.form.get("action")
        if action:
            uninstall = Postgre_Install("postgres", password, db_name, port, host)
            if action == "restore":
                config_list = {
                    'config_status': 'True',
                    'config_date': dt.now().strftime("%m-%d-%y"),
                    'CSV_path': None,
                    'XLSX_path': None,
                    'JSON_path': None,
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
                    user_handle.update_config(key,value)
                user_handle.send_query("SELECT * FROM config_database;")
                msg = "Configuration restored to defaults"

            elif action == "clear":
                print("emails cleared")
                user_handle.send_command("DELETE FROM email_list;")
                user_handle.send_query("SELECT * FROM email_list;")
                msg = "Email list cleared"
            elif action == "delete_people":
                print("db reset")
                user_handle.send_command("DELETE FROM people_database;")
                user_handle.send_query("SELECT * FROM people_database;")
                msg = "Employee database deleted"
            elif action == "delete_timesheets":
                print("db reset")
                user_handle.send_command("DELETE FROM timesheet_database;")
                user_handle.send_query("SELECT * FROM timesheet_database;")
                msg = "Timesheet database deleted"
            elif action == "clean":
                uninstall.drop_tables('people_database')
                uninstall.drop_tables('timesheet_database')
                uninstall.drop_tables('config_database')
                uninstall.drop_database(db_name)
                uninstall.drop_user(user)                                    
                msg = "System reinstalled from clean state"
            flash(msg, "warning")
            return redirect(url_for("frontend.settings"))

        # Configuration changes
        if "companyname" in request.form:
            new_company = request.form.get("companyname")
            user_handle.update_config("company", new_company)
            msg = f"Company name updated to {new_company}"
            return redirect(url_for("frontend.settings"))
        
        if "cityname" in request.form:
            new_city = request.form.get("cityname")
            user_handle.update_config("city", new_city)
            msg = f"Company name updated to {new_city}"
            return redirect(url_for("frontend.settings"))
            

        # API keys
        if  "wkey" in request.form and request.form.get("wkey"):
            new_key = request.form.get("wkey")
            user_handle.update_config("weather_key", new_key)
            msg = "Weather key updated"
        if "nkey" in request.form and request.form.get("nkey"):
            new_key = request.form.get("nkey")
            user_handle.update_config("news_key", new_key)
            msg = "News key updated"


        if "reset_colors" in request.form:
            colors = {'main_background_color':'#0a0a1f',
                    'main_text_color':'#f0f0f0',
                    'content_color': '#1c1c33',
                    'content_text_color': '#ffffff',
                    'sidebar_color':'#193763',
                    'sidebar_text_color':'#ffffff',
                    'button_color':'#1a73ff',
                    'button_text_color':'#ffffff',
                    'button_hover_color':'#0050b3',
                    'border_color':'#3399ff'}
            for key,value in colors.items():
                user_handle.update_config(key,value)
            user_handle.send_query("SELECT * FROM config_database;")
            flash("Colors restored to defaults", "sucess")

        # Emails
        if "emails" in request.form:
            report_email = request.form.get("emails").strip().lower().replace("'", "''")
            freq = request.form.get("send-reports").strip().lower().replace("'", "''")
            try:
                user_handle.send_command(f"INSERT INTO email_list (email, frequency) VALUES ('{report_email}', '{freq}');")
                user_handle.send_query(f"SELECT (email, frequency) FROM email_list WHERE email = '{report_email}';")
                flash(f"Sucessfully added {report_email} at frequency {freq }into database", "success")
            except Exception as e:
                flash(f"Failed to insert {report_email} into database: {e}", "error")
            return redirect(url_for("frontend.settings"))


        # color updates dynamically
        if request.form.get("form_type") == "colors":
                for key, value in request.form.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
                        user_handle.update_config(key, value)
                        flash(f"{key} updated", "success")
                return redirect(url_for("frontend.settings"))

        # file upload
        if "fileUpload" in request.files:
            file = request.files["fileUpload"]
            if file and file.filename:
                filename = file.filename
                allowed_extensions = {'.csv', '.xlsx', '.json'}
                ext = os.path.splitext(filename)[1].lower()
                if ext not in allowed_extensions:
                    flash("Unsupported file type. Please upload a CSV, XLSX, or JSON file.", "warning")
                    return redirect(url_for("frontend.settings"))
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
                        user_handle.send_command(f"""
                        INSERT INTO people_database (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department) VALUES (
                        {int(row['employee_id'])}, '{row['first_name']}', '{row['last_name']}', '{row['email']}', '{row['phone']}', '{row['pic_path']}', '{row['employee_role']}', '{row['position']}', '{row['department']}');""")

                    flash(f"File {filename} uploaded and data imported successfully.", "success")
                except Exception as e:
                    flash(f"Failed to import data: {e}", "error")

                return redirect(url_for("frontend.settings"))


        # manual database entry
        if 'manual-entry-action' in request.form:
            action = request.form.get('manual-entry-action')
            try:
                employee_id = int(request.form.get('idnumber'))
                first_name = request.form.get('fname').strip().title()
                last_name = request.form.get('lname').strip().title()
                email = request.form.get('email').strip().lower()
                phone = request.form.get('pnumber').strip()
                pic_path = request.form.get('filename').strip()
                employee_role = request.form.get('role').strip().title()
                position = request.form.get('position').strip().title()
                department = request.form.get('department').strip().title()
            except Exception as e:
                flash(f"Error parsing form input: {e}", "error")
                return redirect(url_for("frontend.settings"))

            if action == "add":
                try:
                    user_handle.send_command(f"""
                        INSERT INTO people_database 
                        (employee_id, first_name, last_name, email, phone, pic_path, employee_role, position, department)
                        VALUES
                        ({employee_id}, '{first_name}', '{last_name}', '{email}', '{phone}', '{pic_path}', '{employee_role}', '{position}', '{department}')
                        ON CONFLICT (employee_id) DO NOTHING;
                    """)
                    flash(f"Added {first_name} {last_name} to the database", "success")
                except Exception as e:
                    flash(f"Failed to add entry: {e}", "error")

            elif action == "update":
                try:
                    fields = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "pic_path": pic_path,
                        "employee_role": employee_role,
                        "position": position,
                        "department": department
                    }
                    def is_skip(v):
                        if v is None:
                            return True
                        s = str(v).strip().lower()
                        return s in {"", " ", "none", "none@none.com"}

                    update_fields = {k: v for k, v in fields.items() if not is_skip(v)}

                    if update_fields:
                        kv_parts = []
                        for k, v in update_fields.items():
                            safe_v = str(v).replace("'", "''")
                            kv_parts.append(f"{k} = '{safe_v}'")
                        key_values = ", ".join(kv_parts)

                        user_handle.send_command(
                            f"UPDATE people_database SET {key_values} WHERE employee_id = {int(employee_id)};"
                        )
                        flash(f"Updated employee ID {employee_id} in the database {key_values}", "success")
                    else:
                        flash("No valid fields to update", "warning")
                except Exception as e:
                    flash(f"Update failed: {e}", "error")

                except Exception as e:
                    flash(f"Failed to update entry: {e}", "error")

            elif action == "remove":
                try:
                    user_handle.send_command(f"""
                        DELETE FROM people_database
                        WHERE employee_id = {employee_id};
                    """)
                    flash(f"Removed employee ID {employee_id} from the database", "success")
                except Exception as e:
                    flash(f"Failed to remove entry: {e}", "error")
            else:
                flash("Invalid action selected", "warning")

            return redirect(url_for("frontend.settings"))
        
        
    
    config = Setting(user, password, db_name, port, host)
    news = News_Report(config.country, config.news_key)
    weather_data = weather_report(config.city, config.weather_key)
    
    return render_template("settings.html", cf=config)

@frontend.route('/reports')
def reports():
    return render_template("reports.html", 
        cf = config, 
        recent_people = recent_list
        )
    
app.register_blueprint(frontend)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
    #serve(app, host="0.0.0.0", port=2000))