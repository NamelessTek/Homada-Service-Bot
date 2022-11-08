from homada.models import Admin


def get_admin(admin: str) -> dict:
    # return all the columns of the admin table
    return Admin.__repr__(Admin.query.filter_by(phone=admin).first())
