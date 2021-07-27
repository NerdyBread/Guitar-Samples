from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, SignUpForm, UserDescription
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
		db.session.commit()
		flash('Your description has been updated!')
		return redirect(url_for('index'))

	return render_template('user_profile.html', samples=samples, user=user, image_file=image_file, form=form)
	






