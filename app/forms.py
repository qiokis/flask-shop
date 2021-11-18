from wtforms import StringField, TextAreaField, IntegerField, FloatField, FileField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, regexp, InputRequired, StopValidation, NumberRange
from flask_wtf import FlaskForm
import re


class UserLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class UserRegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password')])


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired()])


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    mark = FloatField('mark', validators=[DataRequired()])


class CartForm(FlaskForm):
    quantity = IntegerField('quantity', default=1, validators=[InputRequired(), NumberRange(min=1)])