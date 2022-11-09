from homada.models import Admin


def get_admin(admin: str) -> dict:
    # return all the columns of the admin table
    return Admin.__repr__(Admin.query.filter_by(phone=admin).first())

def get_admin_phones( ) -> list:
    # return phones of all admins
    phones = []
    admins = Admin.query.all()
    for admin in admins:
        phones.append(admin.phone)
    return phones