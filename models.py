from app import db
from datetime import datetime
import re


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_name()

    def __repr__(self):
        return f'Post id: {self.id}, title: {self.title}'

    def generate_name(self):
        if self.title:
            pattern = r'[^\w+]'
            self.name = re.sub(pattern, '-', self.title)
            return self.name
