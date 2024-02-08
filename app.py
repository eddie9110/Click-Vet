import os
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
#from ussd1 import app
import africastalking
import os
import random

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

username = "sandbox"
api_key = "Your API key goes here"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    requests = db.relationship('Requests', backref='vet', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    month_created = db.Column(db.DateTime, default=datetime.now().month)
    location = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(13), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    diagnosis = db.Column(db.Text)
    

    def __repr__(self):
        return f"Request('{self.id}', '{self.date_created}', '{self.phone_no}', '{self.diagnosis}')"
    

#routes    
@app.route('/ussd', methods=['POST', 'GET'])
def ussd_callback():
    global response
    global location
    global request1
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    #ussd logic
    if text == "":
        response = "CON Please choose your constituency\n"
        response += "1. Nyeri Town\n"
        response += "2. Mathira\n"
        response += "3. Kieni\n"
        response += "4. Othaya\n"
        response += "5. Tetu\n"
        response += "6. Mukuruwe-ini"
    elif text == "1":
        location = "Nyeri Town"
        vets_details = {'John Kimani':'071234567', 'Angela Achieng':'071234567', 'Njogu Wanderi':'071234567',
        "Njeri Wanjiku":'071234567', 'Priscilla Kanini': '071234567', 'George Wafula':'071234567', 
        'Edwin Mwangi':'071234567', 'Anne Wanjira':'071234567', 'Agnes Mwikali': '071234567',
        'John Kamau':'071234567'}
        #query database for user where location = location . A list will be returned as 'name-phonenumber' it can be split at '-' 
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    elif text == "2":
        location = "Mathira"
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    elif text == "3":
        location = "Kieni"
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    elif text == "4":
        location = "Othaya"
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    elif text == "5":
        location = "Tetu"
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    elif text == "6":
        location = "Mukuruwe-ini"
        request1 = Requests(phone_no=phone_number, location=location)
        db.session.add(request1)
        db.session.commit() 
        response = "END Your assigned vet is:\n"
        name, phone_number = random.choice(list(vets_details.items()))
        response += f'{name}\nphone number: {phone_number}'
    else:
        response = "END Invalid input. Try again."

    return response


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/search") #end point that takes a query string to facilitate search in tables from database
#@login_required
def search():
    q = request.args.get("q")
    print(q)
    global results
    if q:
        results = Requests.query.filter(Requests.id.icontains(q) | Requests.phone_no(q) | Requests.date_created(q)
                                        | Requests.location(q) | Requests.vet_assigned.icontains(q) | Requests.diagnosis(q)) \
        .order_by(Requests.date_created.asc()).order_by(Requests.user_id.asc).limit(20).all()
    else:
        results = []

    return render_template("search_results.html", results=results)



"""
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
"""



"""
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))
"""






"""
@app.route("/register", methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm, LoginForm
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
"""


"""
@app.route("/login", methods=['GET', 'POST'])
def login():
    from forms import RegistrationForm, LoginForm
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            page_link = request.args.get('next')
            return redirect(page_link) if page_link else redirect(url_for('home'))
        else:
            flash('Unsuccessful Login', 'danger')
    return render_template('login.html', title='Login', form=form)
"""



"""
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))