from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,DateField,SelectField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
from wtforms.fields.html5 import DateField
from reservation.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class reservationForm(FlaskForm):
    package = SelectField('Package', choices=[('Menu1', 'PACM'), ('Menu2', 'PACM'), ('Menu3', 'CB'), ('Menu4', 'CB')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    location = TextAreaField('Location', validators=[DataRequired()])
    occasion = SelectField('Occasion', choices=[('Birthday', 'Bd'), ('Wedding', 'Wed'), ('Anniversary', 'Anniv'), ('Corporate Event', 'CE'), ('Christening', 'CH'), ('Reunion', 'Re'), ('School Event', 'SE')], validators=[DataRequired()])
    addons = TextAreaField('Addons', validators=[DataRequired()])
    submit = SubmitField('Reserve')
    id = IntegerField('ID')
