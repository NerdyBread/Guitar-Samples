import os

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import LoginForm, SignUpForm, UploadFileForm
from app.models import User, Post

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		flash(f'Signed in as {current_user.username}')
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignUpForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Thank you for signing up')
		return redirect(url_for('login'))
	return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
	form = UploadFileForm()
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(path)
			new_sample = Post(path=path, description=form.description.data, genre=form.genre.data, author=current_user)
			db.session.add(new_sample)
			db.session.commit()
			flash("File uploaded")
			return redirect(url_for('index'))
		else:
			flash("File type not allowed")
			return redirect(request.url)


	return render_template("upload.html", title="Upload", form=form)

def allowed_file(filename):
	allowed_extensions = ["mp3", "wav"]
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions