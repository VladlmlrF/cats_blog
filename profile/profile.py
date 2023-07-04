from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.login_page'))


@profile.route('/')
@login_required
def profile_page():
    user_id = current_user.get_username()
    return render_template('profile.html', user_id=user_id)

