from homada.models import *
from flask import session
import phonenumbers
import re
import datetime


def delete_session_completly() -> None:
    '''
    Delete the keys in the session dictionary
    '''
    for key in list(session.keys()):
        del session[key]


def delete_session() -> None:
    '''
    Delete the keys in the session dictionary
    '''
    for key in ['question_id', 'revision', 'nombre_cliente', 'telefono_cliente', 'email_cliente', 'num_reservacion_cliente', 'dia_llegada_cliente', 'dia_salida_cliente', 'ubicacion_cliente', 'hr_llegada_cliente', 'hr_salida_cliente']:
        if key in session:
            del session[key]


def validate_phone_number(phone_number: str) -> bool:
    '''
    Validate phone number
    '''
    try:
        phone = phonenumbers.parse(phone_number.strip(), None)
        client = Client.query.filter_by(phone=phone_number).first()
        return phonenumbers.is_valid_number(phone) and client is not None
    except Exception:
        return False


def validate_email(email: str) -> bool:
    '''
    Validate email
    '''
    try:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    except Exception:
        return False


def validate_reservation_number(reservation_number: str) -> bool:
    '''
    Validate reservation number
    '''
    try:
        reservation = Booking.query.filter_by(
            booking_number=reservation_number).first()
        session['reservación'] = reservation.booking_number
        session['menú'] = 3
        return True
    except Exception:
        return False


def validate_date(date: str) -> bool:
    '''
    Validate that the date is in the correct format dd-mm-yyyy and that it is not a past date
    '''
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y')
        return date >= datetime.datetime.now() - datetime.timedelta(days=1)
    except Exception:
        return False


# def validate_location(location: str) -> bool:
#     '''
#     Validate location
#     '''
#     # use regex to validate if incoming message is a location in DB, else show answers that are similar to the incoming message
#     try:
#         location = Ubicacion.query.filter_by(
#             name=location.strip().lower()).first()
#         re.match(r"[^@]+@[^@]+\.[^@]+", location)
#         return location is not None
#     except Exception:
#         return False
