from app import request, app, User, Requests, db
import africastalking
import os
import random

username = "sandbox"
api_key = "you API key goes here"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    global location
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
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    elif text == "2":
        location = "Mathira"
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    elif text == "3":
        location = "Kieni"
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    elif text == "4":
        location = "Othaya"
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    elif text == "5":
        location = "Tetu"
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    elif text == "6":
        location = "Mukuruwe-ini"
        vet_id = []
        users = User.query.filter_by(location=location)
        for user in users:
            vet_id.append(user.id)
        chosen_id = random.choice(vet_id)
        user = User.query.filter_by(id=chosen_id).first()
        vet_name = user.username
        vet_phone_number = user.phone_no 
        request_ = Requests(phone_no=phone_number, location=location, vet_id=user.id)
        db.session.add(request_)
        db.session.commit()
        response = "END Your assigned vet is:\n"
        response += f'{vet_name}\nphone number: {vet_phone_number}'
    else:
        response = "END Invalid input. Try again."

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
