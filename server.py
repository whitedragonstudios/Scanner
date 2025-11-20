from flask import Flask, render_template, request, redirect, Blueprint, flash
import classSettings
from classNews import News_Report
from classQuotes import quote_generator
from classWeather import weather_report
from classHandler import Handler
from classPerson import Person, Default_Person
import services

config = classSettings.Setting()
weather_data = weather_report(config.city, config.weather_key)
news = News_Report(config.country, config.news_key)
quoteOTDay = quote_generator().QotD


def message_parser(messages):
    for k,v in messages.items():
        if len(v) > 0:
            #revmsg = list(reversed(v))
            catagory = k
            for msg in v:
                flash(msg, catagory)
    return messages


# Intialize flask server
app = Flask(__name__)
app.secret_key = "stoic"
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
                print(f"Error: Person failed to find mathcing ID {e}")
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
        user_handle = Handler("user")

        # Danger Zone
        action = request.form.get("action")
        if action:
            msg = services.danger(action, user_handle)
            config = classSettings.Setting()
            message_parser(msg)
        
        # Simple config changes    
        keys = ["company", "city", "weather_key", "news_key"]
        updated = False
        for key in keys:
            try:
                msg = services.single_button(key, user_handle)
                if len(msg['success']) > 0:
                    message_parser(msg)
                    updated = True
                elif len(msg['error']) > 0:
                    message_parser(msg)
            except Exception as e:
                print(f"Failed to update {key}: {e}")
        if updated:
            config = classSettings.Setting()
            news = News_Report(config.country, config.news_key)
            weather_data = weather_report(config.city, config.weather_key)

        # color updates dynamically
        if request.form.get("form_type") == "colors":
            for key, value in request.form.items():
                if hasattr(config, key):
                    try:
                        setattr(config, key, value)
                        user_handle.update_database("config_database", "key", "value", key, value)
                        config = classSettings.Setting()
                        flash(f"{key} updated to {value}", "success")
                    except Exception as e:
                        flash(f"Failed to update {key}: {e}", "error")
        
        # reset colors to default settings
        if "reset_colors" in request.form:
            default = config.default_colors()
            for key,value in default.items():
                try:
                    user_handle.update_database("config_database", "key", "value", key, value)
                    flash(f"{key} reset to {value}", "info")
                except Exception as e:
                    flash(f"Failed to reset {key}: {e}", "error")
            config = classSettings.Setting()
            #user_handle.send_query("SELECT * FROM config_database;")


        # Emails
        if "emails" in request.form:
            report_email = request.form.get("emails").strip().lower().replace("'", "''")
            freq = request.form.get("send-reports").strip().lower().replace("'", "''")
            try:
                user_handle.update_database("email_list", "key", "value", report_email, freq)
                flash(f"Added {report_email} at frequency {freq } to database", "success")
            except Exception as e:
                flash(f"Failed to insert {report_email} into database: {e}", "error")

        # file upload
        if "fileUpload" in request.files:
            file_handle = request.files["fileUpload"]
            msgs = services.upload(file_handle, user_handle)
            message_parser(msgs)

        # manual database entry
        if 'manual-entry-action' in request.form:
            action = request.form.get('manual-entry-action')
            request_dict = request.form.to_dict()
            msg = services.manual_entry(action, request_dict, user_handle)
            message_parser(msg)
    
    return render_template("settings.html", cf=config)




@frontend.route('/reports')
def reports():
    return render_template("reports.html", 
        cf = config, 
        recent_people = recent_list
        )
    
