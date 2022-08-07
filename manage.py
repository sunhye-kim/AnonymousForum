
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from views import forum_views
    app.register_blueprint(forum_views.forum_app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()

