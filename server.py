from flask import Flask, render_template, request
from datetime import datetime as dt
import json
import os
from classSettings import Setting

user = "marcus"
password = "stoic"
db_name = "scanner"
port = 5000
host = "localhost"


# Intialize flask server
app = Flask(__name__)

config = Setting(user, password, db_name, port, host).assign_settings()
# Set default and index route
@app.route ('/')
#@app.route('/index')
# Render updates from person to webpage
def update_webpage():
    # Get text from input box on webpage
    scanned_id = request.args.get('idnumber')
    if scanned_id == None:
        scanned_id = "No ID"
    # Pass idnumber to person object. Person object returns name, group, time, and image (if availible)
    return render_template("index.html", 
                           idnumber=scanned_id,
                           name="Marcus Aurelius",
                           group="Emperor of Rome", 
                           date=dt.now().strftime("%m-%d-%y"),
                           time=dt.now().strftime("%H:%M"),
                           picture = "default.jpg",
                           cf = config
                           )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
    #serve(app, host="0.0.0.0", port=2000))