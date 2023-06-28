from flask import Blueprint, render_template
from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index_page():
    psts = Post.query.all()
    return render_template('index.html', posts=psts)


@posts.route('/<url>')
def post_detail_page(url):
    post = Post.query.filter(Post.url == url).first()
    tags = post.tags
    if post:
        return render_template('post_detail.html', post=post, tags=tags)
    else:
        return render_template('page404.html'), 404


@posts.route('/tag/<url>')
def tag_detail_page(url):
    tag = Tag.query.filter(Tag.url == url).first()
    psts = tag.posts.all()
    return render_template('tag_detail.html', tag=tag, psts=psts)


