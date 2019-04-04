from dependency import db
from dotenv import load_dotenv
import os


# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # public_id will be put inside the token and prevent bad user supply the previous or next user
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return "<User {}: {}>".format(self.id, self.user_name)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # represent the actual to do text
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return "<Todo {}: {}: {}>".format(self.user_id, self.text, self.complete)


# productsCarts = db.Table('products_carts',
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
#     db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True)
# )
#
# usersProducts = db.Table('users_products',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
# )


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     cart = db.relationship('Cart', backref='user', uselist=False)    # one to one relation
#     products = db.relationship('Product', backref='users', lazy='subquery', secondary=usersProducts)
#
#     def __repr__(self):
#         return "<User {}: {}>".format(self.id, self.user_name)


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String, nullable=False)
#     product_price = db.Column(db.Integer, nullable=False)
#     carts = db.relationship('Cart', backref='products', lazy='subquery', secondary=productsCarts)
#
#     def __repr__(self):
#         return "<Product {}: {}: {}>".format(self.id, self.product_name, self.product_price)
#
#
# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return "<Cart {}: {}: {}: {}>".format(self.id, self.user_id, self.product.id, self.quantity)




