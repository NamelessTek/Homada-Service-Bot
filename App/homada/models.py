from optparse import Option
from homada import db
from dataclasses import dataclass
from datetime import datetime


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
    status: bool = db.Column(db.Boolean, nullable=False)
    option: Option = db.Column(db.String(280), nullable=True)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return {"ID": self.id, "Ubicacion": self.ubicacion, "URL": self.url, "Direccion": self.direccion, "SSID": self.ssid, "Clave": self.clave, "Modem": self.modem,
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
    Client Model for storing client related details 
    '''
    __tablename__ = 'Client'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    last_name: str = db.Column(db.String(280), nullable=False)
    phone: str = db.Column(db.String(280), nullable=False)
    reservation: str = db.Column(db.String(280), nullable=False)
    arrvial = db.Column(db.DateTime, nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return {"ID": self.id, "Name": self.name, "Last Name": self.last_name, "Phone": self.phone, "Reservation": self.reservation, "Arrival": self.arrvial, "Departure": self.departure, "Status": self.status, "Creation Date": self.creation_date, "Last Update": self.last_update}
