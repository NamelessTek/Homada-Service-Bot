from flask import Blueprint, request, jsonify
from homada.reservaciones.utils import *
from homada.twilio.utils import *
import pandas as pd

reservacion = Blueprint('reservacion', __name__)

@ reservacion.route('/data_loader_booking', methods=['GET', 'POST'])
def data_loader_booking():

    req_data = {}
    clean_headers = ['Casa Mirador', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9']
    headers = ["nombre_cliente", "telefono_cliente", "email_cliente", 
        "num_reservacion_cliente", "dia_llegada_cliente", "dia_salida_cliente", "ubicacion_cliente"]
    if 'file' not in request.files:
        message = {"success": False, "code": 1, "error": True,
                   "message": 'No data sent'}
        resp = jsonify(message)
        return resp
    else:
        files = request.files.keys()
        for fl in files:

            file = request.files[fl]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                message = {"success": False, "code": 2, "error": True,
                           "message": 'No file selected'}
                resp = jsonify(message)
                return resp
            if file:
                df = pd.read_excel(file)
                headers.sort()
                headers_df = list(df)
                headers_df.sort()
                for clean_header in clean_headers: headers_df.remove(clean_header)
                print(headers)
                print(headers_df)
                
                if headers == headers_df:
                    
                    for header in headers:
                        for index, row in df.iterrows():
                            # Obtain data and saving it in request data
                            print(row[header])
                            if not pd.isna(header):
                                req_data[header] = row[header]
                    
                    data = save_reservation_data_loader(req_data)
                    if data:
                        message = {
                            "success": True,
                            "code": 1,
                            "error": False,
                            "message": 'Bookings created successfully'
                        }
                        resp = jsonify(message)
                        return resp
                else:
                    message = {
                        "success": True,
                        "code": 3,
                        "error": False,
                        "message": 'Formato Incorrecto, los encabezados del archivo no son los correctos.'
                    }
                    resp = jsonify(message)
                    return resp