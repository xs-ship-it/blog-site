from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required


class CommentForm(FlaskForm):
    content=TextAreaField('comment on blog', validators=[Required()])
    submit=SubmitField('comment')

class BlogForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    category = SelectField('Category',choices=[('Technology','Technology'),('Music','Music'),('Sports','Sports')],validators = [Required()])
    post = TextAreaField('Your blog', validators = [Required()])
    submit = SubmitField('share your blog')