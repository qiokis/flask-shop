from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    # 0 - default user, 1 - superuser (can create categories and products)
    role = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User>-Username:{self.username}-Email:{self.email}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_super(self):
        return True if self.role == 1 else False

    def get_cart_content(self):
        return Cart.query.filter_by(user_id=self.id).count()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    picture = db.Column(db.String(255))

    def __repr__(self):
        return f'<Category>-Name:{self.name}'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    price = db.Column(db.Float)
    mark = db.Column(db.Float)

    def __repr__(self):
        return f'<Product>-Name:{self.name}'


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f'<Cart>-UserID:{self.user_id}-ProductID:{self.product_id}-Quantity:{self.quantity}'
