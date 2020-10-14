from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, URL, NumberRange


class AddDribbbleTaskForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    amount_like = DecimalField(
        'Likes', validators=[DataRequired(), NumberRange(min=1, max=500)]
    )
    submit = SubmitField('Submit')


class AddFakePersonsForm(FlaskForm):
    amount_persons = DecimalField(
        'How much', validators=[DataRequired(), NumberRange(min=1, max=500)]
    )
    submit = SubmitField('Submit')

class DeleteTask(FlaskForm):
    submit = SubmitField('Delete')
