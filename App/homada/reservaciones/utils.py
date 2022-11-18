from homada import db
from homada.models import Booking, Client, Ubicacion
from homada.clientes.utils import create_client
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
