# !/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post, Merchant, Category, Subcategory, Product, Housewares, SportsAndTravel, ToysAndBooks, MyList
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

if __name__ == '__main__':
    unittest.main(verbosity=2)
