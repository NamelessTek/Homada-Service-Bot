from typing import List
from homada.models import Client, Ubicacion
from homada.ubicacion.utils import get_ubicacion


def get_client(client: Client) -> dict:
    '''
    Get client data
    '''
    return {key: value for key, value in Client.__repr__(client).items() if client.status and value != []}

# returns list of dicts


def get_client_reservation(client: Client) -> List[dict]:
    '''
    Get client reservation data
    '''
    client_data = Client.query.filter_by(id=client.id).first()
    return [get_ubicacion(
        ubicacion) for ubicacion in client_data.ubicaciones if ubicacion.status]
