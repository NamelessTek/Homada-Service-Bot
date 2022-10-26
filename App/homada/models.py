from homada import db
from dataclasses import dataclass
from datetime import datetime
from homada.relations import *


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
    email: str = db.Column(db.String(280), nullable=True)
    mascotas: bool = db.Column(db.Boolean, nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False)
    option: str = db.Column(db.String(280), nullable=True)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return {"ID": self.id, "Ubicacion": self.ubicacion, "Email": self.email, "URL": self.url, "Direccion": self.direccion, "SSID": self.ssid, "Clave": self.clave, "Modem": self.modem,
                "Mascotas": self.mascotas, "Status": self.status, "Option": self.option, "Creation Date": self.creation_date, "Last Update": self.last_update}


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

    def __repr__(self):
        return {"ID": self.id, "Option": self.option, "Value": self.value,
                "Creation Date": self.creation_date, "Last Update": self.last_update}


@dataclass()
class Client(db.Model):
    '''
    Client Model for storing client related data 
    '''
    __tablename__ = 'Client'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    last_name: str = db.Column(db.String(280), nullable=False)
    phone: str = db.Column(db.String(280), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Child relationships
    ubicaciones = db.relationship('Ubicacion', secondary=Relation_table_client_ubicacion,
                                  backref=db.backref('client_ubicacion', lazy='dynamic'))

    def __repr__(self):
        return {"ID": self.id, "Name": self.name, "Last Name": self.last_name, "Phone": self.phone, "Status": self.status,
                "Creation Date": self.creation_date, "Last Update": self.last_update}


@dataclass()
class Booking(db.Model):
    '''
    Booking Model for storing client-location booking related data
    '''
    __tablename__ = 'Booking'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    booking_number: str = db.Column(db.String(280), nullable=False)
    arrival: str = db.Column(db.Date, nullable=False)
    arrival_time: str = db.Column(db.Time, nullable=False)
    departure: str = db.Column(db.Date, nullable=False)
    departure_time: str = db.Column(db.Time, nullable=False)
    ubicacion: int = db.Column(db.Integer, db.ForeignKey(
        'Ubicacion.id'), nullable=False)
    cliente: int = db.Column(db.Integer, db.ForeignKey(
        'Client.id'), nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    status: bool = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return {"ID": self.id, "Booking Number": self.booking_number, "Arrival": self.arrival, "Arrival Time": self.arrival_time,
                "Departure": self.departure, "Departure Time": self.departure_time, "Ubicacion": self.ubicacion,
                "Client": self.cliente, "Creation Date": self.creation_date, "Last Update": self.last_update, "Status": self.status}
