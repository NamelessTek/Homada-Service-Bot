from homada.models import Ubicacion, Booking, Client
from flask_admin.contrib.sqla import ModelView
from homada import db
from homada.forms.forms import *
from wtforms import FileField, SubmitField, TextAreaField, StringField, SelectField, IntegerField, DateField, TimeField, validators


class BookingView(ModelView):
    form_excluded_columns = ['creation_date', 'last_update', 'status']
    column_exclude_list = ['creation_date', 'last_update']


class UbicacionView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = [column.name for column in Ubicacion.__table__.columns if column.name !=
                   'creation_date' and column.name != 'last_update' and column.name != 'id']
    column_list = [column for column in column_list]
    ['bookings', Ubicacion.bookings]
    column_searchable_list = [column for column in column_list]
    column_filters = [column for column in column_list]
    column_editable_list = [column for column in column_list]
    column_sortable_list = [column for column in column_list]
    column_default_sort = ('id', True)

    can_export = True
    can_view_details = True
    can_set_page_size = True

    form_columns = [column for column in column_list]
    form_overrides = {
    }
