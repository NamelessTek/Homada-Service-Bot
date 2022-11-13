from flask import Flask, request
from homada.models import Uploads
from homada import db
import os
import requests


def get_upload(document: str) -> Uploads:
    '''
    Get upload data
    '''
    return Uploads.get_data(Uploads.query.filter_by(document=document).first())


def upload_document(url: str, file_name: str, document: str) -> Uploads:
    '''
    Create a new upload in DB
    '''

    db.session.add(Uploads(url=url, file_name=file_name, document=document))
    db.session.commit()
