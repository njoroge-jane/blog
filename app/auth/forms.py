from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo
from ..models import Blogger
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators=[
                        InputRequired(), Email()])
    username = StringField('Enter your username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Passwords', validators=[
                                     InputRequired(), EqualTo('password', message='Passwords dont match')])
    submit = SubmitField('Sign Up')

    def validate_email(self, data_field):
        if Blogger.query.filter_by(email=data_field.data).first():
            raise ValidationError('That Email already exists')


class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators=[
                        InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[InputRequired()])
    submit = SubmitField('Submit')
