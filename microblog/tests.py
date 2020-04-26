
#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config
from app.models import *


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):

    def testData(self):
        app = create_app(TestConfig)
        app_context = app.app_context()
        app_context.push()
        db.create_all()
        mer1 = Merchant(999, 'Test Company', 'Testing', 5.0)
        sc1 = Subcategory(ps_id=999, ps_name="sc1")
        c1 = Category(pc_id=999, pc_name="c1", ps_id=999)
        p1 = Product(pid=999, pname='Testing Product1', qty=1, price=45, mid=999,
                     status="Good", pc_id=999, ps_id=999)

        #pending = [mer1, sc1, c1, p1]
        db.session.add(mer1)
        db.session.add(sc1)
        db.session.add(c1)
        db.session.add(p1)
        db.session.commit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
