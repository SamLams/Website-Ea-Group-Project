from datetime import datetime
from hashlib import md5
from app import db, login
from flask import current_app
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('product.pid'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(120))
    delivery_addresses = db.relationship('Delivery_Address', backref='user')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    my_list = db.relationship('MyList', backref='user', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    cs = db.relationship('Customer_Services', backref='user')
    cart = db.relationship('Shopping_cart', backref='user')
    order = db.relationship('Order', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def followed_address(self):
        followed = Delivery_Address.query.join(
            followers, (followers.c.followed_id == Delivery_Address.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Delivery_Address.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Delivery_Address.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']

        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.reviews)


class MyList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))


class Delivery_Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(255))
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    mid = db.Column(db.Integer, db.ForeignKey('merchant.mid'), nullable=False)
    status = db.Column(db.String(255))
    cart = db.relationship('Shopping_cart', backref='product')
    link = db.Column(db.String(500))
    pc_id = db.Column(db.Integer, db.ForeignKey('category.pc_id'), nullable=False)
    ps_id = db.Column(db.Integer, db.ForeignKey('subcategory.ps_id'), nullable=False)
    pets = db.relationship('Pets', backref='Product', lazy=True)
    disney = db.relationship('Disney', backref='Product', lazy=True)
    SportsAndTravels = db.relationship('SportsAndTravel', backref='product', uselist=False)
    ToysAndBook = db.relationship('ToysAndBooks', backref='product', uselist=False)
    list = db.relationship('MyList', backref='product', lazy='dynamic')



    def unfollow(self, product):
        if self.is_following(product):
            self.followed.remove(product)

    def is_following(self, product):
        return self.followed.filter(
            followers.c.followed_id == product.pid).count() > 0


    def follow(self, product):
        if not self.is_following(product):
            self.followed.append(product)

    def __init__(self, pid, pname, qty, price, mid, status, pc_id, ps_id, link):
        self.pid = pid
        self.pname = pname
        self.qty = qty
        self.price = price
        self.mid = mid
        self.status = status
        self.pc_id = pc_id
        self.ps_id = ps_id
        self.link = link


class Category(db.Model):
    pc_id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(255))
    ps_id = db.Column(db.Integer, db.ForeignKey('subcategory.ps_id'), nullable=False)
    product = db.relationship('Product', backref='Category', lazy=True)

    def __init__(self, pc_id, pc_name, ps_id):
        self.pc_id = pc_id
        self.pc_name = pc_name
        self.ps_id = ps_id


class Subcategory(db.Model):
    ps_id = db.Column(db.Integer, primary_key=True)
    ps_name = db.Column(db.String(255))
    product = db.relationship('Product', backref='Subcategory', lazy=True)
    category = db.relationship('Category', backref='Subcategory', lazy=True)

    def __init__(self, ps_id, ps_name):
        self.ps_id = ps_id
        self.ps_name = ps_name


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    link = db.Column(db.String(120))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))


class Disney(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    link = db.Column(db.String(120))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))


class Merchant(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(255))
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    product = db.relationship('Product', backref='Merchant', lazy=True)

    def __init__(self, mid, mname, description, rating):
        self.mid = mid
        self.mname = mname
        self.description = description
        self.rating = rating


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'))
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.String(255), db.ForeignKey('status.status_id'))

    create_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    card = db.relationship('Payment', backref='card')

    def __repr__(self):
        return '<Order {}>'.format(self.order_id)


class Status(db.Model):
    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    shipment = db.Column(db.String(255))
    order_id = db.relationship('Order', backref='status')

    def __repr__(self):
        return '<Status {}>'.format(self.status_id)


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    card_number = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Payment {}>'.format(self.payment_id)


class Customer_Services(db.Model):
    services_id = db.Column(db.Integer, primary_key=True)
    services = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Services {}>'.format(self.services_id)


class Voucher(db.Model):
    v_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    expiary = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    discount = db.Column(db.Integer)

    def __repr__(self):
        return '<Voucher {}>'.format(self.v_id)


class Shopping_cart(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.relationship('Order', backref='shopping_cart')

    def __repr__(self):
        return '<Post {}>'.format(self.user_id)


class Housewares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    link = db.Column(db.String(255))
    price = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))

    def __repr__(self):
        return '<Housewares {}>'.format(self.id)


class SportsAndTravel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    link = db.Column(db.String(120))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))

    def __repr__(self):
        return '<SportsAndTravel {}>'.format(self.id)


class ToysAndBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    link = db.Column(db.String(120))
    product_id = db.Column(db.Integer, db.ForeignKey('product.pid'))

    def __repr__(self):
        return '<ToysAndBooks {}>'.format(self.id)
