from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from app.models import User

class PostForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=40)])
    image = FileField("Image")
    description = StringField("Description", validators=[Length(max=500)])
    user_id = SelectField("User", validators=[DataRequired()], coerce=int, choices=[])
    submit = SubmitField("Save New Post")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, f"{u.username}") for u in User.query.all()]
