from homada.models import Booking


def get_booking(booking: Booking) -> dict:
    '''
    Get booking data
    '''
    return {key: value for key, value in Booking.__repr__(booking).items() if booking.status and value != []}
