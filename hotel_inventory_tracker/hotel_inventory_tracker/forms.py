## forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ItemForm(FlaskForm):
    """
    Form for adding, updating items in the inventory.
    """
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, message='Quantity must be at least 1')])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01, message='Price must be at least 0.01')])
    submit = SubmitField('Submit')
