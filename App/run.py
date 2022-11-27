from email import message
from homada import create_app, db
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException
import traceback
from flask_admin import Admin
from homada.models import Ubicacion, Booking, Client, Questions
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView


app = create_app()
admin = Admin(app)

class ModifiedView(ModelView):
    form_excluded_columns = ['bookings',
                             'creation_date', 'last_update', 'status']
    can_export = True
    can_view_details = True


VIEWS = [admin.add_view(ModifiedView(model, db.session))
         for model in [Ubicacion, Booking, Client, Questions]]


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    print("Error:", traceback.print_exc(), flush=True)
    # now you're handling non-HTTP exceptions only
    return {"error": True, "message": str(e)}, 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True,
            use_reloader=True, use_debugger=True)
