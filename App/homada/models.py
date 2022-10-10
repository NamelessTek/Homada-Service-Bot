from optparse import Option
from homada import db
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ubicacion(db.Model):
    __tablename__ = 'Ubicacion'

    Id: int = db.Column(db.Integer, primary_key=True,
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
        rows = {"ID": self.Id, "Ubicacion": self.ubicacion, "URL": self.url, "Direccion": self.direccion, "SSID": self.ssid, "Clave": self.clave, "Modem": self.modem,
                "Mascotas": self.mascotas, "Status": self.status, "Option": self.option, "Creation Date": self.creation_date, "Last Update": self.last_update}
        return rows


@dataclass
class Option(db.Model):
    __tablename__ = 'Option'

    Id: int = db.Column(db.Integer, primary_key=True)
    option: int = db. Column(db.Integer, nullable=False)
    value: str = db.Column(db.String(280), nullable=False)
    creation_date: str = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    last_update: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        rows = {"ID": self.Id, "Option": self.option, "Value": self.value,
                "Creation Date": self.creation_date, "Last Update": self.last_update}
        return rows
