from flask import Blueprint, request, jsonify, render_template
from homada.forms.forms import RegistrationForm, LoginForm
from homada.models import *

user = Blueprint('user', __name__)


@user.route('/', methods=['GET', 'POST'])
def status():
    # get status of the app
    message = {
        'status': 'ok',
        'message': 'App is running',
        'port': 5555,
        'app': 'homada'
    }
    return jsonify(message), 200


@user.route('/home', methods=['GET', 'POST'])
def homepage():
    data_client = Client.query.filter_by(id=1).first()
    return render_template('home.html', data_client=data_client)


@user.route('/register')
def register_endpoint():
    """
    Register an User in DB
    """
    form = RegistrationForm()
    return render_template('register.html', form=form, title='Register')


@user.route('/login', methods=['GET'])
def login_endpoint():
    """
    Register an User in DB
    """
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form, title='Login')
