from homada.models import Ubicacion


def get_ubicacion(ubicacion: int) -> dict:
    return Ubicacion.__repr__(Ubicacion.query.filter_by(id=ubicacion).first())
