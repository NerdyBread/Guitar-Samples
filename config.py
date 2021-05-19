import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or open(os.path.join(os.path.dirname(__file__), 'config.key'), 'r').read()
	# .key in gitignore