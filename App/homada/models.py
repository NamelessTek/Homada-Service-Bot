from homada import db
from dataclasses import dataclass
from datetime import datetime
from homada.relations import *


@dataclass
class Admin(db.Model):
    '''
    Admin model
    '''
    __tablename__ = 'Admin'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    phone: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False,)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@dataclass
class Ubicacion(db.Model):
    '''
    Ubicacion Model for storing ubicacion related details 
    '''
    __tablename__ = 'Ubicacion'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    ubicacion: str = db.Column(db.String(280), nullable=False)
    url: str = db.Column(db.String(500), nullable=False)
    direccion: str = db.Column(db.String(280), nullable=False)
    ssid: str = db.Column(db.String(280), nullable=True)
    clave: str = db.Column(db.String(280), nullable=True)
    modem: str = db.Column(db.String(280), nullable=True)
    mascotas: bool = db.Column(db.Boolean, nullable=False)
    arrival_time: str = db.Column(db.Time, nullable=False)
    departure_time: str = db.Column(db.Time, nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    option: str = db.Column(db.String(280), nullable=True)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # child relationship
    bookings = db.relationship(
        'Booking', backref='ubicacion', lazy='dynamic')

    def __repr__(self) -> dict:
        return {column.capitalize(): getattr(self, column) for column in [column.name for column in self.__table__.columns]}

    def __str__(self) -> str:
        return self.ubicacion


@dataclass
class Option(db.Model):
    '''
    Option Model serves as a table to store options and values for the app
    '''
    __tablename__ = 'Option'

    id: int = db.Column(db.Integer, primary_key=True)
    option: int = db. Column(db.Integer, nullable=False)
    value: str = db.Column(db.String(280), nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> dict:
        return {column.capitalize(): getattr(self, column) for column in [column.name for column in self.__table__.columns]}


@dataclass
class Questions(db.Model):
    '''
    Questions Model serves as a table to store questions for the app
    '''
    __tablename__ = 'Questions'

    id: int = db.Column(db.Integer, primary_key=True)
    question: str = db.Column(db.String(250), nullable=False)
    type_question: str = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> dict:
        return {column.capitalize(): getattr(self, column) for column in [column.name for column in self.__table__.columns]}


@dataclass
class Client(db.Model):
    '''
    Client Model for storing client related data 
    '''
    __tablename__ = 'Client'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(460), nullable=False)
    phone: str = db.Column(db.String(280), nullable=False)
    status: int = db.Column(db.Integer, nullable=False, default=1)
    email: str = db.Column(db.String(280), nullable=True)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # child relationship
    bookings = db.relationship(
        'Booking', backref='client', lazy='dynamic')

    def __repr__(self) -> dict:
        return {column.capitalize(): getattr(self, column) for column in [column.name for column in self.__table__.columns]}

    def __str__(self) -> str:
        return self.name


@dataclass
class Booking(db.Model):
    '''
    Booking Model for storing client-location booking related data
    '''
    __tablename__ = 'Booking'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    booking_number: str = db.Column(db.String(280), nullable=False)
    arrival: str = db.Column(db.Date, nullable=False)
    departure: str = db.Column(db.Date, nullable=False)

    ubicacion_id: int = db.Column(db.Integer, db.ForeignKey(
        'Ubicacion.id'), nullable=False,)
    cliente_id: int = db.Column(db.Integer, db.ForeignKey(
        'Client.id'), nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    status: int = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> dict:
        # convert to dict and capitalize first letter of each key and captilize ID
        return {column.capitalize(): getattr(self, column) for column in [column.name for column in self.__table__.columns]}

    def __str__(self) -> str:
        return 'Booking %r' % str(self.booking_number)
