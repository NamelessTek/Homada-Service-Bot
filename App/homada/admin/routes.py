from flask import Blueprint, request, jsonify, render_template
from homada.models import *
from homada.tools.utils import *
import socket
import datetime
from uptime import uptime
import psutil

admin_homada = Blueprint('admin_homada', __name__)


@admin_homada.route('/health', methods=['GET', 'POST'])
def health():
    '''
    Check if the server is up
    status: OK, SLOW, CRITICAL
    memory_usage: percentage of memory usage
    cpu_usage: percentage of cpu usage
    port: port where the server is running
    message: Server is up and running
    '''
    cpu = psutil.cpu_percent()
    return jsonify({
        "status": f"{server_status()}",
        "memory_usage": f"{getattr(psutil.virtual_memory(), 'percent')}%",
        "cpu_usage": f"{cpu}%",
        "port": 5555,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": f"{uptime() / 60 / 60 / 24:.2f} days",
        "message": "Server is up and running",
    })
