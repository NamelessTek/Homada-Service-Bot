from homada.models import *
from homada import db

Relation_table_client_booking = db.Table('Relation_table_client_booking',
                                         db.Column(
                                             'client_id', db.Integer, db.ForeignKey('Client.id')),
                                         db.Column(
                                             'booking_id', db.Integer, db.ForeignKey('Booking.id'))
                                         )
