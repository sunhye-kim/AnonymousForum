
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from views import main_views, forum_api
    app.register_blueprint(main_views.test_api)
    app.register_blueprint(forum_api.forum_api)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

