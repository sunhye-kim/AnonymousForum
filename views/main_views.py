from flask import Blueprint

test_api = Blueprint('main', __name__, url_prefix='/')

@test_api.route('/')
def test():
    return 'Hello'