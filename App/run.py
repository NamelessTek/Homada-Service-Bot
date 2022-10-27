from email import message
from homada import create_app, db
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException
import traceback
from flask_admin import Admin
from homada.models import *
from flask_admin.contrib.sqla import ModelView


app = create_app()
admin = Admin(app)
admin.add_view(ModelView(Ubicacion, db.session))
# admin.add_view(ModelView(Client, db.session))
# admin.add_view(ModelView(Booking, db.session))
# for model in [Ubicacion, Client, Booking]:
#     admin.add_view(ModelView(model, db.session))


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    print("Error:", traceback.print_exc(), flush=True)
    # now you're handling non-HTTP exceptions only
    return {"error": True, "message": str(e)}, 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True,
            use_reloader=True, use_debugger=True)

# create a function that creates a modelview for each model
