from homada.models import *
from homada import db

Relation_client_document_table = db.Table('Relation_client_document_table',
                                          db.Column(
                                              'cliente_id', db.Integer, db.ForeignKey('Client.id')),
                                          db.Column(
                                              'upload_id', db.Integer, db.ForeignKey('Uploads.id'))
                                          )
