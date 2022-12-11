from homada.models import Admin
from homada.clientes.utils import initialize_client_conversation
from homada.admin.utils import initialize_admin_conversation
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
<<<<<<< HEAD
        client = Client.query.filter_by(phone=phone_number).first()
        if client:
            session['client_id'] = getattr(Client.query.filter_by(
                phone=phone_number).first(), 'id', None)
            if 'reservación' in session:
                booking = Booking.query.filter_by(
                    booking_number=session['reservación'], status=1).first()
                print('Se mando booking para saber cual es')
                print(booking)
                session['client_id'] = getattr(Client.query.filter_by(
                    id=booking.cliente_id).first(), 'id', None)
            else:
                if incoming_message == "salir" or incoming_message == "adios" or incoming_message == "gracias":
                    delete_session_completly()
                    goodbye_client(resp)
                elif incoming_message == "menú" or "menú" in session or incoming_message == "menu":
                    client_flow(incoming_message, resp, phone_number)
                else:
                    welcome_client(resp)
        else:
            print('No client')
            no_reservation_found(resp)
            session['reservación'] = 1
=======
        initialize_client_conversation(incoming_message, phone_number, resp)
>>>>>>> a9797c673a1b49dcce187ed5abacd81eddbdf83e
    elif phone_number == admin.phone:
        # Admin conversation
        session['admin_id'] = admin.id
        initialize_admin_conversation(incoming_message, phone_number, resp)
    else:
        resp.message("No se encontró el número de teléfono")
    return str(resp)


def error_twiml() -> str:
    goodbye = f"No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe {font_weight('bold', 'menú')} para desplegar las opciones con las que podemos apoyarte."
    delete_session()
    return goodbye
