import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, logout_user, current_user, login_user
from models import User
from app import db, login_manager
from profile.user_login import UserLogin
from .forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('profile.login_page'))


@profile.route('/')
@login_required
def profile_page():
    user_id = current_user.get_username()
    return render_template('profile.html', user_id=user_id)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id)


@profile.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile_page'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter(User.email == form.email.data).first()
        except sqlite3.Error as e:
            print('Пользователь не найден', e)

        if user and check_password_hash(user.password, form.password.data):
            user_log = UserLogin().create(user)
            in_memory = form.remember.data
            login_user(user_log, remember=in_memory)
            return redirect(request.args.get('next') or url_for('profile.profile_page'))
        else:
            print('Неверный логин или пароль')

    return render_template('login.html', form=form)


@profile.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        p_hash = generate_password_hash(form.password.data)
        try:
            user = User(name=form.name.data, email=form.email.data, password=p_hash)
            db.session.add(user)
            db.session.commit()
        except:
            print('User with the same name or email already exists')
        return redirect(url_for('profile.profile_page'))
    return render_template('register.html', form=form)


