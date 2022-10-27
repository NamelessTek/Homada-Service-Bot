from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from homada.twilio.utils import *
from homada.clientes.utils import *
from homada.models import *


client = Blueprint('client', __name__)
