from . import db,login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255),unique= True,nullable=False)
    username =db.Column(db.String(255),unique =True,nullable=False)
    password_hash = db.Column(db.String())
    blog=db.relationship('Blog', backref='user', lazy='dynamic')
    comment=db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
        # print(check_password_hash,"eeeeeeeeeeeeee")
        
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()

    def __repr__ (self):
        return f'User{self.username}'
        
class Blog(db.Model):
    __tablename__ = 'blog'

    id=db.Column(db.Integer,primary_key=True)
    post= db.Column(db.String(255),nullable= False)
    title = db.Column(db.String(255),nullable= False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
    category= db.Column(db.String(255),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    comment=db.relationship('Comment', backref='blog',lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def __repr__ (self):
        return f'Blog{self.post}'

class Comment(db.Model):
    __tablename__ = 'comment'

    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(255),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'))

    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog_id):
        comments= Comment.query.filter_by(blod_id= blog_id).all()


    def __repr__(self):
        return f'Comment:{self.content}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)