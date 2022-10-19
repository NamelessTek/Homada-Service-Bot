from homada.models import *
from homada import db


Relation_table_client_ubicacion = db.Table('Relation_table_client_ubicacion',
                                           db.Column('client_id', db.Integer, db.ForeignKey(
                                               'Client.id'), primary_key=True),
                                           db.Column('ubicacion_id', db.Integer, db.ForeignKey('Ubicacion.id'), primary_key=True))
