from datetime import datetime
from hashlib import md5
from app import db, login
from flask import current_app
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(120))
    delivery_address = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    my_list = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    product = db.relationship('Post', backref='author', lazy='dynamic')

    # followed = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)
    #
    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)

    # def is_following(self, user):
    #     return self.followed.filter(
    #         followers.c.followed_id == user.id).count() > 0
    #
    # def followed_posts(self):
    #     followed = Post.query.join(
    #         followers, (followers.c.followed_id == Post.user_id)).filter(
    #         followers.c.follower_id == self.id)
    #     own = Post.query.filter_by(user_id=self.id)
    #     return followed.union(own).order_by(Post.timestamp.desc())

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
    reviews = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):

        return '<Post {}>'.format(self.body)


class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(255))
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    mid = db.Column(db.Integer)
    status = db.Column(db.String(255))
    pc_id = db.Column(db.Integer)
    ps_id = db.Column(db.Integer)


class Category(db.Model):
    pc_id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(255))
    ps_id = db.Column(db.Integer)


class Subcategory(db.Model):
    ps_id = db.Column(db.Integer, primary_key=True)
    ps_name = db.Column(db.String(255))


class Pets(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)


class Disney(db.Model):
    disney_id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)


class Merchant(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    shipping_cart_id = db.Column(db.Integer)#, db.ForeignKey('shipping_cart'))
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer)#, db.ForeignKey('user_id'))
    status_id = db.Column(db.String(255))#, db.ForeignKey('status_id'))
    Create_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Order {}>'.format(self.order_id)

class Status(db.Model):
    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    shipment = db.Column(db.String(255))

    def __repr__(self):
        return '<Status {}>'.format(self.status_id)

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    cary_type = db.Column(db.Integer)
    card_number = db.Column(db.String(255))
    user_id = db.Column(db.Integer)#, db.ForeignKey('user_id'))

    def __repr__(self):
        return '<Payment {}>'.format(self.payment_id)

class Customer_Services(db.Model):
    services_id = db.Column(db.Integer, primary_key=True)
    services = db.Column(db.String(255))
    user_id = db.Column(db.Integer)#, db.ForeignKey('user_id'))

    def __repr__(self):
        return '<Services {}>'.format(self.services_id)

class Voucher(db.Model):
    v_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    expiary = db.Column(db.DateTime)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return '<Voucher {}>'.format(self.v_id)

class shopping_cart(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer)#, db.ForeignKey('user_id'))

    def __repr__(self):
        return '<Post {}>'.format(self.user_id)

        return '<Post {}>'.format(self.reviews)


class Housewares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    link = db.Column(db.String(255))

    def __repr__(self):
        return '<Housewares {}>'.format(self.id)


class SportsAndTravel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.column(db.String(120))
    link = db.Column(db.String(120))

    def __repr__(self):
        return '<SportsAndTravel {}>'.format(self.id)


class ToysAndBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(120))
    link = db.Column(db.String(120))

    def __repr__(self):
        return '<ToysAndBooks {}>'.format(self.id)


class UserProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<UserProduct {}>'.format(self.id)

