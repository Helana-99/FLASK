
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from app.models import User, db

class PostForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 40)])
    image= FileField("Image")
    description = StringField("Description", validators=[Length(1, 40)])
    user_id = SelectField("user", validators=[DataRequired()], choices= [])
    submit = SubmitField("Save new Post")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.user_id.choices = [(t.id, f"{t.first_name} {t.last_name}") for t in User.query.all()]