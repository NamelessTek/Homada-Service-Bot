from ast import Raise
from twilio.twiml.messaging_response import MessagingResponse
from homada import client
from homada.config import Config
from flask import request


def send_message(phone_number: str, message: str) -> dict:
    '''
    Send message to a phone 
    '''
    if phone_number and message:
        try:
            message = client.messages.create(
                to=phone_number,
                from_=Config.TWILIO_PHONE_NUMBER,
                body=message
            )
        except Exception:
            Raise(Exception('Message could not be sent'))

    else:
        pass


def incoming_message() -> dict:
    '''
    Receive incoming messages
    '''
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)

    response = MessagingResponse()
    response.message('The Robots are coming! Head for the hills!')
    return response
