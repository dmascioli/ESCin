from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from app.__init__ import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Event
from app.forms import LoginForm, RegistrationForm, EventForm
from app.__init__ import app
import qrcode
from app.config import BASE_URL

#app = Flask(__name__)

QR_DIR = 'app/static/qr_codes/'


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create', methods=['GET','POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(name=form.name.data, author=current_user.username)
        db.session.add(event)
        db.session.commit()
        qr_img = qrcode.make(BASE_URL + url_for('display_code', event_id=event.id))
        path = QR_DIR+str(event.id) 
        qr_img.save(path +'.png')
        flash('Event Created')
        return redirect(url_for('display_code', event_id=event.id))
    return render_template('create_event.html', title='Create Event', form=form)

@app.route('/event/<event_id>')
@login_required
def view_attendees(event_id=None):
    pass

@app.route('/event/<event_id>/display')
@login_required
def display_code(event_id=None):
    pass

@app.route('/event/<event_id>/checkin')
def check_in(event_id=None):
    pass


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event}