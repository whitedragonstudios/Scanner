from flask import Flask, render_template, request
from datetime import datetime as dt
import json
import os


# Load a config file which allows users to easily change settings NOTE this may be changed to postgre DB in the future. 
def load_config():
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')
    try:
        with open(config_path,"r") as config_file:
            config = json.load(config_file)
            print("Config file loaded.")
    except FileNotFoundError:
        config = {"placeholder_key": "placeholder_value"}
        print("Config file not found. Using default settings.") 
    return config


# Intialize flask server
app = Flask(__name__)

config = load_config()
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