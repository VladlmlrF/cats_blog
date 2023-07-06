import sqlite3

from app import db
from datetime import datetime
import re


def generate_url(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


def get_user(user_id):
    try:
        user = User.query.filter(User.id == user_id).first()
        return user
    except sqlite3.Error as e:
        print('Ошибка получения данных из БД', e)
    print('Пользователь не найден')
    return False


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    avatar = db.Column(db.BLOB, default=None)
    url = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.url = generate_url(self.title)

    def __repr__(self):
        return f'Post id: {self.id}, title: {self.title}'


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String, unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.url = generate_url(self.title)

    def __repr__(self):
        return f'Tag id: {self.id}, title: {self.title}'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'User {self.name}, user id: {self.id}'
