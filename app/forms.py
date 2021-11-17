from wtforms import StringField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm


class UserLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class UserRegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password2 = StringField('password2', validators=[DataRequired(), EqualTo('password')])


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    picture = StringField('picture', validators=[DataRequired()])


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    picture = StringField('picture', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    mark = FloatField('mark', validators=[DataRequired()])