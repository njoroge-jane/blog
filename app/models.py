from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, confirm_login
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(blogger_id):
    return Blogger.query.get(int(blogger_id))


class Blogger(UserMixin, db.Model):
    __tablename__ = 'blogger'
    pass_secure = db.Column(db.String(255))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('Blogs', backref='blogger', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Blogs(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    blog = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.utcnow())
    blogger_id = db.Column(db.Integer, db.ForeignKey("blogger.id"))
    comments_id = db.relationship(
        'Comments', backref='commenter', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls, id):
        blogs = Blogs.query.filter_by(blogger_id=id).all()
        return blogs


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comments.query.filter_by(blog_id=id).all()
        return comments

class Subscription(db.Model):
    __tablename__ = 'subcription'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True)

    def save_email(self):
        db.session.add(self)
        db.session.commit()