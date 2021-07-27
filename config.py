import os

basedir = os.path.dirname(__file__)

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or \
		open(os.path.join(os.path.dirname(__file__), 'config.key'), 'r').read()
	# .key in gitignore

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOAD_FOLDER = os.path.join(basedir, 'sounds')