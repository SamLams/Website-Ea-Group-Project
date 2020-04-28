# !/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post, Merchant, Category, Subcategory, Product, Housewares, SportsAndTravel, ToysAndBooks, \
    MyList
from config import Config
from app import db


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):

    def testData(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        print("before")
        mer1 = Merchant(910, 'Test Company', 'Testing', 5.0)

        db.session.add(mer1)



        print("after")

        #pending = [mer1, sc1, c1, p1]
        #db.session.add(mer1)
        #db.session.add(sc1)
        #db.session.add(c1)
        #db.session.add(p1)
        db.session.commit()



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
c3 = Category(pc_id=997, pc_nagitme="c3", ps_id=997)
c4 = Category(pc_id=996, pc_name="c4", ps_id=996)
<<<<<<< HEAD
c5 = Category(pc_id=996, pc_name="c4", ps_id=996)
c6 = Category(pc_id=996, pc_name="c4", ps_id=996)

p1 = Product(pid=999, pname='Testing Product1', qty=1, price=45, mid=999, status="Good", pc_id=999, ps_id=999,
             link="https://picsum.photos/273/190")
p2 = Product(pid=998, pname="TW Disposable Mask Protective Pad", qty=1, price=55, mid=998, status="Good", pc_id=998,
             ps_id=998,
             link="https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg")
p3 = Product(pid=997, pname="FitBoxx - Everlast Evercool Gloves Bag", qty=1, price=56, mid=997, status="Good",
             pc_id=997, ps_id=997, link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg")
p4 = Product(pid=996, pname="HKQgamers - Switch Game - Pokemon Sword", qty=2, price=44, mid=996, status="no", pc_id=996,
             ps_id=996,
             link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg")
p5 = Product(pid=995, pname='Disney Toy Story', qty=3, price=155, mid=995, status="Good", pc_id=995, ps_id=995,
             link="https://images.hktv-img.com/images/HKTV/18800/H1283ToyStoryBook_main_36832182_20200409124617_01_1200.jpg")
p6 = Product(pid=994, pname='FRONTLINE - Plus for Cats & Kittens 8 Weeks or Older', qty=4, price=159, mid=994,
             status="Good", pc_id=994, ps_id=994, link="https://images.hktvmall.com/h0888001/129563/h0888001_10130629_171018034423_01_1200.jpg")

d1 = Disney(id=995, name="Disney Toy Story",
            link="https://images.hktv-img.com/images/HKTV/18800/H1283ToyStoryBook_main_36832182_20200409124617_01_1200.jpg",
            price=155, product_id=995)
pet1 = Pets(id=995, name="FRONTLINE - Plus for Cats & Kittens 8 Weeks or Older",
            link="https://images.hktvmall.com/h0888001/129563/h0888001_10130629_171018034423_01_1200.jpg", price=159,
            product_id=994)
h1 = Housewares(id=995, name="TW Disposable Mask Protective Pad",
                link="https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg",
                price=55, product_id=998)
s1 = SportsAndTravel(id=995, name="FitBoxx - Everlast Evercool Gloves Bag",
                     link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg", price=65,
                     product_id=997)
t1 = ToysAndBooks(id=995, name="HKQgamers - Switch Game - Pokemon Sword",
                  link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg",
                  price=44, product_id=996)
=======
p1 = Product(pid=999, pname='Testing Product1', qty=1, price=45, mid=999, status="Good", pc_id=999, ps_id=999,link= "https://picsum.photos/273/190")
p2 = Product(pid= 998, pname= "TW Disposable Mask Protective Pad", qty = 1, price=55, mid= 998, status= "Good", pc_id= 998, ps_id=998,link = "https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg")
p3 = Product(pid= 997, pname= "FitBoxx - Everlast Evercool Gloves Bag", qty = 1, price=56, mid= 997, status= "Good", pc_id= 997, ps_id=997,link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg")
p4 = Product(pid= 996, pname= "HKQgamers - Switch Game - Pokemon Sword", qty = 2, price=44, mid= 996, status= "no", pc_id= 996, ps_id=996,link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg")
h1 = Housewares(id = 995, name = "TW Disposable Mask Protective Pad", link= "https://images.hktv-img.com/images/HKTV/10787/MIT-001A_main_35311815_20200310182421_01_1200.jpg", price= 55,product_id=998)
s1 = SportsAndTravel(id=995, name="FitBoxx - Everlast Evercool Gloves Bag",link="https://images.hktvmall.com/h0395001/m/photos/8831465193522_1_1200.jpg",price=65, product_id=997)
t1 = ToysAndBooks(id=995, name="HKQgamers - Switch Game - Pokemon Sword",link="https://images.hktv-img.com/images/HKTV/10823/GA20191104A08_main_31312491_20191112141038_01_1200.jpg",price=44, product_id=996)
>>>>>>> 350499d56e3e967988faf17fcab070a5cee94be2
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
db.session.add(p5)
db.session.add(p6)
db.session.add(d1)
db.session.add(pet1)

db.session.commit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
