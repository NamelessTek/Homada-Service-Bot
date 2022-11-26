from homada.models import Admin, Client
from homada.tools.utils import *
from homada.clientes.utils import notify_client, review_client
from homada.reservaciones.utils import save_reservation
from flask import session


def get_admin(admin: str) -> dict:
    '''return all the columns of the admin table'''
    return Admin.__repr__(Admin.query.filter_by(phone=admin).first())


def get_admin_phones() -> list:
    '''return phones of all admins'''
    phones = []
    admins = Admin.query.all()
    for admin in admins:
        phones.append(admin.phone)
    return phones


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
                    if not Booking.query.filter_by(booking_number=incoming_message, status=1).first():
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
                messages.append(review_client())

        elif 'revision' in session:
            if incoming_message == "si":
                reservation = save_reservation()
                if not reservation:
                    messages.append(
                        f'No se pudo guardar la reservación, por favor intenta nuevamente')
                else:
                    notify_client(session['telefono_cliente'])
                    messages.append(goodbye_admin())
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


def goodbye_admin() -> str:
    '''Goodbye message'''
    goodbye = f"Ya quedó creada la reservación {session['num_reservacion_cliente']} :)"
    delete_session()
    return goodbye


def redirect_to_first_question() -> str:
    '''
    Redirect the user to the first question
    '''
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question
