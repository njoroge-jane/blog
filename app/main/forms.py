from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired


class PitchForm(FlaskForm):

    title = StringField('Pitch Title', validators=[InputRequired()])
    category = SelectField('Which category?', choices=[(
        1, 'Pickup'), (2, 'Products'), (3, 'Business')], validators=[InputRequired()])
    pitch = TextAreaField('Write your pitch', validators=[InputRequired()])
    submit = SubmitField('Post')


class CommentsForm(FlaskForm):
    comment = TextAreaField('Write your comment')
    submit = SubmitField('Submit')
