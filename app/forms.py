from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
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
        if user:
            raise ValidationError('Please use a different email address.')

class UserDescription(FlaskForm):
    description = StringField('Update your description', validators=[Length(max=120)])
    submit = SubmitField('Update')

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


class UpdateEmail(FlaskForm):
    email = StringField('Enter new password', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken, please chose a different one.')

class DeleteConfirm(FlaskForm):
    submit = SubmitField("Delete")