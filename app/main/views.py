from unicodedata import category
from flask import render_template, request, redirect, url_for, abort
from . import main
from app.auth.forms import UpdateProfile
from .. import db, photos
from flask_login import login_required, current_user
from ..models import Blogs, Comments,Blogger, Quotes, Subscription
from .forms import BlogForm, CommentsForm,SubscriptionForm



@main.route('/', methods=['GET', 'POST'])
def index():
    blogs = Blogs.query.all()
    title = 'Home Page'
    # quote = Quotes(quote=quote,author=author)
    blogs = Blogs.query.all()
    form = SubscriptionForm()
    # if form.validate_on_submit():
    #     email = form.email.data
    #     new_subscriber = Subscription(email = email)
    #     new_subscriber.save_email()
    #     return redirect(url_for('main.index'))  

    return render_template('index.html',title=title, blogs = blogs, blogger = blogs, subscription_form = form)
    


@main.route('/user/<uname>')
def profile(uname):
    user = Blogger.query.filter_by(username=uname).first()
    blogs = Blogs.get_pitches(user.id)

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, blogs=blogs)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = Blogger.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user =Blogger.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    user = Blogger.query.first()

    if form.validate_on_submit():
        blog_title = form.title.data
        blog = form.blog.data
        new_blog = Blogs(title=blog_title,
                          blog=blog, user=current_user)
        new_blog.save_blog()
        return redirect(url_for('.profile', uname=user.username))

    title = 'Add Blog'
    return render_template('new_blog.html', title=title, blog_form=form)


@main.route('/comment/<int:id>', methods=["GET", "POST"])
def comment(id):
    form = CommentsForm()
    comments = Comments.query.filter_by(blog_id=id).all()
    blog = Blogs.query.filter_by(id=id).first()

    if form.validate_on_submit():
        comment_submitted = form.comment.data
        new_comment = Comments(comment=comment_submitted, commenter=blog)
        new_comment.save_comment()

    return render_template('comments.html', comment_form=form, comments=comments, blog=blog)

