from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    avatar = FileField('Avatar', validators=[FileRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    create = SubmitField('Create')
