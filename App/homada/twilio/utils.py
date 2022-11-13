from homada.config import Config
from twilio.rest import Client as TwilioClient
from homada.models import Ubicacion, Client, Booking, Questions, Admin
from homada.reservaciones.utils import save_reservation, delete_reservation
from homada.documents.utils import upload_document
from twilio.twiml.messaging_response import MessagingResponse
from flask import session, request
import phonenumbers
import datetime
import re
import requests
import os


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
        session['reservacion'] = reservation.booking_number
        session['menu'] = 3
        return True
    except Exception:
        return False


def validate_date(date: str) -> bool:
    '''
    Validate that the date is in the correct format dd-mm-yyyy and that it is not a past date
    '''
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y')
        return date >= datetime.datetime.now()
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
    if not client:
        booking = Booking.query.filter_by(
            booking_number=session['reservacion']).first()
    else:
        booking = Booking.query.filter_by(cliente_id=client.id).first()
        ubicacion = Ubicacion.query.filter_by(
            id=booking.ubicacion_id).first() if booking else None
    if incoming_message:
        match incoming_message:
            case "1":
                for message in flow_ubicacion(client, booking, ubicacion):
                    messages.append(message)
            case "2":
                for message in flow_facturacion(incoming_message, phone_number):
                    messages.append(message)
            case "3":
                for message in flow_network(client, booking, ubicacion):
                    messages.append(message)
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')
    else:
        pass

    return messages


def flow_network(client: int, booking: int, ubicacion: int) -> list:
    '''
    Conversation flow sending the network data to the user
    '''
    if client:
        messages = [
            f'¡Hola {client.name}! Hola bienvenido a Homada, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Sabemos que puedes necesitar conexión a internet, la red es {ubicacion.ssid} y el password es {ubicacion.clave}.',
                 'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])

            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    else:
        messages = [
            f'¡Hola! Hola bienvenido a Homada, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Sabemos que puedes necesitar conexión a internet, la red es {ubicacion.ssid} y el password es {ubicacion.clave}.',
                 'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])

            if 'menu' in session:
                delete_session()
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
    return messages


def flow_ubicacion(client: int, booking: int, ubicacion: int) -> list:
    '''
    Conversation flow sending the location data to the user
    '''
    if client:
        messages = [f'¡Hola {client.name}!, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'{client.name}, para tu entrada el día {booking.arrival.strftime("%d/%m/%Y")}, queremos compartirte algunos datos. ',
                 f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion.url}.',
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
                [f'Para tu entrada el día {booking.arrival.strftime("%d/%m/%Y")}, queremos compartirte algunos datos. ',
                 f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion.url}.',
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
    messages = []

    if incoming_message:
        if 'question_id' in session:
            question_id = session['question_id']

            print(question_id, flush=True)
            # Answer saved
            match question_id:
                case 1:
                    session['nombre_cliente'] = incoming_message
                    print(
                        f"Nombre del cliente {session['nombre_cliente']}", flush=True)

                case 2:
                    session['telefono_cliente'] = incoming_message
                    print(
                        f"Nombre del cliente {session['nombre_cliente']}", flush=True)
                case 3:
                    if validate_email(incoming_message):
                        session['email_cliente'] = incoming_message
                        print(
                            f"Email del cliente {session['email_cliente']}", flush=True)
                    else:
                        messages.append(
                            f'El correo electrónico no es válido, por favor intenta nuevamente')
                        messages.append(
                            Questions.query.get(question_id).question)
                        return messages

                case 4:
                    session['num_reservacion_cliente'] = incoming_message
                    print(
                        f"Numero de reservacion del cliente {session['num_reservacion_cliente']}", flush=True)
                case 5:
                    # validate that the date is in the correct format and that it is a date that has not yet passed
                    if validate_date(incoming_message):
                        session['dia_llegada_cliente'] = incoming_message
                        print(
                            f"Dia de llegada del cliente {session['dia_llegada_cliente']}", flush=True)
                    else:
                        messages.append(
                            f'La fecha no es válida, por favor intenta nuevamente')
                        messages.append(Questions.query.get(
                            question_id).question)
                        return messages
                case 6:
                    # validate that the date is in the corredt format and that it is a date that has not yet passed and that it is greater than the arrival date
                    if validate_date(incoming_message):
                        session['dia_salida_cliente'] = incoming_message
                        print(
                            f"Dia de salida del cliente {session['dia_salida_cliente']}", flush=True)
                    else:
                        messages.append(
                            f'La fecha no es válida, por favor intenta nuevamente')
                        messages.append(Questions.query.get(
                            question_id).question)
                        return messages
                case 7:
                    session['ubicacion_cliente'] = incoming_message
                    print(
                        f"Ubicacion del cliente {session['ubicacion_cliente']}", flush=True)
                    ubicacion_query = Ubicacion.query.filter_by(
                        ubicacion=session['ubicacion_cliente']).first()
                    session['hr_llegada_cliente'] = ubicacion_query.arrival_time
                    session['hr_salida_cliente'] = ubicacion_query.departure_time
                    print(
                        f"Hora de llegada del cliente {session['hr_llegada_cliente']}", flush=True)
                    print(
                        f"Ubiacion del cliente {session['ubicacion_cliente']}", flush=True)
                case _:
                    pass

            next_id_question = int(session['question_id'])+1
            print("Siguiente pregunta", flush=True)
            next_question = Questions.query.filter_by(
                id=next_id_question, type_question="Reserva").first()
            if next_question:
                print(
                    f"Pregunta siguiente {next_question.question}", flush=True)
                session['question_id'] = next_question.id
                messages.append(next_question.question)
            else:
                session['revision'] = 1
                if 'question_id' in session:
                    del session['question_id']
                messages.append(review_user())

        elif 'revision' in session:
            print(f"En revision\n{incoming_message}", flush=True)
            if incoming_message == "si":
                save_reservation()
                notify_client(session['telefono_cliente'])
                messages.append(goodbye_twiml())
            else:
                # restart the conversation
                messages.append(
                    "De acuerdo, vamos a empezar de nuevo o si prefieres puedes escribir la palabra 'salir' para terminar la conversación")
                messages.append(redirect_to_first_question())
        else:
            print("Primera pregunta", flush=True)
            pregunta = redirect_to_first_question()
            print("Pregunta " + pregunta, flush=True)
            messages.append(pregunta)
    else:
        pass

    return messages


def notify_client(phone_number: str) -> None:
    '''
    Send a notification to the client telling him about the reservation
    '''
    client = Client.query.filter_by(phone=phone_number).first()
    if client:
        body = f"¡Hola {client.name}!, muchas gracias por tu preferencia. Para tu entrada el día {session['dia_llegada_cliente']}, queremos compartirte algunos datos. Para tu facilidad, el link de navegación es el siguiente: {session['ubicacion_cliente']}. En caso de necesitar apoyo por favor escribe en el chat la palabra 'menú'"
        client = TwilioClient(
            Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=f'whatsapp:{phone_number}',
            from_=Config.TWILIO_PHONE_NUMBER,
            body=body
        )
        print(message.sid, flush=True)


def delete_session_completly() -> None:
    '''
    Delete the keys in the session dictionary
    '''
    for key in list(session.keys()):
        print(f'Eliminando {key}: {session[key]}', flush=True)
        del session[key]


def delete_session():
    '''
    Delete the keys in the session dictionary
    '''
    for key in ['question_id', 'revision', 'nombre_cliente', 'telefono_cliente', 'email_cliente', 'num_reservacion_cliente', 'dia_llegada_cliente', 'dia_salida_cliente', 'ubicacion_cliente', 'hr_llegada_cliente', 'hr_salida_cliente']:
        if key in session:
            del session[key]


def redirect_to_first_question() -> str:
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question


def font(style: str, text: str) -> str:
    '''
    Return the text with the style
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


def review_user() -> str:
    '''
    Sends the information with session keys info to the admin to review
    '''
    def bold(x: str) -> str: return f"*{x}*"

    review_text = f'''
{bold("-Nombre:")} {session['nombre_cliente']}
{bold("-Telefono:")} {session['telefono_cliente']}
{bold("-Email:")} {session['email_cliente']}
{bold("-No. Reservación:")} {session['num_reservacion_cliente']}
{bold("-Día de llegada:")} {session['dia_llegada_cliente']}
{bold("-Día de salida:")} {session['dia_salida_cliente']}
{bold("-Día de salida:")} {(session['ubicacion_cliente']).title()}
{bold("-Hora de llegada:")} {session['hr_llegada_cliente']}
{bold("-Hora de salida:")} {session['hr_salida_cliente']}

¿Los datos son correctos?
Contesta con "si" o "no"
'''
    return review_text


def goodbye_twiml() -> str:
    goodbye = f"Ya quedo creada la reservación {session['num_reservacion_cliente']} :)"
    delete_session()
    return goodbye


def welcome_homada(resp) -> str:
    '''
    Sends a welcome message to the admin and a list of fields to fill in order to create a reservation and a client
    '''
    resp.message("Hola, bienvenido a Homada 👍")
    resp.message(
        "Para la creación de una reservación es necesario crear el cliente con los siguientes datos:")
    resp.message(
        " - Nombre\n- Teléfono\n- Email\n- Número de reservación\n- Día de llegada\n- Hora de llegada\n- Día de partida\n- Hora de partida\n- ubicación")


def menu(resp) -> None:
    '''
    Sends the client the menu of options
    '''
    resp.message(
        "¿Qué deseas hacer? 💫\n1. Obtener Ubicación 📍\n2. Facturación 💳\n3. Clave WIFI 🔐")


def goodbye_client(resp) -> None:
    '''
    Sends a goodbye message to the client
    '''
    resp.message(f'¡Adiós! Esperamos verte pronto 😃')


def client_flow(incoming_message, resp, phone_number) -> None:
    '''
    Creates the flow for the client to follow if the client is already in the database,
    has a reservation the incoming message is a menu option
    '''
    if incoming_message == "menu" or "menu" in session:
        if validate_phone_number(phone_number) or validate_reservation_number(incoming_message) or "reservacion" in session:
            if incoming_message == "menu" or session['menu'] == 3:
                menu(resp)
                session['menu'] = 0
            elif "menu" in session and session['menu'] == 1:
                for message in conversations_client(phone_number, incoming_message):
                    resp.message(message)
            if "menu" not in session or session['menu'] == 0:
                session['menu'] = 1
        else:
            session['menu'] = 0
            no_reservation_found(resp)


def no_reservation_found(resp) -> str:
    '''No reservation found'''
    resp.message(
        'Lo sentimos, no pudimos encontrar una reservación a tu nombre 😟')
    resp.message('Por favor compartenos tu número de reservación.')


def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    # Get the document of the person sending the text message

    resp = MessagingResponse()
    admin = Admin.query.filter_by(phone=phone_number).first()
    if not admin:
        # Client conversation
        client_flow(incoming_message, resp, phone_number)
    elif phone_number == admin.phone:
        if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias":
            delete_session_completly()
            goodbye_client(resp)
        elif incoming_message == "menu" or "menu" in session:
            client_flow(incoming_message, resp, phone_number)
        elif incoming_message == 'cancelar reserva' or incoming_message == 'cancelar' or 'cancelar' in session:
            for message in cancel_reservation(incoming_message):
                resp.message(message)
        else:
            if 'question_id' not in session and 'revision' not in session:
                if 'revision' not in session:
                    welcome_homada(resp)

            for message in conversations_homada(incoming_message):
                resp.message(message)
    else:
        no_reservation_found(resp)
        session['reservacion'] = 1
    return str(resp)


def cancel_reservation(incoming_message: str) -> list:
    '''
    Cancel reservation
    '''
    session['cancelar'] = True
    messages = []
    if incoming_message:
        if 'question_id' in session:
            match  session['question_id']:
                case 8:
                    session['booking_no'] = incoming_message
                    print(
                        f'El número de reservación es: {session["booking_no"]}')
                case _:
                    pass
            session['review_cancel'] = True
            if 'question_id' in session:
                del session['question_id']
            messages.append(
                f'¿Estás seguro que deseas cancelar la reservación {session["booking_no"]}?')

        elif 'review_cancel' in session:
            if incoming_message == 'si':
                # delete the reservation from the database with the booking numberç
                delete_reservation(session['booking_no'])
                messages.append(f'Reservación cancelada')
                delete_session_completly()
            elif incoming_message == 'no':
                messages.append('Reservación no cancelada')
                delete_session_completly()
        else:
            question = Questions.query.filter_by(
                id=8, type_question="Cancelacion").first()
            messages.append(question.question)
            session['question_id'] = question.id
    else:
        pass

    return messages


def flow_facturacion(incoming_message: str, phone_number: str, resp: str) -> str:
    session['upload'] = True
    messages = []
    if incoming_message:
        print(incoming_message)
        if 'question_id' in session:
            match session['question_id']:
                case 9:
                    print(f'{incoming_message}')
                    media_url = request.form.get('MediaUrl0', None)
                    if media_url:
                        r = requests.get(media_url)
                        print(r.content)
                        content_type = r.headers['content-type']
                        client = Client.query.filter_by(
                            phone=phone_number).first()
                        if content_type == 'application/pdf':
                            filename = f'uploads/{client.name}/factura.pdf'
                        else:
                            filename = None
                        if filename:
                            if not os.path.exists(f'uploads/{client.name}'):
                                os.makedirs(f'uploads/{client.name}')
                            with open(filename, 'wb') as f:
                                f.write(r.content)
                            session['document'] = filename.replace(
                                'uploads/', '')
                            messages.append(
                                f'Gracias por enviarnos tu factura {client.name} 😃')
                            session['review_upload'] = True
                        else:
                            messages.append(
                                f'Lo sentimos, no pudimos recibir tu factura, solo se aceptan archivos en formato PDF 😟')
                            messages.append(
                                Questions.query.filter_by(id=9, type_question="Factura").first().question)
                            return messages
                    else:
                        messages.append(
                            f'Lo sentimos, no pudimos recibir tu factura 😟')
                case _:
                    pass

            if 'question_id' in session:
                del session['question_id']
            messages.append(
                f'¿Estás seguro que deseas subir el documento {session["document"]}?')

        elif 'review_upload' in session:
            if incoming_message == 'si':
                upload_document(filename, session['document'], phone_number)
                messages.append(f'Documento subido')
                delete_session_completly()
            elif incoming_message == 'no':
                messages.append('Documento no subido')
        else:
            question = Questions.query.filter_by(
                id=9, type_question="Upload").first()
            messages.append(question.question)
            session['question_id'] = question.id
    else:
        print('No message')

    return messages
