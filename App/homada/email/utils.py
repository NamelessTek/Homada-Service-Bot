from flask import current_app as app
from flask_mail import Message
from homada.config import Config
from homada.models import Client, Booking, Ubicacion
from homada import mail
from smtplib import SMTPException
from email.message import EmailMessage
from email.mime.text import MIMEText
from flask import session
import ssl
import smtplib
import os


def send_email(booking: str, email: str) -> None:
    '''
    Send email to client with the booking, it attaches the last pdf generated
    '''
    mail = EmailMessage()
    client = booking.client
    ubicacion = booking.ubicacion
    mail['From'] = Config.MAIL_EMAIL
    #mail['To'] = email
    mail['To'] = "gomezrbz@gmail.com"
    mail['Subject'] = f'''Factura de número de reservación {booking.booking_number}'''
    mail.add_header('Content-Type', 'text/html',)

    html = (f'''
    <html>
    <head>
    <style>


    
    table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }}

    td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }}

    tr:nth-child(even) {{
        background-color: #dddddd;
    }}
    </style>
    </head>
    <body>

    <h2>Hola equipo Homada!</h2>

    El cliente {client.name} con el número de reservación {booking.booking_number} ha solicitado su factura. Te anexamos su constancia fiscal, y este es su contacto.

    <table>
        <tr>
            <th>Nombre</th>
            <th>Correo electrónico</th>
            <th>Teléfono</th>
            <th>Ubicación</th>
        </tr>
        <tr>
            <td>{client.name}</td>
            <td>{client.email}</td>
            <td>{client.phone}</td>
            <td>{ubicacion.ubicacion}</td>
        </tr>
    </table>

    </body>
    </html>''')
    mail.set_payload(html)

    upload_url = os.path.join(
        app.config['UPLOAD_FOLDER'], session['constancia'])
    name_file = f"Constancia_Fiscal_{str(booking.booking_number)}.pdf"
    mail.add_attachment(open(upload_url, 'rb').read(), maintype='application',
                        subtype='octet-stream', filename=name_file)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', Config.MAIL_PORT, context=ssl.create_default_context()) as smtp:
            smtp.login(mail['From'], Config.MAIL_PASSWORD)
            smtp.sendmail(mail['From'], mail['To'],
                          mail.as_string().encode('utf-8'))
            smtp.quit()

        print('Email sent!')
    except SMTPException as e:
        print('Error sending email: ', e)
