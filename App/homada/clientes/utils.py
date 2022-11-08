from typing import List
from homada import db
from homada.models import Client, Ubicacion
from homada.ubicacion.utils import get_ubicacion
import datetime


def get_client(client: Client) -> dict:
    '''
    Get client data
    '''
    return Client.__repr__(Client.query.filter_by(id=client).first())


def create_client(name: str, last_name: str, phone: str, email: str) -> dict:
    '''
    Create client data in the database by receiving the name, last name, phone and email
    from whatsApp
    '''
    client = Client(name, last_name, phone, email, True,
                    datetime.now(), datetime.now())
    db.session.add(client)
    db.session.commit()
