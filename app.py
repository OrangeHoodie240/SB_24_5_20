from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something something something'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)


@app.route('/', methods=['GET'])
def index():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(f'/users/{session.get("username")}')
        
    form = RegisterForm()

    if form.validate_on_submit():
        if(not User.username_available(form.username.data)):
            form.username.errors.append('Username unavailable')
            return render_template('register.html', form=form)

        user = User.register_from_form(form)
        User.add(user)

        session['username'] = user.username
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.validate(form)
        if(not user):
            form.username.errors.append(
                'Invalid Password / Username Combination')
            return render_template('login.html', form=form)

        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('/')


@app.route('/users/<username>')
def user_home(username):
    if 'username' not in session:
        flash('You Must log in in order to access this page')
        return redirect('/login')
    user = User.get(username)
    feedbacks = Feedback.get_for(username)

    return render_template('user_home.html', user=user, feedbacks=feedbacks)


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    # if the user doesn't exist 404
    User.query.get_or_404(username)

    if 'username' not in session or session.get('username') != username:
        flash("Unable to access this page.")
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form, username=username)


@app.route('/users/<username>/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(username, id):
    # return 404 if username does not exist
    User.query.get_or_404(username)

    if 'username' not in session or session.get('username') != username:
        flash("Unable to access this page.")
        return redirect('/login')

    Feedback.query.filter(Feedback.id == id).delete()
    db.session.commit()

    return redirect(f'/users/{username}')


@app.route('/users/<username>/feedback/<int:id>/edit', methods=['GET', 'POST'])
def edit_feedback(username, id):
    # return 404 if username does not exist
    User.query.get_or_404(username)

    if 'username' not in session or session.get('username') != username:
        flash("Unable to access this page.")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('edit_feedback.html', form=form, username=username, id=feedback.id)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # 404 if the username doesn't exist
    user = User.query.get_or_404(username)

    if 'username' not in session or session.get('username') != username:
        flash("Unable to access this page.")
        return redirect('/login')

    session.pop('username')    
    User.delete(user)


    return redirect('/')



@app.route('/secret', methods=['GET'])
def secret():
    if 'username' not in session:
        flash('You Must log in in order to access this page')
        return redirect('/login')
    return render_template('secret.html')
