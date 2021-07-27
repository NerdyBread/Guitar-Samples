from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	image_file = db.Column(db.String(20), nullable=False, default='default_profile.jpg')
	user_desc = db.Column(db.String(120))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f'<User {self.username}>'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(128))
	description = db.Column(db.String(100))
	genre = db.Column(db.String(48))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Post by user {self.user_id}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))