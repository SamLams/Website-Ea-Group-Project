from app import db
from app.main import bp
from app.models import Merchant, Product, Housewares, SportsAndTravel, ToysAndBooks, Subcategory, Category, User
from flask import url_for, redirect
from datetime import datetime


@bp.route('/init', methods=['GET', 'POST'])
def init():
    mer1 = Merchant(999, 'Test Company', 'Testing', 5.0)
    mer2 = Merchant(998, 'Test Company2', 'Testing', 5.2)
    mer3 = Merchant(997, 'Test Company3', 'Testing', 5.3)
    mer4 = Merchant(996, 'Test Company4', 'Testing', 5.5)
    sc1 = Subcategory(ps_id=999, ps_name="sc1")
    sc2 = Subcategory(ps_id=998, ps_name="sc2")
    sc3 = Subcategory(ps_id=997, ps_name="sc3")
    sc4 = Subcategory(ps_id=996, ps_name="sc4")
    c1 = Category(pc_id=999, pc_name="c1", ps_id=999)
    c2 = Category(pc_id=998, pc_name="c2", ps_id=998)
    c3 = Category(pc_id=997, pc_name="c3", ps_id=997)
    c4 = Category(pc_id=996, pc_name="c4", ps_id=996)
    p1 = Product(pid=999, pname='Testing Product1', qty=1, price=45, mid=999, status="Good", pc_id=999, ps_id=999,
                 link="https://picsum.photos/273/190")
    p2 = Product(pid=998, pname="TW Disposable Mask Protective Pad", qty=1, price=55, mid=998, status="Good", pc_id=998,
                 ps_id=998,
                 link="https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg")
    p3 = Product(pid=997, pname="FitBoxx - Everlast Evercool Gloves Bag", qty=1, price=56, mid=997, status="Good",
                 pc_id=997, ps_id=997, link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg")
    p4 = Product(pid=996, pname="HKQgamers - Switch Game - Pokemon Sword", qty=2, price=44, mid=996, status="no",
                 pc_id=996, ps_id=996,
                 link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg")
    h1 = Housewares(id=995, name="TW Disposable Mask Protective Pad",
                    link="https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg",
                    price=55, product_id=998)
    s1 = SportsAndTravel(id=995, name="FitBoxx - Everlast Evercool Gloves Bag",
                         link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg", price=65,
                         product_id=997)
    t1 = ToysAndBooks(id=995, name="HKQgamers - Switch Game - Pokemon Sword",
                      link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg",
                      price=44, product_id=996)
    admin = User(id=0, first_name="a", last_name="a", username="a", email="a@g.com", phone=132, password_hash="pbkdf2:sha256:50000$K1aBNTtq$a627489faa2332223c5225bbc26a9c875d57437fa4865b83875eeb957b3f04dd")
    db.session.add(admin)
    db.session.add(mer1)
    db.session.add(sc1)
    db.session.add(c1)
    db.session.add(p1)
    db.session.add(mer2)
    db.session.add(sc2)
    db.session.add(p2)
    db.session.add(c2)
    db.session.add(h1)
    db.session.add(mer3)
    db.session.add(sc3)
    db.session.add(c3)
    db.session.add(p3)
    db.session.add(s1)
    db.session.add(mer4)
    db.session.add(sc4)
    db.session.add(c4)
    db.session.add(p4)
    db.session.add(t1)
    db.session.commit()
    return redirect(url_for('main.index'))