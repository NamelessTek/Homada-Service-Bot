from homada.models import Client, Admin
from homada.reservaciones.utils import cancel_reservation
from homada.email.utils import send_email
from homada.facturacion.utils import flow_facturacion
from homada.clientes.utils import client_flow, goodbye_client, welcome_client
from homada.admin.utils import conversations_admin
from homada.tools.utils import *
from twilio.twiml.messaging_response import MessagingResponse
from flask import session, request


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
        if not session.get('client_id'):
            no_reservation_found(resp)
            session['reservación'] = 1
        else:
            if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias":
                delete_session_completly()
                goodbye_client(resp)
            elif incoming_message == "menú" or "menú" in session or incoming_message == "menu":
                client_flow(incoming_message, resp, phone_number)
            else:
                welcome_client(resp)
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


def error_twiml() -> str:
    goodbye = f"No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe {font_weight('bold', 'menú')} para desplegar las opciones con las que podemos apoyarte."
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
