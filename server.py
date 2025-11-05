from flask import Flask, render_template, request, redirect, Blueprint
from datetime import datetime as dt
import json
import os
from classSettings import Setting
import databaseConfig
from quotes import quote_generator
from classweather import weather_report

db = databaseConfig. databaseSettings()
user = db["user"]
password = db["password"]
db_name = db["db_name"]
port = db["port"]
host = db["host"]

quoteOTDay = quote_generator().QotD

# Intialize flask server
app = Flask(__name__)

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')

config = Setting(user, password, db_name, port, host).assign_settings()

weather = weather_report(config['city'], config['weather_key'])

# Set default and index route
@frontend.route ('/')
def index():
    return redirect('/home')
# Render updates from person to webpage
@frontend.route ('/home')
def home():
    # Get text from input box on webpage
    scanned_id = request.args.get('idnumber')
    if scanned_id == None:
        scanned_id = "No ID"
    # Pass idnumber to person object. Person object returns name, group, time, and image (if availible)
    return render_template("home.html", 
                           idnumber=scanned_id,
                           name="Marcus Aurelius",
                           group="Emperor of Rome", 
                           date=dt.now().strftime("%m-%d-%y"),
                           time=dt.now().strftime("%H:%M"),
                           picture = "default.jpg",
                           cf = config,
                           quote = quoteOTDay[0],
                           author = quoteOTDay[1],
                           city = weather.city,
                           state = weather.state,
                           country = weather.country,
                           icon = weather.icon, 
                           description = weather.description, 
                           feel = weather.feel, 
                           tmin = weather.min, 
                           tmax = weather.max, 
                           humid = weather.humid, 
                           clouds = weather.clouds
                           )


@frontend.route('/settings')
def settings():
    return render_template("settings.html", cf = config)


@frontend.route('/reports')
def reports():
    return render_template("reports.html", cf = config)
    
app.register_blueprint(frontend)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
    #serve(app, host="0.0.0.0", port=2000))