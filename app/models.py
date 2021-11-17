from datetime import datetime,timezone
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from . import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Quote:
    """
    Quote class to define Quote Objects"""
    def __init__(self,id,author,quote):
        self.id = id
        self.author = author
        self.quote = quote

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String(255))
    email = db.Column(db.String(255))
    bio=db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    comment=db.relationship('Comment',backref='user',lazy='dynamic')
    blog=db.relationship('Blog',backref='user',lazy='dynamic')
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__='blog'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column (db.String(255))
    blog=db.Column(db.String(255))
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
       return f'blog {self.title}'

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id=db.Column(db.Integer,db.ForeignKey('blog.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
       return f'Comment{self.comment}'
    @classmethod
    def get_comments(cls,id):
        comment=Comment.query.filter_by(blog_id=id).all()
        return comment



