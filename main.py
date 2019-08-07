from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from app.__init__ import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Event, Checkin
from app.forms import LoginForm, RegistrationForm, EventForm, CheckinForm
from app.__init__ import app
import qrcode
from app.config import BASE_URL

#app = Flask(__name__)

QR_DIR = 'app/static/qr_codes/'


@app.route('/')
def home():
    if current_user.is_anonymous:
        return render_template("home.html")
    else:
        events = Event.query.filter_by(creator=current_user.id).all()
        return render_template("home.html", events=events)

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
        event = Event(name=form.name.data, creator=current_user.username)
        db.session.add(event)
        db.session.commit()
        qr_img = qrcode.make(BASE_URL + url_for('check_in', event_id=event.id))
        path = QR_DIR+str(event.id)+'.png' 
        qr_img.save(path)
        relPath = '/static/qr_codes/'+str(event.id)+'.png'
        event.qr_code = relPath
        db.session.commit()
        flash('Event Created')
        return redirect(url_for('display_code', event_id=event.id))
    return render_template('create_event.html', title='Create Event', form=form)

@app.route('/event/<event_id>')
@login_required
def view_attendees(event_id=None):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('attendees.html', event=event)

@app.route('/event/<event_id>/display')
@login_required
def display_code(event_id=None):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('display.html', event=event)

@app.route('/event/<event_id>/checkin', methods=['GET', 'POST'])
def check_in(event_id=None):
    form = CheckinForm()
    if form.validate_on_submit():
        checkin = Checkin(first=form.first.data, last=form.last.data, pittid=form.pittid.data)
        event = Event.query.filter_by(id=event_id).first()
        event.checkins.append(checkin)
        db.session.add(checkin)
        db.session.commit()
        flash('Checked in!')
        return redirect(url_for('checkin_success'))
    return render_template('checkin.html', title='Check In', form=form)

@app.route('/success')
def checkin_success():
    return render_template('successful_checkin.html')




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event}