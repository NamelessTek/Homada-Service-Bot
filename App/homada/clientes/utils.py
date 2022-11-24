from homada import db
from homada.models import Client


def get_client(client: Client) -> dict:
    '''
    Get client data
    '''
    return Client.get_data(Client.query.filter_by(phone=client).first())


def create_client(name: str, phone: str, email: str) -> Client:
    '''
    Create client data in the database by receiving the name, last name, phone and email
    from whatsApp
    '''
    query_client = Client.query.filter_by(phone=phone).first()
    if not query_client:

        client = Client(name=name, phone=phone, email=email)
        db.session.add(client)
        db.session.commit()
    else:
        raise Exception('Client already exists')

    return client
