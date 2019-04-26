from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db=SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(10),unique=True,nullable=False)
    password=db.Column(db.String(225),nullable=False)
    is_delete=db.Column(db.Boolean,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now())


    __tablename__='user'

    def save(self):
        db.session.add(self)
        db.session.commit()


