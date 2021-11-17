from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Blog
from .. import db
from .form import BlogForm,CommentForm



@main.route('/')
def index():
    blog = Blog.query.all()
    technology = Blog.query.filter_by(category='Technology').all
    sports=Blog.query.filter_by(category='Sports').all
    music=Blog.query.filter_by(category='Music').all
    
    return render_template('index.html', technology=technology,music=music,blog=blog,sports=sports)


@main.route('/blog',methods=['GET','POST'])
@login_required
def new_blog():
    form=BlogForm()
    if form.validate_on_submit():
        title=form.title.data
        category=form.category.data
        post=form.post.data
        user_id=current_user
        
        new_blog_object = Blog(post=post,title=title,category=category,user_id=current_user._get_current_object().id)
        new_blog_object.save_blog()
        return redirect(url_for('main.index'))
    return render_template('blog.html', form=form)



@main.route('/comment/<int:blog_id>', methods=['GET','POST'])
@login_required
def comment(blog_id):
    form=CommentForm()
    blog= Blog.query.get(blog_id)
    all_comments=Comment.query.filter_by(blog_id=blog_id).all()
    if form.validate_on_submit():
        comment=form.content.data
        blog_id=blog_id
        user_id = current_user._get_current_object().id
        new_comment= Comment(comment=comment,user_id=user_id,blog_id=blog_id)
        new_comment.save_comment()
        return redirect(url_for('.comment',blog_id=blog_id))
    return render_template('comment.html',form=form,blog=blog,all_comments=all_comments)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    posts = Blog.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
