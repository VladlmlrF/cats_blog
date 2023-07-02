from flask import Blueprint, render_template, request, redirect, url_for
from models import Post, Tag, post_tags, User
from app import db
from .forms import PostForm
from werkzeug.security import check_password_hash, generate_password_hash

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['GET', 'POST'])
def create_post_page():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tags = request.form.get('tags').split(' ')

        if title:
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                all_tags = []

                db_tags = Tag.query.all()
                db_tags_titles = []
                for db_tag in db_tags:
                    db_tags_titles.append(db_tag.title)

                for t in tags:
                    if t in db_tags_titles:
                        all_tags.append(Tag.query.filter(Tag.title == t).first())
                    else:
                        tag = Tag(title=t)
                        db.session.add(tag)
                        all_tags.append(tag)

                post.tags = all_tags
                db.session.commit()
            except:
                print('Something wrong')

        return redirect(url_for('posts.index_page'))

    form = PostForm()
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


@posts.route('/login')
def login_page():
    return render_template('login.html')


@posts.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if len(name) > 4 and len(email) > 4 and len(password) > 4 and password2 == password:
            p_hash = generate_password_hash(request.form.get('password'))
            try:
                user = User(name=name, email=email, password=p_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('posts.login_page'))
            except:
                print('User with the same name already exists')
        else:
            print('Неверно заполнены поля')
    return render_template('register.html')
