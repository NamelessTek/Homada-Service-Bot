from homada.models import Ubicacion, Client, Booking, Questions
from homada import db
from homada.ubicacion.utils import get_ubicacion
from homada.admin.utils import *
from homada.clientes.utils import get_client
from homada.reservaciones.utils import get_booking
from twilio.twiml.messaging_response import MessagingResponse
from homada import client as twilio_client
from flask import Flask, request, url_for, session, redirect
import phonenumbers
import datetime

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

def validate_reservation_number(reservation_number: str,resp) -> bool:
    '''
    Validate reservation number
    '''
    try:
        reservation = Booking.query.filter_by(booking_number=reservation_number).first()
        session['reservacion']=reservation.booking_number
        session['menu']=3
        return True
    except Exception:
        return False

def conversations_client(phone_number: str, incoming_message: str) -> list:
    '''
    Conversations with the user
    '''
    messages = []
    client = Client.query.filter_by(phone=phone_number).first()
    if not client:
        booking = get_booking(
            Booking.query.filter_by(booking_number=session['reservacion']).first())
    else:
        booking = get_booking(
            Booking.query.filter_by(cliente_id=client.id).first())
    ubicacion = get_ubicacion(
        Ubicacion.query.filter_by(id=booking['Ubicacion_id']).first())
    if incoming_message:
        match incoming_message:
            case "1":
                for message in flow_ubicacion(messages,client,booking,ubicacion):
                    messages.append(message)
            case "3":
                for message in flow_red(messages,client,booking,ubicacion):
                    messages.append(message)
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')

    else:
        pass

    return messages

def flow_red(messages,client,booking,ubicacion):
    
    if client:
        messages = [f'¡Hola {client.name}! Hola bienvenido a Homada, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Sabemos que puedes necesitar conexión a internet, la red es {ubicacion["Ssid"]} y el password es {ubicacion["Clave"]}.',
                'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
                
            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    else:
        messages = [f'¡Hola! Hola bienvenido a Homada, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Sabemos que puedes necesitar conexión a internet, la red es {ubicacion["Ssid"]} y el password es {ubicacion["Clave"]}.',
                'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
                
            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    return messages

def flow_ubicacion(messages,client,booking,ubicacion):
    if client:
        messages = [f'¡Hola {client.name}!, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'{client.name}, para tu entrada el día {booking["Arrival"].strftime("%d/%m/%Y")}, queremos compartirte algunos datos. ',
                f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion["Url"]}.',
                'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    else:
        messages = [f'¡Hola!, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Para tu entrada el día {booking["Arrival"].strftime("%d/%m/%Y")}, queremos compartirte algunos datos. ',
                f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion["Url"]}.',
                'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    return messages

def conversations_homada(incoming_message: str) -> list:
    '''
    Conversations with the homada user
    '''
    response = MessagingResponse()
    messages = []

    if incoming_message:
        if 'question_id' in session:
            question_id = session['question_id']

            print(question_id, flush=True)
            # Answer saved
            match question_id:
                case 1:
                    session['nombre_cliente'] = incoming_message
                    print("Nombre del cliente " +
                          str(session['nombre_cliente']), flush=True)

                case 2:
                    if incoming_message != Client.query.filter_by(phone=incoming_message).first():
                        print(Client.query.filter_by(
                            phone=incoming_message).first(), flush=True)
                        session['telefono_cliente'] = incoming_message
                        print("Telefono del cliente " +
                              str(session['telefono_cliente']), flush=True)
                    else:
                        messages.append(
                            f'El número de teléfono ya existe, por favor ingresa otro')
                        question_id = 2
                case 3:
                    session['email_cliente'] = incoming_message
                    print("Email del cliente " +
                          str(session['email_cliente']), flush=True)
                case 4:
                    session['num_reservacion_cliente'] = incoming_message
                    print("Num Reservacion del cliente " +
                          str(session['num_reservacion_cliente']), flush=True)
                case 5:
                    session['dia_llegada_cliente'] = incoming_message
                    print("Dia Llegada del cliente " +
                          str(session['dia_llegada_cliente']), flush=True)
                case 6:
                    session['dia_salida_cliente'] = incoming_message
                    print("Dia Salida del cliente " +
                          str(session['dia_salida_cliente']), flush=True)
                case 7:
                    session['ubicacion_cliente'] = incoming_message
                    ubicacion_query = Ubicacion.query.filter_by(
                        ubicacion=session['ubicacion_cliente']).first()
                    session['hr_llegada_cliente'] = ubicacion_query.arrival_time
                    session['hr_salida_cliente'] = ubicacion_query.departure_time
                    print("Ubicacion del cliente " +
                          str(session['ubicacion_cliente']), flush=True)
                case _:
                    pass

            next_id_question = int(session['question_id'])+1
            print("Siguiente pregunta", flush=True)
            next_question = Questions.query.filter_by(
                id=next_id_question).first()
            if next_question:
                print("Pregunta siguiente " +
                      next_question.question, flush=True)
                session['question_id'] = next_question.id
                messages.append(next_question.question)
            else:
                session['revision'] = 1
                if 'question_id' in session:
                    del session['question_id']
                review_message = review_user()
                messages.append(review_message)

        elif 'revision' in session:
            print("En revision", flush=True)
            print(incoming_message, flush=True)
            if incoming_message == "si":
                save_reservation()
                messages.append(goodbye_twiml())
            else:
                # Mensaje de que se repetira el ciclo?
                messages.append(goodbye_twiml())
        else:
            print("Primera pregunta", flush=True)
            pregunta = redirect_to_first_question()
            print("Pregunta " + pregunta, flush=True)
            messages.append(pregunta)
    else:
        pass

    return messages

def delete_session_completly():
    if 'question_id' in session:
        del session['question_id']
    if 'revision' in session:
        del session['revision']
    if 'nombre_cliente' in session:
        del session['nombre_cliente']
    if 'telefono_cliente' in session:
        del session['telefono_cliente']
    if 'email_cliente' in session:
        del session['email_cliente']
    if 'num_reservacion_cliente' in session:
        del session['num_reservacion_cliente']
    if 'dia_llegada_cliente' in session:
        del session['dia_llegada_cliente']
    if 'dia_salida_cliente' in session:
        del session['dia_salida_cliente']
    if 'ubicacion_cliente' in session:
        del session['ubicacion_cliente']
    if 'hr_llegada_cliente' in session:
        del session['hr_llegada_cliente']
    if 'hr_salida_cliente' in session:
        del session['hr_salida_cliente']
    if 'menu' in session:
        del session['menu']
    if 'reservacion' in session:
        del session['reservacion']

def delete_session():
    if 'question_id' in session:
        del session['question_id']
    if 'revision' in session:
        del session['revision']
    if 'nombre_cliente' in session:
        del session['nombre_cliente']
    if 'telefono_cliente' in session:
        del session['telefono_cliente']
    if 'email_cliente' in session:
        del session['email_cliente']
    if 'num_reservacion_cliente' in session:
        del session['num_reservacion_cliente']
    if 'dia_llegada_cliente' in session:
        del session['dia_llegada_cliente']
    if 'dia_salida_cliente' in session:
        del session['dia_salida_cliente']
    if 'ubicacion_cliente' in session:
        del session['ubicacion_cliente']
    if 'hr_llegada_cliente' in session:
        del session['hr_llegada_cliente']
    if 'hr_salida_cliente' in session:
        del session['hr_salida_cliente']

def save_reservation():

    name = session['nombre_cliente']
    phone = session['telefono_cliente']
    email = session['email_cliente']

    client = Client(name=name, phone=phone, email=email)
    db.session.add(client)
    db.session.commit()

    client = Client.query.filter_by(email=email).first()
    num_reservacion_cliente = session['num_reservacion_cliente']
    dia_llegada_cliente = datetime.datetime.strptime(
        session['dia_llegada_cliente'], '%d-%m-%Y')
    dia_salida_cliente = datetime.datetime.strptime(
        session['dia_salida_cliente'], '%d-%m-%Y')
    ubicacion_cliente = session['ubicacion_cliente']

    ubicacion = Ubicacion.query.filter_by(ubicacion=ubicacion_cliente).first()
    arrival_time = ubicacion.arrival_time
    departure_time = ubicacion.departure_time

    booking = Booking(booking_number=num_reservacion_cliente, arrival=dia_llegada_cliente, departure=dia_salida_cliente, client=client, ubicacion=ubicacion, status=1,
                      arrival_time=arrival_time, departure_time=departure_time)

    db.session.add(booking)
    db.session.commit()

def redirect_to_first_question():
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question

def welcome_user(send_function):
    welcome_text = """Para la creación de una reservación es necesario crear el cliente con los siguientes datos:
                    - Nombre 
                    - teléfono
                    - Email
                    - número de reservación
                    - día de llegada
                    - hora de llegada
                    - día de partida
                    - hora de partida
                    - ubicación
                    """
    return welcome_text

def review_user():
    review_text = f'''Puedes confirmar los siguientes datos:
                    - Nombre {session['nombre_cliente']}
                    - teléfono {session['telefono_cliente']}
                    - Email {session['email_cliente']}
                    - número de reservación {session['num_reservacion_cliente']}
                    - día de llegada {session['dia_llegada_cliente']}
                    - hora de llegada {session['hr_llegada_cliente']}
                    - día de partida {session['dia_salida_cliente']}
                    - hora de partida {session['hr_salida_cliente']}
                    - ubicación {session['ubicacion_cliente']}

                    Contesta con un si o un no
                    '''
    return review_text

def goodbye_twiml():
    mensaje = "Ya quedo creada la reservación " + \
        session['num_reservacion_cliente'] + " :)"
    delete_session()
    return mensaje

def welcome_homada(resp):
    resp.message("""Hola, bienvenido a Homada
                    Para la creación de una reservación es necesario crear el cliente con los siguientes datos:
                    - Nombre
                    - teléfono
                    - Email
                    - número de reservación
                    - día de llegada
                    - hora de llegada
                    - día de partida
                    - hora de partida
                    - ubicación
                    """)

def welcome_client(resp):
    resp.message("""¿Qué deseas hacer? 💫
                    1. Obtener Ubicación 📍
                    2. Facturación 💳
                    3. Clave WIFI 🔐
                    """)

def goodbye_client(resp):
        resp.message(f'¡Adios! Esperamos verte pronto 😃')

def client_flow(incoming_message,resp,phone_number):
    if incoming_message == "menu" or "menu" in session:
        if validate_phone_number(phone_number) or validate_reservation_number(incoming_message,resp) or "reservacion" in session:
            if incoming_message == "menu" or session['menu']==3:
                welcome_client(resp)
                session['menu']=0
            elif "menu" in session and session['menu']==1:
                for message in conversations_client(phone_number, incoming_message):
                    resp.message(message)
            if "menu" not in session or session['menu']==0:
                session['menu']=1
        else:
            session['menu']=0    
            no_reservation_found(resp)

def no_reservation_found(resp):
    resp.message('Lo sentimos, no pudimos encontrar una reservación a tu nombre 😟')
    resp.message('Por favor compartenos tu número de reservación.')

def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    resp = MessagingResponse()
    admin = get_admin_phones()
    if phone_number not in admin:
        # Client conversation
        client_flow(incoming_message,resp,phone_number)
    elif phone_number in admin:
        if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias" :
            delete_session_completly()
            goodbye_client(resp)
        elif incoming_message == "menu" or "menu" in session:
            client_flow(incoming_message,resp,phone_number)
        else:
            if 'question_id' not in session and 'revision' not in session:
                if 'revision' not in session:
                    welcome_homada(resp)       
            for message in conversations_homada(incoming_message):
                resp.message(message)
    else:
        no_reservation_found(resp)
        session['reservacion']=1
    return str(resp)