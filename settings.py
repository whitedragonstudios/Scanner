from flask import Flask, render_template, request
from datetime import datetime as dt

from initialization import Setting

setting = Setting()


# Intialize flask server
app = Flask(__name__)

# Set menu route
@app.route ('/menu')

# Render updates from setting to webpage
def open_settings():
    # Get text from input box on webpage
    new_company_name = request.args.get('new_companyname')

    return render_template("menu.html", 
                        company_name=setting.company,
                        cf = setting
                        )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
    #serve(app, host="0.0.0.0", port=2000))