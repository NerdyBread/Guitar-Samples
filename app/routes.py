from flask import flash, redirect, render_template, url_for, session

from app import app, oauth
from app.forms import LoginForm

google = oauth.register(
    name='google',
    client_id='430463536908-10a790mc125t036in6fusbt0phfj9mf8.apps.googleusercontent.com',
    client_secret=open('client_secret.key', 'r').read(),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/')
@app.route('/index')
def index():
	email = dict(session).get('email', None)
	return render_template('index.html', title="Home", email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f"Login requested for user {form.username.data}, remember me {form.remember_me.data}")
		return redirect(url_for('index'))
	return render_template('login.html', title="Sign In", form=form)

@app.route('/googlelogin')
def googlelogin():
	google = oauth.create_client('google')
	redirect_uri = url_for('authorize', _external=True)
	return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
	google = oauth.create_client('google')
	token = google.authorize_access_token()
	resp = google.get('userinfo')
	resp.raise_for_status()
	user_info = resp.json()
	session['email'] = user_info['email'] # TODO get info directly from database instead of lifting from dict
	return redirect(url_for('index'))