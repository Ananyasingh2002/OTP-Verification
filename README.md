# OTP Verification Web Application

This is a simple web application built with Flask and Twilio for sending and verifying OTPs (One-Time Passwords). Users can request an OTP, receive it via SMS, and then verify it.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- [Python](https://www.python.org/downloads/)
- Flask
- Twilio
- Flask-Session

You can install these packages using pip:

```bash
pip install Flask twilio Flask-Session
```

## Configuration

Make sure to configure the following variables in the code:

- app.config['SECRET_KEY']: Set a secret key for session management.
  
- ACCOUNT_SID: Your Twilio account SID.
  
- AUTH_TOKEN: Your Twilio authentication token.
  
- TWILIO_PHONE_NUMBER: The Twilio phone number from which OTPs will be sent.

## Usage

- Run the application: `app.py`

- Open your web browser and navigate to http://localhost:5000 to access the application.

- Enter your information (name, prn, email, branch, and phone number) and click the "Get OTP" button.

- An OTP will be sent to the provided phone number via SMS. Enter the OTP in the "Verification Code" field and click "Verify OTP."

- If the OTP is valid and hasn't expired, the user data will be printed to the console. You can customize this part to process or store the user data as needed.

## Routes

- `/`: The main page where users can enter their information and request an OTP.

- `/getOTP`: A POST request to generate and send an OTP via Twilio.

- `/verifyOTP`: A POST request to verify the OTP and display user data.

## Notes

- The OTP is considered valid if it was generated within the last 60 seconds or you can change it according to yourself.

- This code is for educational purposes and may need further customization and security enhancements for production use.




Please remember to keep sensitive information like Twilio credentials and secret keys secure and never expose them in public repositories or publicly visible code.


## License

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
