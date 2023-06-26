from flask import Flask, render_template
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404


from models import Post
admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
