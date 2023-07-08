import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, make_response

import app
from models import Post, Tag, post_tags, User
from app import db, login_manager
from .forms import PostForm, LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from user_login import UserLogin
from flask_login import login_user, login_required, current_user

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post_page():
    form = PostForm()
    if form.validate_on_submit():
        try:
            f = form.avatar.data.read()
            post = Post(title=form.title.data, body=form.body.data, avatar=f)
            db.session.add(post)
            all_tags = []

            db_tags = Tag.query.all()
            db_tags_titles = []
            for db_tag in db_tags:
                db_tags_titles.append(db_tag.title)

            for t in form.tags.data.split(' '):
                if t in db_tags_titles:
                    all_tags.append(Tag.query.filter(Tag.title == t).first())
                else:
                    tag = Tag(title=t)
                    db.session.add(tag)
                    all_tags.append(tag)

            post.tags = all_tags
            db.session.commit()
        except sqlite3.Error as e:
            print('Something wrong', e)
        return redirect(url_for('posts.index_page'))
    return render_template('create_post_page.html', form=form)


@posts.route('/')
def index_page():
    q = request.args.get('q')
    if q:
        psts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        psts = Post.query.all()
    return render_template('index.html', posts=psts)


@posts.route('/<url>')
@login_required
def post_detail_page(url):
        post = Post.query.filter(Post.url == url).first()
        tags = post.tags
        return render_template('post_detail.html', post=post, tags=tags)

@posts.route('/post_avatar/<url>')
def get_post_avatar(url):
    post: Post = Post.query.filter(Post.url == url).first()
    avatar = post.get_avatar(posts)
    img = make_response(avatar)
    img.headers['Content-Type'] = 'image/jpg'
    return img


@posts.route('/tag/<url>')
def tag_detail_page(url):
    tag = Tag.query.filter(Tag.url == url).first()
    psts = tag.posts.all()
    return render_template('tag_detail.html', tag=tag, psts=psts)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id)


@posts.route('/login', methods=['GET', 'POST'])
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


@posts.route('/register', methods=['GET', 'POST'])
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
