from http import client
from flask import Blueprint, request, jsonify
from homada.ubicacion.utils import *
from homada.twilio.utils import *
from homada.ubicacion.utils import *

client = Blueprint('client', __name__)
