from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def delete(cls, user):
        Feedback.query.filter(Feedback.username == user.username).delete() 
        db.session.commit() 

        cls.query.filter(cls.username == user.username).delete() 
        db.session.commit() 
        return True

    @classmethod
    def username_available(cls, username):
        if(cls.query.filter(cls.username == username).count() > 0):
            return False
        return True

    @classmethod
    def add(cls, user):
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def register_from_form(cls, form):
        username = form.username.data

        password = form.password.data
        password = bcrypt.generate_password_hash(password, 14)
        password = password.decode('utf-8')
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = cls(username=username, password=password, email=email,
                   first_name=first_name, last_name=last_name)

        return user

    @classmethod
    def validate(cls, form):
        user = cls.query.filter(
            cls.username == form.username.data).one_or_none()
        if(not user):
            return False

        if bcrypt.check_password_hash(user.password, form.password.data):
            return user

        return False

    @classmethod
    def get(cls, username):
        return cls.query.filter(cls.username == username).one()

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

    @classmethod
    def get_for(cls, username):
        return cls.query.filter(cls.username == username).all() 