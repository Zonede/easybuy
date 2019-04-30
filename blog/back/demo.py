from flask import Flask
from flask import Blueprint

app = Flask(__name__)
blue=Blueprint('blue',__name__)
app.register_blueprint(blueprint=blue,url_prefix='/blue')

@blue.route('/')
def index():
    return 'index'


@blue.route('/list2')
def list():
    return 'list'


@blue.route('/detail')
def detail():
    return 'detail'


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8010,debug=True)