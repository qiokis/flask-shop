from app import app, db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    picture = db.Column(db.String(255))

    def __repr__(self):
        return f"Category {self.name}"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    price = db.Column(db.Float)
    mark = db.Column(db.Float)

    def __repr__(self):
        return f"Product {self.name}"