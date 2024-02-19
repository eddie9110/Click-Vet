from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
import os

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
username = "sandbox"
#api_key = "7f1d73232127999fd52e5cc14541b6ceee53b6b3fae2fb1a44952e6e64d13ac3"
#africastalking.initialize(username, api_key)
#sms = africastalking.SMS

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "53b6b3fae2fb1a44952e6e64d13ac3"
db = SQLAlchemy(app)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone_no = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(60), nullable=False, default='password')
    location = db.Column(db.String(30), nullable=False)
    requests = db.relationship('Requests', backref='vet', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.phone_no}', '{self.location}')"


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    month_created = db.Column(db.Integer, default=datetime.now().month)
    location = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(13), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    diagnosis = db.Column(db.Text)
    

    def __repr__(self):
        return f"Request('{self.id}', '{self.date_created}', '{self.location}', '{self.phone_no}', '{self.vet_id}', '{self.diagnosis}')"

@app.route("/")
@app.route("/home")
def home():
    final_results = []
    unsorted_diagnosis = []
    constituencies = ['Nyeri Town', 'Mathira', 'Kieni', 'Othaya', 'Tetu', 'Mukuruwe-ini']
    for i in constituencies:
        results = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month, Requests.location==i)
        for result in results:
            diagnosis_ = result.diagnosis
            unsorted_diagnosis.append(diagnosis_)
        from collections import Counter
        occurence_count = Counter(unsorted_diagnosis)
        most_frequent, the_count = occurence_count.most_common(1)[0]
        final_results.append([i, most_frequent, the_count])
    
    #card1
    per_location_list = []
    constituencies = ['Nyeri Town', 'Mathira', 'Kieni', 'Othaya', 'Tetu', 'Mukuruwe-ini']
    for i in constituencies:
        new_list = []
        requests = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month, Requests.location==i)
        for request_ in requests:
            new_list.append(request_)
        no_of_requests = len(new_list)
        per_location_list.append({"location":i, "number":no_of_requests})
    pre_sum = {d['location']:d['number'] for d in per_location_list}
    values_only = pre_sum.values()
    summed_values = sum(values_only)
    card1 = summed_values

    #card2
    card2 = []
    unsorted_diagnosis = []
    results = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month)
    for result in results:
        diagnosis_ = result.diagnosis
        unsorted_diagnosis.append(diagnosis_)
    from collections import Counter
    occurence_count = Counter(unsorted_diagnosis)
    most_frequent, the_count = occurence_count.most_common(1)[0]
    card2.append([most_frequent, the_count])

    #card3
    pre_resolved_list = []
    constituencies = ['Nyeri Town', 'Mathira', 'Kieni', 'Othaya', 'Tetu', 'Mukuruwe-ini']
    for i in constituencies:
        new_list = []
        requests = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month, Requests.location==i)
        for request_ in requests:
            new_list.append(request_)
        no_of_requests = len(new_list)
        pre_resolved_list.append({"location":i, "number":no_of_requests})
    resolved_list = {d['location']:d['number'] for d in pre_resolved_list}
    card3 = max(resolved_list, key = resolved_list.get)


    return render_template('home.html', data=final_results, card1=card1, card2=card2, card3=card3)

########################################################################
@app.route("/update_info")
def update_info():
    page = request.args.get('page', 1, type=int)
    requests = Requests.query.filter(Requests.diagnosis == None).paginate(page=page, per_page=10)
    return render_template("requestsdata.html", requests=requests)


@app.route("/update_diagnosis/<int:request_id>/", methods=['GET', 'POST'])
def update_diagnosis(request_id):
    from forms import DiagnosisForm
    request_ = Requests.query.get_or_404(request_id)
    
    form = DiagnosisForm()
    if form.validate_on_submit():
        request_.diagnosis = form.diagnosis.data
        db.session.commit()
        flash('Diagnosis updated successfully', 'success')
        return redirect(url_for('update_info'))
    elif request.method == 'GET':
        return render_template('update_diagnosis.html', form=form)
    
@app.route("/delete_request/<int:request_id>/", methods=['POST', 'GET'])
def delete_request(request_id):
    request_ = Requests.query.get_or_404(request_id)
    db.session.delete(request_)
    db.session.commit()
    flash('Request deleted successfully', 'success')
    return redirect(url_for('update_info'))

##################################################################
@app.route("/vets_info")
def vets_info():
    page = request.args.get('page', 1, type=int)
    vets = User.query.paginate(page=page, per_page=10)
    return render_template("vet.html", vets=vets)

@app.route("/create_vet/", methods=['GET', 'POST'])
def create_vet():
    from forms import CreateVetForm
    form = CreateVetForm()
    if form.validate_on_submit():
        vet = User(username=form.name.data, phone_no=form.phone.data, location=form.phone.data)
        db.session.add(vet)
        db.session.commit()
        flash('Vet added successfully', 'success')
        return redirect(url_for('vets_info'))
    elif request.method == 'GET':
        return render_template('addnewvet.html', form=form)

@app.route("/update_vet/<int:vet_id>/", methods=['GET', 'POST'])
def update_vet(vet_id):
    from forms import UpdateVetForm
    vet = User.query.get_or_404(vet_id)
    
    form = UpdateVetForm()
    if form.validate_on_submit():
        vet.location = form.location.data
        vet.phone_no = form.phone.data
        db.session.commit()
        flash('Vet info updated successfully', 'success')
        return redirect(url_for('vets_info'))
    elif request.method == 'GET':
        return render_template('updatevet.html', form=form)

@app.route("/requests")
def requests():
    final_results = []
    unsorted_diagnosis = []
    constituencies = ['Nyeri Town', 'Mathira', 'Kieni', 'Othaya', 'Tetu', 'Mukuruwe-ini']
    for i in constituencies:
        results = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month, Requests.location==i)
        for result in results:
            diagnosis_ = result.diagnosis
            unsorted_diagnosis.append(diagnosis_)
        from collections import Counter
        occurence_count = Counter(unsorted_diagnosis)
        most_frequent, the_count = occurence_count.most_common(1)[0]
        final_results.append([i, most_frequent, the_count])
    return jsonify(final_results)

@app.route("/resolved")
def resolved():
    pre_resolved_list = []
    constituencies = ['Nyeri Town', 'Mathira', 'Kieni', 'Othaya', 'Tetu', 'Mukuruwe-ini']
    for i in constituencies:
        new_list = []
        requests = Requests.query.filter(Requests.diagnosis != None, Requests.month_created==datetime.now().month, Requests.location==i)
        for request_ in requests:
            new_list.append(request_)
        no_of_requests = len(new_list)
        pre_resolved_list.append({"location":i, "number":no_of_requests})
    resolved_list = {d['location']:d['number'] for d in pre_resolved_list}
    val = max(resolved_list, key = resolved_list.get)
    return jsonify(val)
