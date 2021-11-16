from app import app, db
from app.models import Category, Product
from flask import render_template, request, redirect, url_for
from app.forms import CategoryForm, ProductForm


@app.route('/')
def index():

    return render_template('index.html', title='Test')


@app.route('/catalog')
def catalog():
    categories = Category.query.all()
    title = 'Catalog'
    # categories = [
    #     {'id': 1, 'name': 'Processors', 'picture': 'category_processors.jpg'},
    #     {'id': 2, 'name': 'Video cards', 'picture': 'category_videocards.jpg'}
    # ]
    new = {'fun': 'add_category', 'name': 'Добавить категорию'}
    return render_template('catalog.html', title=title, categories=categories, new=new)


@app.route('/catalog/<category_id>')
def products(category_id):
    prods = Product.query.filter_by(category_id=category_id)
    category = Category.query.filter_by(id=category_id).first()
    title = f'{category}'
    # prods = [
    #     {'id': 1, 'category_id': 1, 'name': 'Intel 12', 'picture': 'test.jpg'},
    #     {'id': 2, 'category_id': 2, 'name': 'Some Videocard', 'picture': 'product_some_videocart.jpg'}
    # ]
    new = {'fun': 'add_product', 'name': 'Добавить товар'}
    return render_template('products.html', prods=prods, new=new, category_id=category_id)


@app.route('/product/<product_id>')
def product(product_id):
    p = Product.query.filter_by(id=product_id).first()
    c = Category.query.filter_by(id=p.category_id).first()
    return render_template('product.html', prod=p, category_name=c.name)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        c = Category(name=form.name.data, picture=form.picture.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('add_category'))
    return render_template('add_category.html', form=form)


@app.route('/catalog/<category_id>/add_product', methods=['GET', 'POST'])
def add_product(category_id):
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
                           category_name=category_name)
