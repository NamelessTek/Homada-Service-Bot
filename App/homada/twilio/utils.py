from homada.models import Ubicacion, Client, Booking, Questions, Admin
from homada.reservaciones.utils import save_reservation
from homada import db
from twilio.twiml.messaging_response import MessagingResponse
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


def conversations_client(phone_number: str, incoming_message: str) -> list:
    '''
    Conversations with the user
    '''
    messages = []
    client = Client.query.filter_by(phone=phone_number).first()
    booking = Booking.query.filter_by(cliente_id=client.id).first()
    ubicacion = Ubicacion.query.filter_by(
        id=booking.ubicacion_id).first() if booking else None

    if incoming_message:
        match incoming_message:
            case 'hola':
                messages = [
                    f'¡Hola {client.name}! Hola bienvenido a Homada, muchas gracias por tu preferencia']
                if booking:
                    messages.extend(
                        [f'{client.name}, para tu entradad el día {booking.arrival.strftime("%d/%m/%Y")}, queremos compartirte algunos datos. La hora de entrada es a las {booking.arrival_time.strftime("%H:%M")}. Sabemos que puedes necesitar conexión a internet, la red es {ubicacion["ssid"]} y el password es {ubicacion["clave"]}.',
                         f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion["url"]}.',
                         'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
                else:
                    messages.append(
                        f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
            case 'adios':
                messages.append(
                    f'¡Adios {client.name}! Esperamos verte pronto 😃')
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')
    else:
        pass

    return messages


def conversations_homada(incoming_message: str) -> list:
    '''
    Conversations with the homada user
    '''
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


def delete_session() -> None:
    if 'question_id' in session:
        del session['question_id']

    if 'revision' in session:
        del session['revision']
    del session['nombre_cliente']
    del session['telefono_cliente']
    del session['email_cliente']
    del session['num_reservacion_cliente']
    del session['dia_llegada_cliente']
    del session['dia_salida_cliente']
    del session['ubicacion_cliente']
    del session['hr_llegada_cliente']
    del session['hr_salida_cliente']


def redirect_to_first_question() -> str:
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question


def welcome_user() -> str:
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


def review_user() -> str:
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


def goodbye_twiml() -> str:
    delete_session()
    return f"Ya quedo creada la reservación {session['num_reservacion_cliente']} :)"


def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    resp = MessagingResponse()
    admin = Admin.query.filter_by(phone=phone_number).first()
    if not admin:
        # Client conversation
        if validate_phone_number(phone_number) and incoming_message:
            for message in conversations_client(phone_number, incoming_message):
                resp.message(message)
        else:
            resp.message(
                'Lo sentimos, no pudimos validar tu numero de telefono 😟')
    else:
        if 'question_id' not in session and 'revision' not in session:
            if 'revision' not in session:
                resp.message(welcome_user())
            else:
                resp.message(goodbye_twiml())
        for message in conversations_homada(incoming_message):
            resp.message(message)

    return str(resp)


def send_question(phone_number: str, question_id: int) -> list:
    '''
    Send survey message
    '''
    messages = []
    if phone_number:
        question = Questions.query.filter_by(id=question_id).first()
        messages.append(question.question)
    else:
        pass

    return messages
