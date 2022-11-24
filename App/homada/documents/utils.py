from flask import current_app as app
from homada.models import Uploads, Client
from homada import db
from homada.log.utils import create_log
from flask import session
import os
import secrets


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

    # Create Relationship between Client and Document
    relationship_client_document(session['client_id'], document.id)


def relationship_client_document(client_id: int, document_id: int) -> None:
    '''
    Create a new relationship between client and document in DB passing the client id and the document id
    '''
    client = Client.query.filter_by(id=client_id).first()
    document = Uploads.query.filter_by(id=document_id).first()

    if client and document:
        document.cliente_id.append(client)
        db.session.commit()
    else:
        raise Exception(
            'Could not create relationship between client and document')
