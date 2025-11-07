from flask import Flask, render_template, request, redirect, Blueprint
from datetime import datetime as dt
import json
import os
from classSettings import Setting
from classNews import News_Report
from classQuotes import quote_generator
from classWeather import weather_report
from classHandler import Handler
from classPerson import Person, Default_Person

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

#print(config.news_key)

# Intialize flask server
app = Flask(__name__)

frontend = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')

# Set default and index route
@frontend.route ('/')
def index():
    return redirect('/home')


# Render updates from person to webpage
@frontend.route ('/home', methods=['GET', 'POST'])
def home():
    employee = None
    if request.method == 'POST':
        idscan = request.form.get('idscan')
        employee = Person(idscan)

        # update timesheet here

    # Pass idnumber to person object. Person object returns name, group, time, and image (if availible)
    return render_template("home.html", 
                           scan = employee or Default_Person(),
                           date=dt.now().strftime("%m-%d-%y"),
                            time=dt.now().strftime("%H:%M"),
                           cf = config,
                           quote = quoteOTDay[0],
                           author = quoteOTDay[1],
                           wd = weather_data,
                           news_articles = news.articles
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