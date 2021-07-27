from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Passcode', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is taken.')

class UploadFileForm(FlaskForm):
	genres = ["Placeholder1", "Placeholder2", "Placeholder3"]
	file = FileField('Choose file', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired(), Length(min=10, max=80)])
	genre = SelectField('Select genre', choices=genres, validators=[DataRequired()])
	submit = SubmitField('Upload')

class UpdatePassword(FlaskForm):
	old_password = StringField('Enter current password', validators=[DataRequired()])
	new_password = StringField('Enter new password', validators=[DataRequired()])
	new_password_confirmation = StringField('Re-enter new password', validators=[DataRequired(), EqualTo("new_password")])
	submit = SubmitField('Submit')
						