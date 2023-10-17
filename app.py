from flask import Flask, render_template, request, session, jsonify
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import load_dotenv
from flask_session import Session
import random
import time
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello@123'
app.config['SESSION_TYPE'] = 'filesystem'
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
Session(app)

def generate_otp():
    return ''.join(random.choice('0123456789') for _ in range(6))

def send_otp(twilio_client, phone_number, otp):
    try:
        message = twilio_client.messages.create(
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            body=f'Your OTP is {otp}',
            to=phone_number
        )
        return message
    except TwilioRestException as e:
        return None

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/getOTP', methods=['POST'])
def get_otp():
    if 'phone-number' in request.form:
        phone_number = str(request.form['phone-number'])
        otp = generate_otp()
        message = send_otp(twilio_client, phone_number, otp)
        if message:
            session['otp_code'] = otp
            session['otp_time'] = time.time()

            # Store the user data in the session
            user_data = {}
            for field in ['name', 'prn', 'email', 'branch', 'phone-number']:
                if field in request.form:
                    user_data[field] = request.form.get(field)

            session['user_data'] = user_data
            print(user_data)
            return jsonify({"message_sid": message.sid, "status": "OTP sent"})
        else:
            return jsonify({"error": "Failed to send OTP"})
    return jsonify({"error": "Phone number is required"})

@app.route('/verifyOTP', methods=['POST'])
def verify_otp():

    if 'verification-code' in request.form:
        code = request.form['verification-code']
        if code == session.get('otp_code'):
            # Check if the OTP is still valid (generated within the last 60 seconds)
            otp_time = session.get('otp_time', 0)
            current_time = time.time()
            if current_time - otp_time <= 120:
                #We can collect user data directly from session
                user_details = session.get('user_data')
    
                # Collect user data
                # name = request.form.get('name')
                # prn = request.form.get('prn')
                # email = request.form.get('email')
                # branch = request.form.get('branch')
                # phone_number = request.form.get('phone-number')

                # You can now process or store this user data as needed
                user_data = {
                    'name': user_details['name'],
                    'prn': user_details['prn'],
                    'email': user_details['email'],
                    'branch': user_details['branch'],
                    'phone_number': user_details['phone-number']
                }
                
                # Printing the stored user data
                print("User data:", user_data)
                
                return jsonify({"status": "success"})
            else:
                return jsonify({"error": "OTP has expired"})
        return jsonify({"error": "You entered the wrong code!"})
    return jsonify({"error": "Verification code is required"})

if __name__ == '__main__':
    app.run(debug=True)
