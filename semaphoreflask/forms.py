from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class CreateTaskForm(FlaskForm):
    task_title = StringField('Task Title', validators=[DataRequired()])
    task_description = TextAreaField('Task Description')
    task_submit = SubmitField('Create Task')