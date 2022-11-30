from flask import current_app as app
from homada.models import Uploads, Questions, Booking, Client
from homada.tools.utils import delete_session, delete_session_completly, validate_email
from homada.email.utils import send_email
from homada import db
from homada.log.utils import create_log
from flask import session, request
import os
import secrets
import requests


def get_upload(document: str) -> Uploads:
    '''
    Get upload data
    '''
    return Uploads.get_data(Uploads.query.filter_by(document=document).first())


def upload_document(file_name: str, content: bytes) -> Uploads:
    '''
    Create a new upload in DB passing the final file name and the content
    '''

    file_extension = os.path.splitext(file_name)
    file_fn = secrets.token_hex(8) + file_extension[1]
    upload_url = os.path.join(app.config['UPLOAD_FOLDER'], file_fn)
    # Save file in the server
    with open(upload_url, 'wb') as file:
        file.write(content)
    document = Uploads(url=upload_url,  document=file_fn)
    db.session.add(document)
    db.session.commit()
    session['constancia'] = str(file_fn)
    # Create a Log in DB
    create_log(document.__class__.__name__,
               document.id, 1, session['admin_id']) if session.get('admin_id') else None

    relationship_booking_document(getattr(Booking.query.filter_by(
        cliente_id=session['client_id']).first(), 'id', None), document.id)


def relationship_booking_document(booking_id: int, document_id: int) -> None:
    '''
    Create a new relationship between booking and document in DB passing the booking id and the document id
    '''
    booking = Booking.query.filter_by(id=booking_id).first()
    document = Uploads.query.filter_by(id=document_id).first()

    if booking and document:
        document.booking_id.append(booking)
        db.session.commit()
    else:
        raise Exception(
            'Could not create relationship between booking and document')


def flow_facturacion(incoming_message: str, booking) -> str:

    messages: list[str] = []
    if 'question_id' in session:
        match session['question_id']:
            case 9:
                media_url = request.form.get('MediaUrl0', None)
                if media_url:
                    r = requests.get(media_url)
                    content_type = r.headers['content-type']
                    if content_type == 'application/pdf':
                        session['document'] = r.headers['content-disposition'].split('=')[
                            1].replace('"', '').replace('+', ' ').replace('%3F', '')
                        session['content'] = r.content
                        session['review_upload'] = True
                    else:
                        messages.append(
                            f'Lo sentimos, no pudimos recibir tu factura, solo se aceptan archivos en formato PDF 😟')
                        messages.append(
                            Questions.query.filter_by(id=9, type_question="Factura").first().question)
                        return messages
                else:
                    messages.append(
                        f'Lo sentimos, no pudimos recibir tu factura 😟')
            case 10:
                if validate_email(incoming_message):
                    session['email_cliente'] = incoming_message
                    print(session['email_cliente'])
                    session['review_client_email'] = True
                else:
                    messages.append("El correo electrónico no es válido 😟")
                    messages.append(
                        Questions.query.filter_by(id=10, type_question="Factura").first().question)
                    return messages
            case _:
                delete_session_completly()

        if 'question_id' in session:
            del session['question_id']

        if session.get('review_upload'):
            messages.append(
                f'¿Estás seguro que deseas subir el documento {session["document"]}? si/no')
        if session.get('review_client_email'):
            messages.append(
                f'¿Estás seguro que deseas subir el documento {session["email_cliente"]}? si/no')

    elif 'review_upload' in session and session['review_upload']:
        if incoming_message == 'si':
            session['review_client_email'] = True
            session['review_upload'] = False
            messages.append(
                f'Se enviará la factura con el correo {getattr(Client.query.filter_by(id=session["client_id"]).first(), "email", None)}, ¿es correcto? si/no')
        elif incoming_message == 'no':
            messages.append('Documento no subido')
            delete_session_completly()
        else:
            messages.append(
                f'De acuerdo, en caso de necesitar ayuda escribe la palabra menú')
            delete_session_completly()
    elif 'review_client_email' in session and session['review_client_email']:
        if incoming_message == 'si':
            confirmed_doc(messages)
            send_email(booking, getattr(Client.query.filter_by(
                id=session["client_id"]).first(), "email", None))
            delete_session_completly()
        elif incoming_message == 'no':
            messages.append(Questions.query.filter_by(
                id=10, type_question="Factura").first().question)
            session['question_id'] = 10
            session['review_client_email'] = False
            return messages
        else:
            messages.append(
                f'Lo sentimos, no pudimos recibir tu constancia fiscal 😟.')
            delete_session_completly()

    else:
        delete_session()
        initialize_facturacion(messages)
    return messages


def confirmed_doc(messages: str) -> None:
    upload_document(session['document'], session['content'])
    messages.append(
        'Muchas gracias, tu información ha sido recibida y nos pondremos en contacto contigo 😊👌')


def initialize_facturacion(messages: str) -> None:
    question = getattr(Questions.query.filter_by(
        id=9, type_question="Factura").first(), 'question', None)
    session['question_id'] = 9
    messages.append(question)
    session['factura'] = True
