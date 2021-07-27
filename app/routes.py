import os

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from app import app, db
from app.forms import LoginForm, SignUpForm, UserDescription, UploadFileForm, UpdatePassword, UpdateEmail, DeleteConfirm
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
  
@app.route("/user/<string:username>", methods=['GET', 'POST'])
def profile(username):
    form = UserDescription()
    user = User.query.filter_by(username=username).first_or_404()
    samples = Post.query.filter_by(author=user)
    image_file = url_for('static', filename=f"profile_pics/{user.image_file}")
  
    if form.validate_on_submit():
        user.user_desc = form.description.data
        db.session.commit()
        flash('Your description has been updated!')
        return redirect(url_for('index'))
    return render_template('user_profile.html', samples=samples, user=user, image_file=image_file, form=form)


@app.route('/admin')
def admin():
	if current_user.username != "Administrator":
		return redirect(url_for('index'))
	else:
		return render_template('admin.html', users=User.query.all())

@app.route('/account')
@login_required
def account():
	return render_template('updateAccount.html')

"""Account management subpages"""
@app.route('/account/password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = UpdatePassword()
	if form.validate_on_submit():
		old_password = form.old_password.data
		correct = check_password_hash(current_user.password_hash, old_password)
		if correct:
			current_user.set_password(form.new_password.data)
			db.session.commit()
			flash("Password updated")
			return redirect(url_for('account'))
		else:
			flash("Incorrect password")
			return redirect(url_for('account/password'))
	return render_template('changePassword.html', form=form)

@app.route('/account/email', methods=['GET', 'POST'])
@login_required
def change_email():
	form = UpdateEmail()
	if form.validate_on_submit():
		current_user.email = form.email.data
		db.session.commit()
		flash('Your email has been updated!')
		return redirect(url_for('index'))
	elif request.method == 'GET':
		form.email.data = current_user.email
	return render_template('update_email.html', form=form)

@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
	form = DeleteConfirm()
	if form.validate_on_submit():
		User.query.filter_by(id=current_user.id).delete()
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('delete_account.html', form=form)

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
