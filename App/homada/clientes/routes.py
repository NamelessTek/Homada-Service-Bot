from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from homada.twilio.utils import *
from homada.clientes.utils import *
from homada.models import *


client = Blueprint('client', __name__)


@client.route('/home', methods=['GET', 'POST'])
def homepage():
    data_client = Client.query.filter_by(id=1).first()
    return render_template('home.html', data_client=data_client)


@client.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
