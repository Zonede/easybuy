from flask import Flask, session
from flask_script import Manager
from flask_session import Session

from back.views import back_blueprint
from web.views import web_blueprint
from back.models import db
from flask import Blueprint
import redis



app=Flask(__name__)

app.register_blueprint(blueprint=back_blueprint,url_prefix='/back')
app.register_blueprint(blueprint=web_blueprint,url_prefix='/web')


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Justdoit886@127.0.0.1:3306/blog1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)


app.secret_key = 'Zsdfsrfe5t4wr312q423e'
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=redis.Redis(host='127.0.0.1',port=6379)
# sess = Session()
# sess.init_app(app)


if __name__ == '__main__':
    manage=Manager(app)
    manage.run()
