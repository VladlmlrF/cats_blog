from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Некорректный email')])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField('Запомнить', default=False)
    login = SubmitField('Войти')
    register = SubmitField('Регистрация')


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[Email('Некорректный email'), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=50)])
    repeat_password = PasswordField('Повторить пароль', validators=[DataRequired(), Length(min=4, max=50),
                                                                   EqualTo('password', message='Пароли не совпадают')])
    register = SubmitField('Регистрация')
