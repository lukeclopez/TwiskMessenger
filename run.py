from flask import Flask, request, render_template, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
# os.environ.get()
# https://www.twilio.com/console
# TWILIO_ACCOUNT_SID
# TWILIO_AUTH_TOKEN

app = Flask(__name__)

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)


@app.route("/")
def home():
    messages = client.messages.list()
    possible_recips = [
        os.environ.get("LUKE_CELL"),
    ]

    return render_template('home.html', messages=messages, possible_recips=possible_recips)


@app.route("/send", methods=['POST'])
def send():
    tw_num = os.environ.get("TW_NUM")
    to_num = request.form['to']
    msg = request.form['body']

    message = client.messages \
        .create(
            body=msg,
            from_=tw_num,
            to=to_num
        )

    print(message.sid)
    return redirect(url_for("home"))


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    if request.method == 'POST':
        for key, value in request.items():
            print(key, value)
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("howdy")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
