from homada.tools.utils import delete_session_completly
from homada import db
from homada.models import Booking, Client, Ubicacion, Questions
from homada.clientes.utils import create_client, create_client_carga_masiva
from homada.log.utils import create_log
from flask import session
import datetime


def get_booking(booking: Booking) -> dict[str, str]:
    '''
    Get booking data in the database in a dictionary
    '''
    return {key: value for key, value in Booking.get_data(booking).items() if booking.status and value != []}


def save_reservation() -> Booking:
    '''
    Save reservation data in the database, it aks for the client data and the location data and
    creates the booking
    '''
    create_client(session['nombre_cliente'],
                  session['telefono_cliente'], session['email_cliente']) if not Client.query.filter_by(phone=session['telefono_cliente']).first() else None
    ubicacion = Ubicacion.query.filter_by(
        ubicacion=session['ubicacion_cliente']).first()
    booking = create_booking(session['telefono_cliente'], ubicacion) if not Booking.query.filter_by(
        booking_number=session['num_reservacion_cliente']).first() else None

    return booking


def save_reservation_data_loader(req_data: str):
    '''
    Save reservation data in the database, it aks for the client data and the location data and
    creates the booking
    '''
    session['admin_id'] = 1
    phone = req_data['telefono_cliente']
    client_result = Client.query.filter_by(phone=phone).first()
    if not client_result:
        create_client_carga_masiva(req_data['nombre_cliente'],
                                   req_data['telefono_cliente'], req_data['email_cliente'])

    ubicacion = Ubicacion.query.filter_by(
        ubicacion=req_data['ubicacion_cliente']).first()
    booking = create_booking_data_loader(phone, ubicacion, req_data) if not Booking.query.filter_by(
        booking_number=req_data['num_reservacion_cliente']).first() else None

    return booking


def create_booking_data_loader(phone: str, ubicacion: str, req_data) -> Booking:
    '''
    Create booking data in the database by receiving the email and the location
    '''
    query_booking = Booking.query.filter_by(
        booking_number=req_data['num_reservacion_cliente'], status=1).first()
    if not query_booking:
        booking = Booking(booking_number=req_data['num_reservacion_cliente'], arrival=req_data['dia_llegada_cliente'], departure=req_data['dia_salida_cliente'], client=Client.query.filter_by(phone=phone).first(), ubicacion=ubicacion,
                          arrival_time=ubicacion.arrival_time, departure_time=ubicacion.departure_time)
        db.session.add(booking)
        db.session.commit()
        create_log(booking.__class__.__name__,
                   booking.id, 1, 1)
    else:
        raise Exception('Booking already exists')

    return booking


def create_booking(phone: str, ubicacion: str) -> Booking:
    '''
    Create booking data in the database by receiving the phone and the location
    '''
    query_booking = Booking.query.filter_by(
        booking_number=session['num_reservacion_cliente'], status=1).first()
    if not query_booking:
        booking = Booking(booking_number=session['num_reservacion_cliente'], arrival=datetime.datetime.strptime(
            session['dia_llegada_cliente'], '%d-%m-%Y'), departure=datetime.datetime.strptime(
            session['dia_salida_cliente'], '%d-%m-%Y'), client=Client.query.filter_by(phone=phone).first(), ubicacion=ubicacion,
            arrival_time=ubicacion.arrival_time, departure_time=ubicacion.departure_time)
        db.session.add(booking)
        db.session.commit()
        create_log(booking.__class__.__name__,
                   booking.id, 1, session['admin_id'])
    else:
        raise Exception('Booking already exists')

    return booking


def delete_reservation(booking_no: str) -> None:
    '''
    Delete reservation from database
    '''
    reservation = Booking.query.filter_by(booking_number=booking_no).first()
    reservation.status = False
    db.session.commit()


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
