from flask import render_template,request,redirect,url_for,abort,flash
from ..request import get_quotes
from . import main
from flask_login import login_required,current_user
from ..models  import User, Blog, Comment
from .forms import UpdateProfile,UploadBlogForm,CommentsForm
from ..import db,photos

#Views
@main.route("/")
def index():
    '''
    View root page function that returns the index page and its data
    '''
    quotes = get_quotes()
    blog = Blog.query.filter_by().all()
    return render_template("index.html", quotes = quotes, blog = blog)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id=current_user.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, blogs = blogs)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>/upload_blog',methods = ['POST','GET'])
@login_required
def upload_blog(uname):
    user = User.query.filter_by(username = uname ).first()
    form = UploadBlogForm()
    if user is None:
        abort(404)

    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        user_id = current_user._get_current_object().id

        new_blog_object = Blog(title = title,blog = blog,user_id = user_id)
        new_blog_object.save_blog()

        return redirect(url_for('main.index'))
    return render_template('new_blog.html', form = form)

@main.route("/comment/<int:blog_id>",methods=["POST","GET"])
@login_required
def comment_blog(blog_id):
    form = CommentsForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.get_comments(blog_id)
    if form.validate_on_submit():
        new_comment = form.comment.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        comment_object = Comment(comment=new_comment,user_id=user_id,blog_id=blog_id)
        comment_object.save_comment()
        return redirect(url_for(".comment_blog",blog_id=blog_id))
    return render_template("comments.html",comment_form=form,blog=blog,all_comments=all_comments)

@main.route('/<int:blog_id>/update',methods=['GET','POST'])
@login_required
def update(blog_id):
    form=UploadBlogForm()
    blog=Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    if form.validate_on_submit():
        blog.title=form.title.data
        blog.blog=form.blog.data
        db.session.commit()
        flash('Successfully Updated!')
        return redirect(url_for('main.profile',uname=blog.user.username))
    elif request.method=='GET':
        form.title.data=blog.title
        form.blog.data=blog.blog

    return render_template('profile/update_blog.html',form=form,legend="Update Blog")

@main.route('/<int:blog_id>/delete',methods=['POST','GET'])
@login_required
def delete_blog(blog_id):
    blog=Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.profile',uname=blog.user.username))




