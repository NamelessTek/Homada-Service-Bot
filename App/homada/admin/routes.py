from flask import Blueprint, request, jsonify, render_template
from homada.models import *
import socket
import datetime
from uptime import uptime

admin_homada = Blueprint('admin_homada', __name__)


@admin_homada.route('/readyz', methods=['GET', 'POST'])
def readyz():
    data = {}
    data['status']="oks"
    data['hostname']=socket.gethostname()
    data['uptime']=uptime()
    data['date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resp = jsonify(data)
    return resp
