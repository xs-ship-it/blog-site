from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import Required,Email,EqualTo

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class UploadBlogForm(FlaskForm):
    title = TextAreaField('Blog',validators=[Required()])
    blog =  TextAreaField('Author',validators=[Required()])
    submit = SubmitField('Post')

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment',validators=[Required()])
    submit = SubmitField('Post')
