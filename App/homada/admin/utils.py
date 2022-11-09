from homada.models import Admin


def get_admin(admin: str) -> dict:
    # return all the columns of the admin table
    return Admin.get_data(Admin.query.filter_by(phone=admin).first())
