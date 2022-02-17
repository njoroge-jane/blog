from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired


class BlogForm(FlaskForm):

    title = StringField('Blog Title', validators=[InputRequired()])
    blog = TextAreaField('Write your opinion', validators=[InputRequired()])
    submit = SubmitField('Post')


class CommentsForm(FlaskForm):
    comment = TextAreaField('Write your comment')
    submit = SubmitField('Submit')

class SubscriptionForm(FlaskForm):

    username = StringField('Your Name', validators=[InputRequired()])
    email = TextAreaField('Email', validators=[InputRequired()])
    submit = SubmitField('Submit')

