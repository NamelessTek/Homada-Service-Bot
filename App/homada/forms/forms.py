from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField, DateField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dataclasses import dataclass


@dataclass
class RegistrationForm(FlaskForm):
    username: str = StringField('Username', validators=[
                                DataRequired(), Length(min=2, max=20)])
    email: str = StringField('Email', validators=[DataRequired(), Email()])
    password: str = PasswordField('Password', validators=[DataRequired()])
    confirm_password: str = PasswordField(
        'Confirm Password', validators=[EqualTo('password')])
    submit: str = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError(
    #             'That username is taken. Please choose a different one.')


@dataclass
class LoginForm(FlaskForm):
    email: str = StringField('Email', validators=[DataRequired(), Email()])
    password: str = PasswordField('Password', validators=[DataRequired()])
    remember: str = BooleanField('Remember Me')
    submit: str = SubmitField('Login')


@dataclass
class CreateBooking(FlaskForm):
    booking_number: int = StringField('Booking Number', validators=[
        DataRequired()])
    # validate that cliend_id exists in the database
