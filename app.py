import json
import smtplib
from flask import Flask, current_app as app
from email.message import EmailMessage
from email.utils import formataddr

app = Flask(__name__)

# Load SMTP config from config.json
with open("config.json") as config_file:
    full_config = json.load(config_file)
    app.config["SMTP_CONFIG"] = full_config["SMTP_CONFIG"]


def send_email_smtp(to_email, subject, body) -> None:
    app_config = app.config["SMTP_CONFIG"]
    print(app_config)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((app_config["SMTP_MAIL_FROM_NAME"], app_config["SMTP_MAIL_FROM"]))
    msg["To"] = to_email

    msg.set_content(body)

    smtp_client = smtplib.SMTP_SSL if app_config["SMTP_SSL"] else smtplib.SMTP

    with smtp_client(app_config["SMTP_HOST"], app_config["SMTP_PORT"]) as smtp:
        if app_config["SMTP_STARTTLS"]:
            smtp.starttls()
        if app_config["SMTP_USER"] and app_config["SMTP_PASSWORD"]:
            smtp.login(app_config["SMTP_USER"], app_config["SMTP_PASSWORD"])
        smtp.send_message(msg)

@app.route('/')
def index():
    return 'Go to /send-email to send a test email.'

@app.route('/send-email')
def send_email_route():
    send_email_smtp(
        subject='Hello from Flask with smtplib',
        body='This is a test email sent from a Flask app using smtplib.',
        to_email='recipient@example.com'
    )
    return 'Email sent!'

if __name__ == '__main__':
    app.run(debug=True)
