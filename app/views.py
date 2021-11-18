import os

from app import app, db
from app.models import Category, Product, User, Cart
from flask import render_template, request, redirect, url_for, flash
from app.forms import CategoryForm, ProductForm, UserRegistrationForm, UserLoginForm, CartForm
from app.utils import check_user_existence, allowed_file, generate_filename
from flask_login import current_user, login_required, login_user, logout_user



@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', title='Test')


@app.route('/catalog')
def catalog():
    title = 'Catalog'
    categories = Category.query.all()
    new = {'fun': 'add_category', 'name': 'Добавить категорию'}
    return render_template('catalog.html', title=title, categories=categories, new=new)


@app.route('/catalog/<int:category_id>')
def products(category_id):
    prods = Product.query.filter_by(category_id=category_id)
    category = Category.query.filter_by(id=category_id).first()
    title = f'{category}'
    new = {'fun': 'add_product', 'name': 'Добавить товар'}
    return render_template('products.html', prods=prods, new=new, category_id=category_id, title=title)


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    p = Product.query.filter_by(id=product_id).first()
    title = f'{p.name}'
    c = Category.query.filter_by(id=p.category_id).first()
    form = CartForm()
    if form.validate_on_submit():
        c = Cart.query.filter_by(user_id=current_user.id).filter_by(product_id=product_id).first()
        if c:
            c.quantity += form.quantity.data
        else:
            c = Cart(user_id=current_user.id, product_id=product_id, quantity=form.quantity.data)
            db.session.add(c)
        db.session.commit()
        return redirect(url_for('product', product_id=product_id))
    return render_template('product.html', prod=p, category_name=c.name, title=title, form=form)


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    title = 'Add category'
    form = CategoryForm()
    if form.validate_on_submit():
        c = Category(name=form.name.data)
        db.session.add(c)
        db.session.commit()
        filename = None
        if form.picture.data:
            filename = form.picture.data.filename
            if allowed_file(filename):
                filename, filepath = generate_filename(filename, c.id, 'category')
                form.picture.data.save(filepath)
        c.picture = filename
        db.session.commit()
        return redirect(url_for('add_category'))
    return render_template('add_category.html', form=form, title=title)


@app.route('/catalog/<int:category_id>/add_product', methods=['GET', 'POST'])
@login_required
def add_product(category_id):
    title = 'Add product'
    form = ProductForm()
    c = Category.query.filter_by(id=category_id).first()
    category_name = c.name
    if form.validate_on_submit():
        p = Product(category_id=category_id, name=form.name.data, description=form.description.data,
                    price=form.price.data, mark=form.mark.data)
        db.session.add(p)
        db.session.commit()
        filename = None
        if form.picture.data:
            filename = form.picture.data.filename
            if allowed_file(filename):
                filename, filepath = generate_filename(filename, p.id, 'product')
                form.picture.data.save(filepath)
        p.picture = filename
        db.session.commit()
        return redirect(url_for('add_product', category_id=category_id, category_name=category_name))
    return render_template('add_product.html', form=form, category_id=category_id,
                           category_name=category_name, title=title)


# TODO если какое то поле не проходит валидацию, то все поля сбрасываются
@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Registration'

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserRegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
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
        else:
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


@app.route('/about')
def about():
    pass


# # TODO Не используется
# @app.route('/add_to_cart/<int:product_id>')
# @login_required
# def add_to_cart(product_id):
#     cart = Cart(user_id=current_user.id, product_id=product_id)
#     db.session.add(cart)
#     db.session.commit()
#     return redirect(url_for('product', product_id=product_id))


@app.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id)
    item_list = list()
    for c in cart:
        item_list.append({'product': Product.query.get(c.product_id), 'quantity': c.quantity})
    return render_template('cart.html', items=item_list)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(name=form.name.data)
        db.session.add(p)
        db.session.commit()
        filename = None
        if form.picture.data:
            filename = form.picture.data.filename
            if allowed_file(filename):
                filename, filepath = generate_filename(filename, p.id, 'post')
                form.picture.data.save(filepath)
        p.picture = filename
        db.session.commit()
        return redirect(url_for('add_post'))
    return render_template('add_post.html', form=form)

