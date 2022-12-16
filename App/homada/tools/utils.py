from homada.models import *
from flask import session
import phonenumbers
import re
import datetime
import psutil


def delete_session_completly() -> None:
    '''
    Delete the keys in the session dictionary
    '''
    for key in list(session.keys()):
        del session[key]


def delete_session() -> None:
    '''
    Delete the keys in the session dictionary: 
    ['document', 'question_id', 'revision', 'nombre_cliente', 
    'telefono_cliente', 'email_cliente', 'num_reservacion_cliente', 
    'dia_llegada_cliente', 'dia_salida_cliente', 'ubicacion_cliente', 
    'hr_llegada_cliente', 'hr_salida_cliente']
    '''
    for key in ['document', 'question_id', 'revision', 'nombre_cliente', 'telefono_cliente', 'email_cliente', 'num_reservacion_cliente', 'dia_llegada_cliente', 'dia_salida_cliente', 'ubicacion_cliente', 'hr_llegada_cliente', 'hr_salida_cliente', 'review_client_email', 'review_upload', 'content', 'content-type']:
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


def similar_ubicacion() -> str:
    '''
    Return a list of similar ubicaciones
    '''
    similar_ubicaciones = Ubicacion.query.filter(Ubicacion.ubicacion.op(
        'REGEXP')(f'{session["ubicacion_cliente"]}')).limit(5)
    if similar_ubicaciones.count() == 0:
        return 'No hay ubicaciones similares, por favor intenta de nuevo.'
    else:
        return f'Quizás quisiste decir:{chr(10)*2}{chr(10).join([f"{(index+1)}. {similar_ubicacion.ubicacion}" for index, similar_ubicacion in enumerate(similar_ubicaciones)])}'


def font_weight(style: str, text: str) -> None:
    '''
    Return the text with:
    style: 
    - bold
    - italic
    - underline
    '''
    match style:
        case "bold":
            return f"*{text}*"
        case "italic":
            return f"_{text}_"
        case "code":
            return f"`{text}`"
        case "pre":
            return f"```{text}```"
        case _:
            raise ValueError(f"Unknown style: {style}")


def no_reservation_found(resp) -> str:
    '''No reservation found message'''
    resp.message('¡Hola! 😀')
    resp.message('''Gracias por tu preferencia.
    
No podemos encontrar una reservación a tu nombre. 😯
    
Por favor compártenos tu número de confirmación.''')


def goodbye_client(resp) -> None:
    '''
    Sends a goodbye message to the client
    '''
    resp.message(f'¡Adiós! Esperamos verte pronto 😃')


def server_status() -> str:
    '''
    Check if the server is up and running
    OK: memory usage < 80% and cpu usage < 80%
    SLOW: memory usage < 80% and cpu usage > 80%
    CRITICAL: memory usage > 80% and cpu usage > 80%
    '''
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    status = ""
    if memory.percent < 80 and cpu < 80:
        status = "OK"
    elif memory.percent < 80 and cpu > 80:
        status = "SLOW"
    else:
        status = "CRITICAL"
    return status
