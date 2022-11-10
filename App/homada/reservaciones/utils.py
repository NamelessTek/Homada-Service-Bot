from homada import db
from homada.models import Booking, Client, Ubicacion
from homada.clientes.utils import create_client
from flask import session
import datetime


def get_booking(booking: Booking) -> dict:
    '''
    Get booking data in the database in a dictionary
    '''
    return {key: value for key, value in Booking.get_data(booking).items() if booking.status and value != []}


def save_reservation() -> Booking:
    '''
    Save reservation data in the database, it aks for the client data and the location data and
    creates the booking
    '''

    email = session['email_cliente']
    create_client(session['nombre_cliente'],
                  session['telefono_cliente'], email)

    ubicacion = Ubicacion.query.filter_by(
        ubicacion=session['ubicacion_cliente']).first()

    db.session.add(Booking(booking_number=session['num_reservacion_cliente'], arrival=datetime.datetime.strptime(
        session['dia_llegada_cliente'], '%d-%m-%Y'), departure=datetime.datetime.strptime(
        session['dia_salida_cliente'], '%d-%m-%Y'), client=Client.query.filter_by(email=email).first(), ubicacion=ubicacion,
        arrival_time=ubicacion.arrival_time, departure_time=ubicacion.departure_time))
    db.session.commit()


def delete_reservation(booking_no: str) -> None:
    '''
    Delete reservation from database
    '''
    reservation = Booking.query.filter_by(
        booking_number=booking_no).first()
    reservation.status = False
    db.session.commit()


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
