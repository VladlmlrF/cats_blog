from models import get_user


class UserLogin:
    def from_db(self, user_id):
        self.us = get_user(user_id)
        return self

    def create(self, user):
        self.us = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.us.id)
