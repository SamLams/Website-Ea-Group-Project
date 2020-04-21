from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post, Product
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
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
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


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


@bp.route('/delivery_address')
@login_required
def delivery_address():
    page = request.args.get('page', 1, type=int)
    user = User.query.order_by(User.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.delivery_address', page=user.next_num) \
        if user.has_next else None
    prev_url = url_for('main.delivery_address', page=user.prev_num) \
        if user.has_prev else None
    return render_template('delivery_address.html', title=_('Delivery Address'),
                           user=user.items, next_url=next_url,
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
        current_user.about_me = form.about_me.data
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
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


# @bp.route('/follow/<pname>')
# @login_required
# def follow(pname):
#     name = Product.query.filter_by(pname=pname).first()
#     if name is None:
#         flash(_('User %(pname)s not found.', pname=pname))
#         return redirect(url_for('main.index'))
#     current_user.follow(name)
#     db.session.commit()
#     flash(_('You are following %(name)s!', pname=pname))
#     #return redirect(url_for('main.user', username=productname))
#
#
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
