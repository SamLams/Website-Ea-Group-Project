from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, PostForm, EditDeliveryAddressForm, CsForm, \
    EditMessage, DeliveryAddressForm, EditDeliveryAddressForm, AddVoucher
from app.models import User, Post, Product, Customer_Services, Delivery_Address, Shopping_cart, Housewares, \
    ToysAndBooks, Disney, SportsAndTravel, MyList, Merchant, Order, Voucher
from app.main import bp

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
    return render_template('index.html', title=_('Home'), prod=prod)


@login_required
@bp.route('/add_to_cart/<int:prod_id>', methods=['GET', 'POST'])
def add_to_cart(prod_id):
    p = Product.query.filter_by(pid=prod_id).first()
    cart_item = Shopping_cart(id=Shopping_cart.query.count() + 1, user_id=current_user.id, product_id=prod_id,
                                qty=1, price=p.price)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.post'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.post', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('post.html', title=_('Post'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


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


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    del_post = Post.query.get_or_404(id)
    db.session.delete(del_post)
    db.session.commit()
    return redirect(url_for('main.post'))


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
    products = db.session.query(Housewares.name, Product.price, Housewares.id, Housewares.link, Housewares.product_id).outerjoin(Product, Housewares.product_id == Product.pid).filter().all()
    return render_template('housewares.html', title=_('Home'), products=products)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/sportsntravel', methods=['GET', 'POST'])
def sportsntravel():
    products = db.session.query(SportsAndTravel.name, Product.price, SportsAndTravel.id, SportsAndTravel.link, SportsAndTravel.product_id).outerjoin(Product, SportsAndTravel.product_id == Product.pid).filter().all()
    return render_template('sportsntravel.html', title=_('Home'), products=products)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/toysnbooks', methods=['GET', 'POST'])
def toysnbooks():
    products = db.session.query(ToysAndBooks.name, Product.price, ToysAndBooks.id, ToysAndBooks.link, ToysAndBooks.product_id).outerjoin(Product, ToysAndBooks.product_id == Product.pid).filter().all()
    return render_template('toysnbooks.html', title=_('Home'), products=products)


@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    ccart = db.session.query(Shopping_cart.user_id, Product.pname, Product.price, Product.pid, Shopping_cart.qty).outerjoin(Product, Shopping_cart.product_id == Product.pid).filter(Shopping_cart.user_id == current_user.id).all()
    count = Shopping_cart.query.filter_by(user_id=current_user.id).count()
    if request.method == "POST":
        qty = request.form.get('quantity')
        prodid = request.form.get('prodid')
        prodprice = request.form.get('prodprice')
        itemcart = Shopping_cart.query.filter_by(product_id=prodid).filter_by(user_id=current_user.id).update({'qty': qty})
        itemcart = Shopping_cart.query.filter_by(product_id=prodid).filter_by(user_id=current_user.id).update({'price': float(prodprice) * int(qty)})
        db.session.commit()
        redirect(url_for('main.cart'))

    return render_template('cart.html', title=_('Shopping Cart'), ccart=ccart, count=count)


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
    next_url = url_for('main.delivery_address', user=user, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.delivery_address', user=user, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('delivery_address.html', user=user, title=_('Post'), form=form,
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


@bp.route('/delete_message/<services_id>', methods=['GET', 'POST'])
@login_required
def delete_message(services_id):
    del_m = Customer_Services.query.get_or_404(services_id)
    db.session.delete(del_m)
    db.session.commit()
    flash(_('Your message have been deleted.'))
    return redirect(url_for('main.cs', username=current_user.username))


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


@bp.route('/mylist')
@login_required
def mylist():
    item = db.session.query(MyList.user_id, MyList.name, Product.price, MyList.id, Product.link).outerjoin(Product, MyList.product_id == Product.pid).filter(MyList.user_id == current_user.id).all()
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

