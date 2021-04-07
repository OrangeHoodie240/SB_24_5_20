from flask_wtf import FlaskForm 
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import Length, InputRequired, Email

class RegisterForm(FlaskForm):
    username = StringField('Username: ', validators=[Length(max=20), InputRequired()])
    password = PasswordField('Password: ', validators=[InputRequired()])
    email = StringField('Email: ', validators=[InputRequired(), Length(max=50), Email()])
    first_name = StringField("First Name: ", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name: ", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[Length(max=20), InputRequired()])
    password = PasswordField('Password: ', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title: ', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Content: ', validators=[InputRequired()], render_kw={'rows': 8, 'cols': 30})
