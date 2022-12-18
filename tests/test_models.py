from App.homada.models import Admin


def TestAdmin():
    '''Test admin creation'''
    # Create admin
    admin = Admin(phone='1234567890', name='admin', email='admin@mail.com')

    # Test that the 'get_data' method returns a dictionary
    data = admin.get_data()
    assert isinstance(data, dict)

    # Test that __str__ returns a string representation of the model
    string = str(admin)
    assert isinstance(string, str)
