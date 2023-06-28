from flask import Blueprint, render_template
from models import Post

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index_page():
    psts = Post.query.all()
    return render_template('index.html', posts=psts)


@posts.route('/<url>')
def post_detail_page(url):
    post = Post.query.filter(Post.url == url).first()
    # return render_template('post_detail.html', post=post)
    if post:
        return render_template('post_detail.html', post=post)
    else:
        return render_template('page404.html'), 404

