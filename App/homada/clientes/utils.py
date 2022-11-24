from homada.facturacion.utils import flow_facturacion
from homada.tools.utils import *
from homada.models import Client, Booking, Ubicacion
from homada import db
from homada.log.utils import create_log
from twilio.rest import Client as TwilioClient
from flask import session
from homada.config import Config


def get_client(client: Client) -> dict:
    '''
    Get client data with a client object type
    '''
    return Client.get_data(Client.query.filter_by(phone=client).first())


def create_client(name: str, phone: str, email: str) -> Client:
    '''
    Create client data in the database by receiving the name, last name, phone and email
    from whatsApp
    '''
    query_client = Client.query.filter_by(phone=phone).first()
    if not query_client:
        client = Client(name=name.title(), phone=phone, email=email)
        db.session.add(client)
        db.session.commit()
        create_log(client.__class__.__name__,
                   client.id, 1, session['admin_id'])
    else:
        raise Exception('Client already exists')

    return client

def create_client_carga_masiva(name: str, phone: str, email: str) -> Client:
    '''
    Create client data in the database by receiving the name, last name, phone and email
    from whatsApp
    '''
    query_client = Client.query.filter_by(phone=phone).first()
    if not query_client:
        client = Client(name=name.title(), phone=phone, email=email)
        db.session.add(client)
        db.session.commit()
        create_log(client.__class__.__name__,
                   client.id, 1, 1)
    else:
        raise Exception('Client already exists')

    return client


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


def review_client() -> str:
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
