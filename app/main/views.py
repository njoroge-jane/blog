from unicodedata import category
from flask import render_template, request, redirect, url_for, abort, jsonify
from . import main
from ..models import Category, User
from app.auth.forms import UpdateProfile
from .. import db, photos
from flask_login import login_required, current_user
from ..models import Pitches, Comments
from .forms import PitchForm, CommentsForm
from multiprocessing import Value

counter = Value('i', 0)


@main.route('/', methods=['GET', 'POST'])
def index():
    pitches = Pitches.query.all()
    title = 'Home Page'
    with counter.get_lock():
        counter.value += 1
        # save the value ASAP rather than passing to jsonify
        # to keep lock time short
        unique_count = counter.value
        counts = jsonify(count=unique_count)

    return render_template('index.html', title=title, pitches=pitches, count=counts)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitches.get_pitches(user.id)

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, pitches=pitches)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
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
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    user = User.query.first()

    if form.validate_on_submit():
        pitch_title = form.title.data
        category = form.category.data
        pitch = form.pitch.data
        pitch_category = Category.query.filter_by(id=category).first()
        new_pitch = Pitches(title=pitch_title,
                            category=category, pitch=pitch, user=current_user, categories=pitch_category)
        new_pitch.save_pitch()
        return redirect(url_for('.profile', uname=user.username))

    title = 'Add Pitch'
    return render_template('new_pitch.html', title=title, pitch_form=form)


@main.route('/user/comment/<int:id>', methods=["GET", "POST"])
@login_required
def comment(id):
    form = CommentsForm()
    comments = Comments.query.filter_by(pitch_id=id).all()
    pitch = Pitches.query.filter_by(id=id).first()

    if form.validate_on_submit():
        comment_submitted = form.comment.data
        new_comment = Comments(comment=comment_submitted, commenter=pitch)
        new_comment.save_comment()

    return render_template('comments.html', comment_form=form, comments=comments, pitch=pitch)


@main.route('/category/<int:id>')
def category(id):
    pitches = Pitches.query.filter_by(category_id=id).all()

    return render_template('category.html', categories=pitches)
