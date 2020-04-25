from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db


from app.main.forms import EditProfileForm, PostForm, EditDeliveryAddressForm, DeliveryAddressForm
from app.models import User, Post, Product, Shopping_cart, Delivery_Address

from app.main.forms import EditProfileForm, PostForm, EditDeliveryAddressForm, CsForm, EditMessage, DeliveryAddressForm, EditDeliveryAddressForm
from app.models import User, Post, Product, Customer_Services, Delivery_Address, Shopping_cart


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
    cart_item = Shopping_cart(id=Shopping_cart.query.count() + 1, user_id=999, product_id=prod_id,
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
    product = Product.query.all()
    return render_template('housewares.html', title=_('Home'), product=product)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/sportsntravel', methods=['GET', 'POST'])
def sportsntravel():
    return render_template('sportsntravel.html', title=_('Home'))


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/toysnbooks', methods=['GET', 'POST'])
def toysnbooks():
    return render_template('toysnbooks.html', title=_('Home'))



@bp.route('/delivery_address/<username>', methods=['GET', 'POST'])

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html', title=_('Cart'))


@bp.route('/delivery_address/<username>')

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


@bp.route('/edit_message/<services_id>', methods=[' GET', 'POST'])
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
    list = Product.query.get_or_404(pid)
    db.session.add(list)
    db.session.commit()
    return redirect(url_for('main.mylist'))


@bp.route('/mylist')
@login_required
def mylist():
    return render_template('mylist.html', title=_('Post'))

# @bp.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash(_('User %(user)s not found.', username=username))
#         return redirect(url_for('main.housewares'))
#     current_user.follow(user)
#     db.session.commit()
#     flash(_('You are following %(user)s!', username=username))
#     return redirect(url_for('main.housewares'))
# @bp.route('/complete/<id>')
# def complete(id):
#     product = Product.query.filter_by(pid = int(id)).first()
#     product.complete = True
#     return redirect(url_for('main.housewares'))

# @bp.route('/unfollow/<pname>')
# @login_required
# def unfollow(pname):
#     name = Product.query.filter_by(pname=pname).first()
#     if name is None:
#         flash(_('User %(pname)s not found.', pname=pname))
#         return redirect(url_for('main.index'))
#     current_user.unfollow(name)
#     db.session.commit()
#     flash(_('You are not following %(username)s.', pname=pname))
#     #return redirect(url_for('main.user', username=username))
