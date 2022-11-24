from homada.models import *
from homada import db

Relation_booking_document_table = db.Table('Relation_booking_document_table',
                                           db.Column(
                                               'booking_id', db.Integer, db.ForeignKey('Booking.id')),
                                           db.Column(
                                               'upload_id', db.Integer, db.ForeignKey('Uploads.id'))
                                           )
