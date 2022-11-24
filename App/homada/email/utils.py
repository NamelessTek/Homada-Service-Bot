from flask_mail import Mail, Message
from homada.config import Config
from homada import mail
from smtplib import SMTPException
import logging


def send_email(recipient: str) -> None:
    """Send an email to the recipient."""
    try:
        msg = Message(
            'Hello',
            sender='namelessnoreply25@gmail.com',
            recipients='gomezrbz@gmail.com'
        )
        msg.body='''Ya casi terminas Raul. Un paso mas y ya.
    '''
        mail.send(msg)
    except SMTPException:
        logging.error("Failed to send email", exc_info=True)
