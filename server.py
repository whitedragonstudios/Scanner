from flask import Flask, render_template, request
from datetime import datetime as dt

# Intialize flask server
app = Flask(__name__)

# Set default and index route
@app.route ('/')
@app.route('/index')
# Render updates from person to webpage
def update_webpage():
    # Get text from input box on webpage
    scanned_id = request.args.get('idnumber')
    # Pass idnumber to person object. Person object returns name, group, time, and image (if availible)
    return render_template("index.html", 
                           name="Bob",
                           group="First shift", 
                           date=dt.now().strftime("%m-%d-%y"),
                           time=dt.now().strftime("%H:%M"),
                           picture = "default.jpg"
                           )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
    #serve(app, host="0.0.0.0", port=2000))