from models import get_user
from flask_login import UserMixin


class UserLogin(UserMixin):
    def from_db(self, user_id):
        self.us = get_user(user_id)
        return self

    def create(self, user):
        self.us = user
        return self

    def get_id(self):
        return str(self.us.id)

    def get_username(self):
        return self.us.name

    def get_user_email(self):
        return self.us.email
