from flask import Flask, render_template, request, session
from flask_mail import Mail
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

with open('config.json', 'r') as c:
    params = json.load(c)['params']

local_server = True
app = Flask(__name__)
app.secret_key = 'super_secret_key'

app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

mail = Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    '''
    sno, name, email, phone_num, msg, date
    '''
    sno = db.Column(db.Integer, unique=True, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(20), nullable = False)
    phone_num = db.Column(db.String(12), nullable = False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable = False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/cpp")
def cpp():
    return render_template("cpp.html")

@app.route("/python")
def python():
    return render_template("python.html")

@app.route("/js")
def js():
    return render_template("js.html")

@app.route("/web")
def web():
    return render_template("web.html")
    
@app.route("/android")
def android():
    return render_template("android.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if (request.method=="POST"):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name = name, email = email, phone_num = phone, msg = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message("New message from Codehunter by " + name,
        sender = email, recipients = [params['gmail-user']], body = message + "\n My phone no. is " + phone + f"and email is {email}")
    return render_template('index.html')

app.run(debug=True)