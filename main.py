from app import app
from posts.posts import posts
from profile.profile import profile


app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(profile, url_prefix='/profile')


if __name__ == '__main__':
    app.run()
