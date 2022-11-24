from homada.config import Config
from twilio.rest import Client as TwilioClient
from homada.models import Ubicacion, Client, Booking, Questions, Admin
from homada.reservaciones.utils import save_reservation, delete_reservation
from homada.email.utils import send_email
from homada.facturacion.utils import flow_facturacion
from homada.tools.utils import *
from twilio.twiml.messaging_response import MessagingResponse
from flask import session, request


def conversations_client(phone_number: str, incoming_message: str) -> list[str]:
    '''
    Conversations with the user
    '''
    messages: list[str] = []
    client = Client.query.filter_by(phone=phone_number).first()
    if not client:
        booking = Booking.query.filter_by(
            booking_number=session['reservación'], status=1).first()
        ubicacion = Ubicacion.query.filter_by(
            id=booking.ubicacion_id).first() if booking else None
    else:
        booking = Booking.query.filter_by(
            cliente_id=client.id, status=1).first()
        ubicacion = Ubicacion.query.filter_by(
            id=booking.ubicacion_id).first() if booking else None
    if "factura" in session:
        for message in flow_facturacion(incoming_message):
            messages.append(message)
        incoming_message = None
    if incoming_message:
        match incoming_message:
            case "1":
                for message in flow_ubicacion(client, booking, ubicacion):
                    messages.append(message)
            case "2":
                for message in flow_facturacion(incoming_message):
                    messages.append(message)
            case "3":
                for message in flow_network(client, booking, ubicacion):
                    messages.append(message)
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menú para desplegar las opciones con las que podemos apoyarte.')
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
                [f'Sabemos que puedes necesitar conexión a internet, la red es {font_weight("bold", ubicacion.ssid)} y el password es {font_weight("bold",ubicacion.clave)}.',
                 f'En caso de necesitar apoyo por favor escribe en el chat la palabra {font_weight("bold", "menú")}.'])

            delete_session() if 'menú' in session else None

        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservación')
    else:
        messages = [
            f'¡Hola! Hola bienvenido a Homada, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Sabemos que puedes necesitar conexión a internet, la red es {ubicacion.ssid} y el password es {ubicacion.clave}.',
                 f'En caso de necesitar apoyo por favor escribe en el chat la palabra {font_weight("bold", "menú")}.'])

            delete_session() if 'menú' in session else None
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservación')
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
            delete_session() if 'menú' in session else None
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservación')
    else:
        messages = [f'¡Hola!, muchas gracias por tu preferencia']
        if booking:
            messages.extend(
                [f'Para tu entrada el día {booking.arrival.strftime("%d/%m/%Y")}, queremos compartirte algunos datos. ',
                 f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion.url}.',
                 'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
            delete_session() if 'menú' in session else None
        else:
            messages.append(
                f'{client.name}, no tienes reservaciones, por favor haz una reservación')
    return messages


def conversations_admin(incoming_message: str) -> list[str]:
    '''
    Conversations with the homada user
    '''
    messages: list[str] = []

    if incoming_message:
        if 'question_id' in session:
            question_id = session['question_id']
            match question_id:
                case 1:
                    client = Client.query.filter_by(
                        phone=incoming_message).first()
                    if not client:
                        session['telefono_cliente'] = incoming_message
                    else:
                        session['telefono_cliente'] = client.phone
                        session['nombre_cliente'] = client.name
                        session['email_cliente'] = client.email
                        session['question_id'] = 3

                case 2:
                    session['nombre_cliente'] = incoming_message
                case 3:
                    if validate_email(incoming_message):
                        session['email_cliente'] = incoming_message
                    else:
                        messages.append(
                            f'El correo electrónico no es válido, por favor intenta nuevamente')
                        messages.append(
                            Questions.query.get(question_id).question)
                        return messages

                case 4:
                    if not Booking.query.filter_by(booking_number=incoming_message).first():
                        session['num_reservacion_cliente'] = incoming_message
                    else:
                        messages.append(
                            f'El número de reservación ya existe, por favor intenta nuevamente')
                        messages.append(
                            Questions.query.get(question_id).question)
                        return messages
                case 5:
                    # validate that the date is in the correct format and that it is a date that has not yet passed
                    if validate_date(incoming_message):
                        session['dia_llegada_cliente'] = incoming_message
                    else:
                        messages.append(
                            f'La fecha no es válida, por favor intenta nuevamente')
                        messages.append(Questions.query.get(
                            question_id).question)
                        return messages
                case 6:
                    # validate that the date is in the corredt format and that it is a date that has not yet passed and that it is greater than the arrival date
                    if validate_date(incoming_message) and incoming_message > session['dia_llegada_cliente']:
                        session['dia_salida_cliente'] = incoming_message
                    else:
                        messages.append(
                            f'La fecha no es válida, por favor intenta nuevamente')
                        messages.append(Questions.query.get(
                            question_id).question)
                        return messages
                case 7:

                    session['ubicacion_cliente'] = incoming_message
                    ubicacion_query = Ubicacion.query.filter_by(
                        ubicacion=session['ubicacion_cliente']).first()
                    session['hr_llegada_cliente'] = ubicacion_query.arrival_time
                    session['hr_salida_cliente'] = ubicacion_query.departure_time
                case _:
                    pass

            next_id_question = int(session['question_id'])+1
            next_question = Questions.query.filter_by(
                id=next_id_question, type_question="Reserva").first()
            if next_question:
                session['question_id'] = next_question.id
                messages.append(next_question.question)
            else:
                session['revision'] = 1
                if 'question_id' in session:
                    del session['question_id']
                messages.append(review_user())

        elif 'revision' in session:
            if incoming_message == "si":
                reservation = save_reservation()
                if not reservation:
                    messages.append(
                        f'No se pudo guardar la reservación, por favor intenta nuevamente')
                else:
                    notify_client(session['telefono_cliente'])
                    messages.append(goodbye_twiml())
            else:
                # restart the conversation
                messages.append(
                    "De acuerdo, vamos a empezar de nuevo o si prefieres puedes escribir la palabra 'salir' para terminar la conversación")
                messages.append(redirect_to_first_question())
        else:
            pregunta = redirect_to_first_question()
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

        ubicacion = Ubicacion.query.filter_by(
            ubicacion=session['ubicacion_cliente']).first()
        hora_llegada = session['hr_llegada_cliente'].strftime(
            "%H") + "pm" if int(session['hr_llegada_cliente'].strftime("%H")) > 12 else "am"
        body = [
            f"¡Hola {client.name}, bienvenido a Homada!, muchas gracias por tu preferencia.", f"Para tu entrada el día {font_weight('bold',session['dia_llegada_cliente'])}, queremos compartirte algunos datos. La hora de entrada es a las {font_weight('bold',hora_llegada)}. Sabemos que puedes necesitar conexión a internet, la red es {font_weight('bold',ubicacion.ssid)} y el password es {font_weight('bold',ubicacion.clave)}. Para tu facilidad el link de navegación es el siguiente: {font_weight('bold',ubicacion.url)}.", f" En caso de necesitar apoyo por favor escribe en el chat la palabra {font_weight('bold', 'menú')}"]
        client = TwilioClient(
            Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        for message in body:
            client.messages.create(
                to=f'whatsapp:{phone_number}',
                from_=Config.TWILIO_PHONE_NUMBER,
                body=message
            )


def redirect_to_first_question() -> str:
    '''
    Redirect the user to the first question
    '''
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question


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


def review_user() -> str:
    '''
    Sends the information with session keys info to the admin to review
    '''
    def bold(x: str) -> str: return f"*{x}*"

    review_text = f'''
{bold("-Teléfono:")} {session['telefono_cliente']}
{bold("-Nombre:")} {session['nombre_cliente']}
{bold("-Email:")} {session['email_cliente']}
{bold("-No. Reservación:")} {session['num_reservacion_cliente']}
{bold("-Día de llegada:")} {session['dia_llegada_cliente']}
{bold("-Día de salida:")} {session['dia_salida_cliente']}
{bold("-Ubicación de Hospedaje:")} {(session['ubicacion_cliente']).title()}
{bold("-Hora de llegada:")} {session['hr_llegada_cliente']}
{bold("-Hora de salida:")} {session['hr_salida_cliente']}

¿Los datos son correctos?
Contesta con "si" o "no"
'''
    return review_text


def error_twiml() -> str:
    goodbye = f"No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe {font_weight('bold', 'menú')} para desplegar las opciones con las que podemos apoyarte."
    delete_session()
    return goodbye


def goodbye_twiml() -> str:
    goodbye = f"Ya quedó creada la reservación {session['num_reservacion_cliente']} :)"
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
        " - Nombre\n- Teléfono\n- Email\n- Número de reservación\n- Día de llegada\n- Hora de llegada\n- Día de partida\n- Hora de partida\n- Ubicación")


def menu(resp) -> None:
    '''
    Sends the client the menú of options
    '''
    resp.message(
        "¿Qué deseas hacer? 💫\n1. Obtener Ubicación 📍\n2. Facturación 💳\n3. Clave WIFI 🔐")


def goodbye_client(resp) -> None:
    '''
    Sends a goodbye message to the client
    '''
    resp.message(f'¡Adiós! Esperamos verte pronto 😃')


def client_flow(incoming_message: str, resp: str, phone_number: str) -> None:
    '''
    Creates the flow for the client to follow if the client is already in the database,
    has a reservation the incoming message is a menú option
    '''
    if incoming_message == "menú" or "menú" in session or incoming_message == "menu":
        if validate_phone_number(phone_number) or validate_reservation_number(incoming_message) or "reservación" in session:
            client = Client.query.filter_by(phone=phone_number).first()
            if not client:
                booking = Booking.query.filter_by(
                    booking_number=session['reservación'], status=1).first()
            else:
                booking = Booking.query.filter_by(
                    cliente_id=client.id, status=1).first()
                if not booking:
                    client = None
            if client or booking:
                if incoming_message == "menú" or incoming_message == "menu" or session['menú'] == 3:
                    menu(resp)
                    session['menú'] = 0
                elif "menú" in session and session['menú'] == 1:
                    for message in conversations_client(phone_number, incoming_message):
                        resp.message(message)

                if "menú" not in session or session['menú'] == 0:
                    session['menú'] = 1
            else:
                session['menú'] = 0
                no_reservation_found(resp)
        else:
            session['menú'] = 0
            no_reservation_found(resp)
    else:
        pass


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
    admin = Admin.query.filter_by(phone=phone_number, status=1).first()
    if not admin:
        # Client conversation
        session['client_id'] = getattr(Client.query.filter_by(
            phone=phone_number).first(), 'id', None)
        if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias":
            delete_session_completly()
            goodbye_client(resp)
        elif incoming_message == "menú" or "menú" in session or incoming_message == "menu":
            client_flow(incoming_message, resp, phone_number)
        else:
            no_reservation_found(resp)
            session['reservación'] = 1
    elif phone_number == admin.phone:
        # Admin conversation
        session['admin_id'] = admin.id
        if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias":
            delete_session_completly()
            goodbye_client(resp)
        elif incoming_message == "menú" or "menú" in session or incoming_message == "menu":
            client_flow(incoming_message, resp, phone_number)
        elif incoming_message == 'cancelar reserva' or incoming_message == 'cancelar' or 'cancelar' in session:
            for message in cancel_reservation(incoming_message):
                resp.message(message)
        elif incoming_message == 'factura' or 'factura' in session:
            for message in flow_facturacion(incoming_message):
                resp.message(message)
        else:
            if 'question_id' not in session and 'revision' not in session:
                if 'revision' not in session:
                    welcome_homada(resp)

            for message in conversations_admin(incoming_message):
                resp.message(message)
    else:
        no_reservation_found(resp)
        session['reservación'] = 1
    return str(resp)


def cancel_reservation(incoming_message: str) -> list[str]:
    '''
    Cancel reservation
    '''
    session['cancelar'] = True
    messages: list[str] = []
    if incoming_message:
        if 'question_id' in session:
            match  session['question_id']:
                case 8:
                    session['booking_no'] = incoming_message
                case _:
                    pass
            session['review_cancel'] = True
            if 'question_id' in session:
                del session['question_id']
            messages.append(
                f'¿Estás seguro que deseas cancelar la reservación {session["booking_no"]}?')

        elif 'review_cancel' in session:
            if incoming_message == 'si':
                # delete the reservation from the database with the booking number
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
