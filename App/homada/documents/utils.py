from flask import current_app as app
from homada.models import Uploads
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
    with open(upload_url, 'wb') as file:
        file.write(content)
    document = Uploads(url=upload_url,  document=file_fn)
    db.session.add(document)
    db.session.commit()

    create_log(document.__class__.__name__,
               document.id, 1, session['admin_id'])
