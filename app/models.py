from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

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