from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='430463536908-10a790mc125t036in6fusbt0phfj9mf8.apps.googleusercontent.com',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/home')
def hello():
	email = dict(session).get('email', None)
	return f'Hello, {email}'


@app.route('/login')
def login():
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
	session['email'] = user_info['email'] # get info directly from database instead of lifting from dict
    # do something with the token and profile 
	return redirect('/home')

if __name__ == '__main__':
	app.run(debug=True)


