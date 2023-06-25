from flask import Blueprint, render_template
from models import Post

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index_page():
    psts = Post.query.all()
    return render_template('index.html', posts=psts)
