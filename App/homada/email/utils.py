from flask_mail import Mail, Message
from homada.config import Config
from homada import mail
from smtplib import SMTPException
import logging


def send_email(recipient: str) -> None:
    """Send an email to the recipient."""
    try:
        msg = Message(
            body="Hello",
            sender=Config.MAIL_EMAIL,
            recipients=[recipient],
            html="<h1>Testing</h1>",
        )
        mail.send(msg)
    except SMTPException:
        logging.error("Failed to send email", exc_info=True)
