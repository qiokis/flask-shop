from wtforms import StringField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    picture = StringField('picture', validators=[DataRequired()])


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    picture = StringField('picture', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    mark = FloatField('mark', validators=[DataRequired()])