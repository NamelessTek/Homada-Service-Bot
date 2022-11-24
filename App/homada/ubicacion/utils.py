from homada.models import Ubicacion


def get_ubicacion(ubicacion: int) -> dict:
    return {key: value for key, value in Ubicacion.get_data(ubicacion).items() if ubicacion.status and value != []}
