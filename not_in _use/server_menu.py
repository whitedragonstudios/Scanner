from flask import Flask, render_template, request
from datetime import datetime as dt
from classSettings import Setting
from databaseConfig import databaseSettings


user = databaseSettings["user"]
password = databaseSettings["password"]
db_name = databaseSettings["db_name"]
port = databaseSettings["port"]
host = databaseSettings["host"]


config = Setting(user, password, db_name, port, host).assign_settings()
#new_company_name = request.args.get('new_companyname')


# Intialize flask server
app = Flask(__name__)

@app.route('/')
def open_settings():
    return render_template("menu.html", cf = config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
    #serve(app, host="0.0.0.0", port=2000))