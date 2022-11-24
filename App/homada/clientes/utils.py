from homada import db
from homada.models import Client
from homada.log.utils import create_log
from flask import session, request


def get_client(client: Client) -> dict:
    '''
    Get client data with a client object type
    '''
    return Client.get_data(Client.query.filter_by(phone=client).first())


def create_client(name: str, phone: str, email: str) -> Client:
    '''
    Create client data in the database by receiving the name, last name, phone and email
    from whatsApp
    '''
    query_client = Client.query.filter_by(phone=phone).first()
    if not query_client:

        client = Client(name=name.title(), phone=phone, email=email)
        db.session.add(client)
        db.session.commit()
        create_log(client.__class__.__name__,
                   client.id, 1, session['admin_id'])
    else:
        raise Exception('Client already exists')

    return client
