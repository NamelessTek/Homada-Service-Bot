from homada import db
from homada.models import Booking, Client, Ubicacion
from homada.clientes.utils import create_client
from homada.log.utils import create_log
from flask import session
import datetime


def get_booking(booking: Booking) -> dict[str, str]:
    '''
    Get booking data in the database in a dictionary
    '''
    return {key: value for key, value in Booking.get_data(booking).items() if booking.status and value != []}


def save_reservation() -> None:
    '''
    Save reservation data in the database, it aks for the client data and the location data and
    creates the booking
    '''
    email = session['email_cliente']
    create_client(session['nombre_cliente'],
                  session['telefono_cliente'], email) if not Client.query.filter_by(email=email).first() else None

    ubicacion = Ubicacion.query.filter_by(
        ubicacion=session['ubicacion_cliente']).first()
    booking = create_booking(email, ubicacion) if not Booking.query.filter_by(
        booking_number=session['num_reservacion_cliente']).first() else None

    return booking

def save_reservation_data_loader(req_data):
    '''
    Save reservation data in the database, it aks for the client data and the location data and
    creates the booking
    '''
    email = req_data['email_cliente']
    print(email)
    create_client(req_data['nombre_cliente'],
                  req_data['telefono_cliente'], email) if not Client.query.filter_by(email=email).first() else None

    ubicacion = Ubicacion.query.filter_by(
        ubicacion=req_data['ubicacion_cliente']).first()
    booking = create_booking(email, ubicacion) if not Booking.query.filter_by(
        booking_number=req_data['num_reservacion_cliente']).first() else None

    return booking

def create_booking(email: str, ubicacion: str) -> Booking:
    '''
    Create booking data in the database by receiving the email and the location
    '''
    query_booking = Booking.query.filter_by(
        booking_number=session['num_reservacion_cliente']).first()
    if not query_booking:
        booking = Booking(booking_number=session['num_reservacion_cliente'], arrival=datetime.datetime.strptime(
            session['dia_llegada_cliente'], '%d-%m-%Y'), departure=datetime.datetime.strptime(
            session['dia_salida_cliente'], '%d-%m-%Y'), client=Client.query.filter_by(email=email).first(), ubicacion=ubicacion,
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
