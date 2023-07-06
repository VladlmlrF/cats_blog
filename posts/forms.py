from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
# import email_validator


class PostForm(FlaskForm):
    title = StringField('title')
    body = TextAreaField('body')
    avatar = FileField('avatar')
    tags = StringField('tags')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Некорректный email')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField('Remember', default=False)
    login = SubmitField('Login')
    register = SubmitField('Register')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[Email('Некорректный email'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), Length(min=4, max=50),
                                                                   EqualTo('password', message='Пароли не совпадают')])
    register = SubmitField('Register')
