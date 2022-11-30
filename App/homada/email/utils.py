from flask import current_app as app
from flask_mail import Message
from homada.config import Config
from homada.models import Client, Booking, Ubicacion
from homada import mail
from smtplib import SMTPException
from email.message import EmailMessage
from flask import session
import ssl
import smtplib
import os


def send_email(booking) -> None:
    em = EmailMessage()
    client = booking.client
    ubicacion = booking.ubicacion
    body = f''' Hola equipo Homada!

El cliente {client.name} con el número de reservación {booking.booking_number} ha solicitado su factura. Te anexamos su constancia fiscal, y este es su contacto.

Nombre {client.name}
Número de reservación {booking.booking_number}
Teléfono {client.phone}
Email {client.email}
Ubicación {ubicacion.ubicacion}


Saludos
    '''
    print('Ruta!!')
    file_fn = session['constancia']
    print(file_fn)
    upload_url = os.path.join(app.config['UPLOAD_FOLDER'], file_fn)
    print(upload_url)
    name_file = "Constancia_Fiscal_"+str({booking.booking_number})+".pdf"
    with open(upload_url, 'rb') as content_file:
        content = content_file.read()
        em.add_attachment(content, maintype='application', subtype='pdf', filename=name_file)
    
    mail = Config.MAIL_EMAIL
    em['From'] = mail
    em['To'] = "gomezrbz@gmail.com"
    em['Subject'] = f'''Factura de número de reservación {booking.booking_number}'''
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', Config.MAIL_PORT, context=context) as smtp:
        smtp.login(mail, Config.MAIL_PASSWORD)

        smtp.sendmail(mail,
                      "gomezrbz@gmail.com", em.as_string())

    return "sent"