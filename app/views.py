from app import app, db, login_manager
from app.models import Category, Product, User
from flask import render_template, request, redirect, url_for, flash
from app.forms import CategoryForm, ProductForm, UserRegistrationForm, UserLoginForm
from app.utils import check_user_existence
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    return render_template('index.html', title='Test')


@app.route('/catalog')
def catalog():
    title = 'Catalog'
    categories = Category.query.all()
    new = {'fun': 'add_category', 'name': 'Добавить категорию'}
    return render_template('catalog.html', title=title, categories=categories, new=new)


@app.route('/catalog/<category_id>')
def products(category_id):
    prods = Product.query.filter_by(category_id=category_id)
    category = Category.query.filter_by(id=category_id).first()
    title = f'{category}'
    new = {'fun': 'add_product', 'name': 'Добавить товар'}
    return render_template('products.html', prods=prods, new=new, category_id=category_id, title=title)


@app.route('/product/<product_id>')
def product(product_id):
    p = Product.query.filter_by(id=product_id).first()
    title = f'{p.name}'
    c = Category.query.filter_by(id=p.category_id).first()
    return render_template('product.html', prod=p, category_name=c.name, title=title)


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    title = 'Add category'
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        c = Category(name=form.name.data, picture=form.picture.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('add_category'))
    return render_template('add_category.html', form=form, title=title)


@app.route('/catalog/<category_id>/add_product', methods=['GET', 'POST'])
@login_required
def add_product(category_id):
    title = 'Add product'
    form = ProductForm(request.form)
    c = Category.query.filter_by(id=category_id).first()
    category_name = c.name
    if request.method == 'POST' and form.validate_on_submit():
        p = Product(category_id=category_id, name=form.name.data, description=form.description.data,
                    picture=form.picture.data, price=form.price.data, mark=form.mark.data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('add_product', category_id=category_id, category_name=category_name))
    return render_template('add_product.html', form=form, category_id=category_id,
                           category_name=category_name, title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Registration'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        access = True
        if check_user_existence(username=form.username.data):
            flash('Username is already taken')
            access = False
        if check_user_existence(email=form.email.data):
            flash('Email is already taken')
            access = False
        if access:
            user = User(name=form.name.data, surname=form.surname.data, username=form.username.data,
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You have been successfully registered')
            return redirect(url_for('register'))
    return render_template('register.html', form=form, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('User does not exist')
            return redirect(url_for('login'))
        access = user.check_password(form.password.data)
        if not access:
            flash('Wrong password or username')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

