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

class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_name = db.Column(db.String(20),unique=True)
    arts = db.relationship('Article',backref='category')

class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),unique=True)
    content = db.Column(db.Text,nullable=False)
    desc = db.Column(db.String(100),nullable=False)
    type = db.Column(db.Integer,db.ForeignKey('category.id'))



    def save(user):
        db.session.add(user)
        db.session.commit()


