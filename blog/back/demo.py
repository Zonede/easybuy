from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/list2')
def list():
    return 'list'


@app.route('/detail')
def detail():
    return 'detail'


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8010,debug=True)