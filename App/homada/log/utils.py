from homada.models import Log
from homada import db


def create_log(type: str, object_id: int, action: int, admin_id: int) -> Log:
    """
    Create log data in the database by receiving the type, object_id, action and admin_id.
    action:
    1: Create
    2: Update
    3: Delete
    default: Unknown
    """

    match action:
        case 1:
            action = 'Create'
        case 2:
            action = 'Update'
        case 3:
            action = 'Delete'
        case _:
            action = 'Unknown'

    db.session.add(Log(type=type, object_id=object_id,
                   action=action, admin_id=admin_id))
    db.session.commit()


def get_logs() -> list:
    return [log.get_data() for log in Log.query.all()]
