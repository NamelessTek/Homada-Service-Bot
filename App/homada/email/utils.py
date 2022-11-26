from flask_mail import Message
from homada.config import Config
from homada import mail
from smtplib import SMTPException
from email.message import EmailMessage
import ssl
import smtplib


def send_email() -> None:
    em = EmailMessage()

    body = "Ya casi Luis, ya casi"

    mail = Config.MAIL_EMAIL
    em['From'] = mail
    em['To'] = "luisitocedillo@gmail.com"
    em['Subject'] = "Prueba de Mail"
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', Config.MAIL_PORT, context=context) as smtp:
        smtp.login(mail, Config.MAIL_PASSWORD)

        smtp.sendmail(mail,
                      "luisitocedillo@gmail.com", em.as_string())

    return "sent"

# def send_email() -> None:
#     """Send an email to the recipient."""
#     try:
#         msg = Message(
#             'Hello',
#             sender='namelessnoreply25@gmail.com',
#             recipients=['gomezrbz@gmail.com']
#         )
#         msg.body = '''Ya casi terminas Raul. Un paso mas y ya.
#     '''
#         mail.send(msg)
#         return 'sent'
#     except SMTPException:
#         logging.error("Failed to send email", exc_info=True)
