from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, PostForm, CsForm, \
    EditMessage, DeliveryAddressForm, EditDeliveryAddressForm, AddVoucher, EditProduct
from app.models import User, Post, Product, Customer_Services, Delivery_Address, Shopping_cart, Housewares, \
    ToysAndBooks, SportsAndTravel, MyList, Order, Voucher, Merchant, Subcategory, Category, Disney, Pets
from app.main import bp
from sqlalchemy import func


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    prod = Product.query.all()
    count = User.query.count()
    return render_template('index.html', title=_('Home'), prod=prod, count=count)


@bp.route('/add_to_cart/<int:prod_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(prod_id):
    p = Product.query.filter_by(pid=prod_id).first()
    if current_user.is_authenticated:
        cart_item = Shopping_cart(user_id=current_user.id, product_id=prod_id,
                                  qty=1, price=p.price)
        db.session.add(cart_item)
        db.session.commit()
    else:
        flash(_('Please login first.'))
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.index'))


@bp.route('/loading', methods=['GET', 'POST'])
@login_required
def loading():
    return redirect(url_for('main.cart'))


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    otherpost = Post.query.all()
    if form.validate_on_submit():
        post = Post(post=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
    return render_template('post.html', title=_('Post'), form=form, otherpost = otherpost)





@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('post.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/del_list/<int:id>')
@login_required
def del_list(id):
    del_list = MyList.query.get_or_404(id)
    db.session.delete(del_list)
    db.session.commit()
    return redirect(url_for('main.mylist'))


@bp.route('/del_address/<int:id>')
@login_required
def del_address(id):
    del_address = Delivery_Address.query.get_or_404(id)
    db.session.delete(del_address)
    db.session.commit()
    return redirect(url_for('main.delivery_address', username=current_user.username))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/housewares', methods=['GET', 'POST'])
def housewares():
    products = db.session.query(Housewares.name, Product.price, Housewares.id, Housewares.link,
                                Housewares.product_id).outerjoin(Product,
                                                                 Housewares.product_id == Product.pid).filter().all()
    return render_template('housewares.html', title=_('Home'), products=products)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/pets', methods=['GET', 'POST'])
def pets():
    products = db.session.query(Pets.name, Product.price, Pets.id, Pets.link,
                                Pets.product_id).outerjoin(Product,
                                                                 Pets.product_id == Product.pid).filter().all()
    return render_template('pets.html', title=_('Home'), products=products)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/disney', methods=['GET', 'POST'])
def disney():
    products = db.session.query(Disney.name, Product.price, Disney.id, Disney.link,
                                Disney.product_id).outerjoin(Product,
                                                                 Disney.product_id == Product.pid).filter().all()
    return render_template('disney.html', title=_('Home'), products=products)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/sportsntravel', methods=['GET', 'POST'])
def sportsntravel():
    products = db.session.query(SportsAndTravel.name, Product.price, SportsAndTravel.id, SportsAndTravel.link,
                                SportsAndTravel.product_id).outerjoin(Product,
                                                                      SportsAndTravel.product_id == Product.pid).filter().all()
    return render_template('sportsntravel.html', title=_('Home'), products=products)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/toysnbooks', methods=['GET', 'POST'])
def toysnbooks():
    products = db.session.query(ToysAndBooks.name, Product.price, ToysAndBooks.id, ToysAndBooks.link,
                                ToysAndBooks.product_id).outerjoin(Product,
                                                                   ToysAndBooks.product_id == Product.pid).filter().all()
    return render_template('toysnbooks.html', title=_('Home'), products=products)


@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    ccart = db.session.query(Shopping_cart.user_id, Product.pname, Product.price, Product.pid,
                             Shopping_cart.qty).outerjoin(Product, Shopping_cart.product_id == Product.pid).filter(
        Shopping_cart.user_id == current_user.id).all()
    count = Shopping_cart.query.filter_by(user_id=current_user.id).count()


    if request.method == "POST":
        qty = request.form.get('quantity')
        prodid = request.form.get('prodid')
        prodprice = request.form.get('prodprice')
        code = request.form.get('voucher')
        result = Voucher.query.filter_by(code=code).first()
        discount = 0
        if result:
            discount = result.discount
        itemcart = Shopping_cart.query.filter_by(product_id=prodid).filter_by(user_id=current_user.id).update(
            {'qty': qty})
        itemcart = Shopping_cart.query.filter_by(product_id=prodid).filter_by(user_id=current_user.id).update(
            {'price': float(prodprice) * int(qty) - float(discount)})
        db.session.commit()

        return redirect(url_for('main.loading'))

    sum = db.session.query(func.sum(Shopping_cart.price)).filter_by(user_id=current_user.id).first()[0]
    return render_template('cart.html', title=_('Shopping Cart'), ccart=ccart, count=count, sum=sum)


@bp.route('/cart_del/<prodid>', methods=['GET', 'POST'])
@login_required
def cart_del(prodid):
    dele = Shopping_cart.query.filter_by(product_id=prodid).filter_by(user_id=current_user.id).first()
    db.session.delete(dele)
    db.session.commit()
    return redirect(url_for('main.cart'))


@bp.route('/confirmed', methods=['GET', 'POST'])
@login_required
def confirmed():
    ###ordered = Order()
    qty = 0
    price = 0
    item = Shopping_cart.query.filter_by(user_id=current_user.id).all()
    for i in item:
        qty += i.qty
        price += i.price
        db.session.delete(i)

    o = Order(qty=qty, price=price,user_id=current_user.id)#shopping_cart_id=i.id
    db.session.add(o)
    db.session.commit()
    return render_template('confirmed.html')

@bp.route('/delivery_address/<username>', methods=['GET', 'POST'])
@login_required
def delivery_address(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = DeliveryAddressForm()
    if form.validate_on_submit():
        address = Delivery_Address(address=form.delivery_address.data, user=current_user)
        db.session.add(address)
        db.session.commit()
        return redirect(url_for('main.delivery_address', username=current_user.username))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_address().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.delivery_address', username = current_user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.delivery_address', username = current_user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('delivery_address.html', user=user, title=_('delivery_address'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email, current_user.phone, current_user.first_name,
                           current_user.last_name)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.gender.data = current_user.gender
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/edit_delivery_address/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_delivery_address(id):
    form = EditDeliveryAddressForm(id)
    if form.validate_on_submit():
        update_address = Delivery_Address.query.get_or_404(id)
        update_address.address = form.delivery_address.data
        db.session.commit()
        return redirect(url_for('main.delivery_address', username=current_user.username))
    elif request.method == 'GET':
        update_address = Delivery_Address.query.get_or_404(id)
        form.delivery_address.data = update_address.address
    return render_template('edit_delivery_address.html', title=_('Edit Delivery Address'),
                           form=form)


@bp.route('/cs/')
@bp.route('/cs/<username>', methods=['GET', 'POST'])
@login_required
def cs(username):
    form = CsForm()
    user = User.query.filter_by(username=username).first_or_404()
    messages = Customer_Services.query.filter_by(user_id=current_user.id).all()
    if current_user.id == 0:
        messages = Customer_Services.query.all()
    if form.validate_on_submit():
        services = Customer_Services(services=form.services.data, user_id=current_user.id)
        db.session.add(services)
        db.session.commit()
        flash(_('Your message sent! Thank you!'))
        return redirect(url_for('main.cs', username=current_user.username))
    return render_template('cs.html', title=_('Customer Services'), form=form, user=user, messages=messages)


@bp.route('/edit_message/<services_id>', methods=['GET', 'POST'])
@login_required
def edit_message(services_id):
    auth = Customer_Services.query.filter_by(services_id=services_id, user_id=current_user.id).all()
    if auth:
        form = EditMessage()
        if form.validate_on_submit():
            mes = Customer_Services.query.get(services_id)
            mes.services = form.message.data
            db.session.commit()
            flash(_('Your message have been updated.'))
            return redirect(url_for('main.cs', username=current_user.username))
        elif request.method == 'GET':
            mes = Customer_Services.query.get(services_id)
            form.message.data = mes.services
        return render_template('edit_message.html', title=_('Edit Message'), form=form)
    else:
        return redirect(url_for('main.index'))

@bp.route('/delete_message/<services_id>', methods=['GET', 'POST'])
@login_required
def delete_message(services_id):
    auth = Customer_Services.query.filter_by(services_id=services_id, user_id=current_user.id).all()
    if auth:
        del_m = Customer_Services.query.get_or_404(services_id)
        db.session.delete(del_m)
        db.session.commit()
        flash(_('Your message have been deleted.'))
        return redirect(url_for('main.cs', username=current_user.username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/add_list/<int:pid>', methods=['GET'])
@login_required
def add_list(pid):
    p = Product.query.filter_by(pid=pid).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=pid)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/add_list1/<int:id>', methods=['GET'])
@login_required
def add_list1(id):
    p = Product.query.filter_by(pid=id).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.housewares'))


@bp.route('/add_list2/<int:id>', methods=['GET'])
@login_required
def add_list2(id):
    p = Product.query.filter_by(pid=id).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.sportsntravel'))


@bp.route('/add_list3/<int:id>', methods=['GET'])
@login_required
def add_list3(id):
    p = Product.query.filter_by(pid=id).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.toysnbooks'))

@bp.route('/add_list4/<int:id>', methods=['GET'])
@login_required
def add_list4(id):
    p = Product.query.filter_by(pid=id).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.pets'))

@bp.route('/add_list5/<int:id>', methods=['GET'])
@login_required
def add_list5(id):
    p = Product.query.filter_by(pid=id).first()
    cart_item = MyList(id=MyList.query.count() + 1, name=p.pname, user_id=current_user.id, product_id=id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.disney'))

@bp.route('/mylist')
@login_required
def mylist():
    item = db.session.query(MyList.user_id, MyList.name, Product.price, MyList.id, Product.link).outerjoin(Product,
                                                                                                           MyList.product_id == Product.pid).filter(
        MyList.user_id == current_user.id).all()
    return render_template('mylist.html', title=_('My List'), item=item)


@bp.route('/order_history/<username>', methods=['GET', 'POST'])
@login_required
def order_history(username):
    user = User.query.filter_by(username=username).first_or_404()
    order = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order/order_history.html', title=_('order'), user=user, order=order)


@bp.route('/voucher', methods=['GET', 'POST'])
@login_required
def voucher():
    form = AddVoucher()
    if form.validate_on_submit():
        result = Voucher.query.filter_by(code=form.voucher.data).all()
        if result:
            flash(_('Voucher is able'))
        else:
            flash(_('Voucher is disable'))
        return redirect(url_for('main.voucher'))
    return render_template('vouchers/voucher.html', title=_('Voucher'), form=form)


@bp.route('/edit_product/<pid>', methods=['GET', 'POST'])
@login_required
def edit_product(pid):
    if current_user.id == 0:
        form = EditProduct()
        if form.validate_on_submit():
            product = Product.query.get(pid)
            product.pid = form.pid.data
            product.pname = form.pname.data
            product.qty = form.qty.data
            product.price = form.price.data
            product.mid = form.mid.data
            product.status = form.status.data
            product.link = form.link.data
            product.pc_id = form.pc_id.data
            product.ps_id = form.ps_id.data
            db.session.commit()
            flash(_('Product have been updated.'))
            return redirect(url_for('main.all_product'))
        elif request.method == 'GET':
            product = Product.query.get(pid)
            form.pid.data = product.pid
            form.pname.data = product.pname
            form.qty.data = product.qty
            form.price.data = product.price
            form.mid.data = product.mid
            form.status.data = product.status
            form.link.data = product.link
            form.pc_id.data = product.pc_id
            form.ps_id.data = product.ps_id
        return render_template('product/edit.html', title=_('Edit Product'), form=form)
    else:
        return redirect(url_for('main.index'))

@bp.route('/delete_product/<pid>', methods=['GET', 'POST'])
@login_required
def delete_product(pid):
    if current_user.id ==0:
        del_product = Product.query.get_or_404(pid)
        db.session.delete(del_product)
        db.session.commit()
        flash(_('Prdouct have been deleted.'))
        return redirect(url_for('main.all_product'))
    else:
        return redirect(url_for('main.index'))

@bp.route('/all_product', methods=['GET', 'POST'])
def all_product():
    products = Product.query.all()
    return render_template('product/all_product.html', title=_('All Product'), products=products)


@bp.route('/insert_product', methods=['GET', 'POST'])
@login_required
def insert_product():
    form = EditProduct()
    if form.validate_on_submit():
        product = Product(pid=form.pid.data,
                          pname=form.pname.data,
                          qty=form.qty.data,
                          price=form.price.data,
                          mid=form.mid.data,
                          status=form.status.data,
                          link=form.link.data,
                          pc_id=form.pc_id.data,
                          ps_id=form.ps_id.data)
        db.session.add(product)
        db.session.commit()
        flash(_('Product have been inserted.'))
        return redirect(url_for('main.all_product'))
    return render_template('product/insert_product.html', title=_('Insert Product'), form=form)


@bp.route('/init', methods=['GET', 'POST'])
def init():
    mer1 = Merchant(999, 'Test Company', 'Testing', 5.0)
    mer2 = Merchant(998, 'Test Company2', 'Testing', 5.2)
    mer3 = Merchant(997, 'Test Company3', 'Testing', 5.3)
    mer4 = Merchant(996, 'Test Company4', 'Testing', 5.5)
    mer5 = Merchant(995, 'Test Company5', 'Testing', 5.6)
    mer6 = Merchant(994, 'Test Company6', 'Testing', 5.7)
    sc1 = Subcategory(ps_id=999, ps_name="sc1")
    sc2 = Subcategory(ps_id=998, ps_name="sc2")
    sc3 = Subcategory(ps_id=997, ps_name="sc3")
    sc4 = Subcategory(ps_id=996, ps_name="sc4")
    sc5 = Subcategory(ps_id=995, ps_name="sc5")
    sc6 = Subcategory(ps_id=994, ps_name="sc6")
    c1 = Category(pc_id=999, pc_name="c1", ps_id=999)
    c2 = Category(pc_id=998, pc_name="c2", ps_id=998)
    c3 = Category(pc_id=997, pc_name="c3", ps_id=997)
    c4 = Category(pc_id=996, pc_name="c4", ps_id=996)
    c5 = Category(pc_id=995, pc_name="c5", ps_id=995)
    c6 = Category(pc_id=994, pc_name="c6", ps_id=994)

    p5 = Product(pid=995, pname='Disney Toy Story', qty=3, price=155, mid=995, status="Good", pc_id=995, ps_id=995,
                 link="https://images.hktv-img.com/images/HKTV/18800/H1283ToyStoryBook_main_36832182_20200409124617_01_1200.jpg")
    p6 = Product(pid=994, pname='FRONTLINE - Plus for Cats & Kittens 8 Weeks or Older', qty=4, price=159, mid=994,
                 status="Good", pc_id=994, ps_id=994,
                 link="https://images.hktvmall.com/h0888001/129563/h0888001_10130629_171018034423_01_1200.jpg")

    d1 = Disney(id=995, name="Disney Toy Story",
                link="https://images.hktv-img.com/images/HKTV/18800/H1283ToyStoryBook_main_36832182_20200409124617_01_1200.jpg",
                price=155, product_id=995)
    pet1 = Pets(id=995, name="FRONTLINE - Plus for Cats & Kittens 8 Weeks or Older",
                link="https://images.hktvmall.com/h0888001/129563/h0888001_10130629_171018034423_01_1200.jpg",
                price=159,
                product_id=994)
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
    admin = User(id=0, first_name="a", last_name="a", username="a", email="a@g.com", phone=132,
                 password_hash="pbkdf2:sha256:50000$K1aBNTtq$a627489faa2332223c5225bbc26a9c875d57437fa4865b83875eeb957b3f04dd")
    db.session.add(admin)
    v1 = Voucher(v_id=1,code="hktv",discount="10")
    db.session.add(v1)
    db.session.add(mer1)
    db.session.add(mer2)
    db.session.add(mer3)
    db.session.add(mer4)
    db.session.add(mer5)
    db.session.add(mer6)
    db.session.add(sc1)
    db.session.add(sc2)
    db.session.add(sc3)
    db.session.add(sc4)
    db.session.add(sc5)
    db.session.add(sc6)
    db.session.commit()
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)
    db.session.commit()
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)
    db.session.add(p6)
    db.session.commit()
    db.session.add(h1)
    db.session.add(s1)
    db.session.add(t1)
    db.session.add(d1)
    db.session.add(pet1)
    db.session.commit()
    return redirect(url_for('main.index'))

