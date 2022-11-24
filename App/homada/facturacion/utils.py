from flask import current_app as app
from homada.models import Uploads, Questions, Booking
from homada.tools.utils import delete_session, delete_session_completly
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


def flow_facturacion(incoming_message: str) -> str:

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
            case _:
                pass

        if 'question_id' in session:
            del session['question_id']
        messages.append(
            f'¿Estás seguro que deseas subir el documento {session["document"]}?')

    elif 'review_upload' in session:
        if incoming_message == 'si':
            upload_document(session['document'].replace(
                ' ', '_'), session['content'])
            # send_email("luisitocedillo@gmail.com")
            messages.append(f'Gracias por subir tu factura')
            delete_session_completly()
        elif incoming_message == 'no':
            messages.append('Documento no subido')
    else:
        delete_session()
        question = Questions.query.filter_by(
            id=9, type_question="Upload").first()
        messages.append(question.question)
        session['question_id'] = question.id
    session['factura'] = True
    return messages
