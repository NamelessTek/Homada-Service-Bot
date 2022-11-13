from flask import Flask, request, current_app as app
from homada.models import Uploads
from homada import db
import os
import requests
import secrets


def get_upload(document: str) -> Uploads:
    '''
    Get upload data
    '''
    return Uploads.get_data(Uploads.query.filter_by(document=document).first())


def upload_document(file_name: str) -> Uploads:
    '''
    Create a new upload in DB
    '''

    # upload_url = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file_extension = os.path.splitext(file_name)
    file_fn = secrets.token_hex(8) + file_extension[1]
    upload_url = os.path.join(app.config['UPLOAD_FOLDER'], file_fn)
    # store the file in upload_url
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(upload_url)
    with open(file_name, 'rb') as f:
        with open(upload_url, 'wb') as f1:
            f1.write(f.read())

    db.session.add(
        Uploads(url=upload_url, file_name=file_name, document=file_fn))
    db.session.commit()
