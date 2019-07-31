from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from utils import fetch_reply


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/news", methods=['POST', 'GET'])
def sms_reply():
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    resp = MessagingResponse()
    msg = resp.message(fetch_reply(msg, sender))

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)