from homada.models import Admin


def get_admin() -> Admin:
    # return all the columns of the admin table
    return Admin.__repr__(Admin.query.first())
