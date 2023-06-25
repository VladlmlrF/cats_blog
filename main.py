from app import app
from posts.blueprint import posts


app.register_blueprint(posts)


if __name__ == '__main__':
    app.run(debug=True)
