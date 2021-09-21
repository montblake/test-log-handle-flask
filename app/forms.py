from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SubmitNameForm(FlaskForm):
    actorname = StringField('Actor Name', validators=[DataRequired()])
    submit = SubmitField('Begin!')
