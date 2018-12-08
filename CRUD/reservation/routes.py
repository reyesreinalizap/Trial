import os
import secrets
from flask import render_template,url_for,flash,redirect,abort,request
from sqlalchemy.sql.functions import current_user
from reservation import app, db, bcrypt
from reservation.models import Reservation, User
from reservation.form import reservationForm, RegistrationForm, LoginForm, UpdateAccountForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/home")
def home():
        reservations = Reservation.query.all()
        return render_template('home.html', reservations=reservations)


@app.route("/menu")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return render_template('home.html')


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)




@app.route('/history')
@login_required
def history():
    reservations = Reservation.query.all()
    return render_template('history.html', reservations=reservations)

@app.route('/index')
@login_required
def index():
	reservations = Reservation.query.all()
	return render_template('index.html', reservations=reservations)



@app.route('/reservation/new', methods=['GET', 'POST'])
@login_required
def new_reservation():
    form = reservationForm()
    if form.validate_on_submit():
        if form.date.data < datetime.now().date():
            flash("You cannot book dates in the past")
            return redirect(url_for('new_reservation'))
        reservation = Reservation(package=form.package.data, date=form.date.data, location=form.location.data, occasion=form.occasion.data, addons=form.addons.data)
        if reservation:
            db.session.add(reservation, current_user)
            db.session.commit()
            flash("Reservation created!")
            return redirect(url_for('index'))
    return render_template('reservation.html', title="Make Reservation", form=form)



@app.route("/reservation/<int:id>")
def reservation(id):
    reservation = Reservation.query.filter_by(id=id).first_or_404()
    return render_template('view.html',  reservation=reservation)


@app.route("/reservation/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_reservation(id):
    reservation = Reservation.query.filter_by(id=id).first_or_404()
    if reservation.user != current_user:
        abort(403)
    form = reservationForm(obj=reservation)
    if form.validate_on_submit():
        if form.date.data < datetime.now().date():
            flash("You cannot book dates in the past")
            return redirect(url_for('update_reservation',id=id))
        #reservation = Reservation(package=form.package.data, date=form.date.data, location=form.location.data, occasion=form.occasion.data, addons=form.addons.data)
        else:
            reservation.package = form.package.data
            reservation.date = form.date.data
            reservation.location = form.location.data
            reservation.occasion = form.occasion.data
            reservation.addons = form.addons.data
            db.session.commit()
            flash("reservation is updated")
            return redirect(url_for('index',id=id))
    elif request.method == 'GET':
        form.package.data = reservation.package
        form.date.data = reservation.date
        form.location.data=reservation.location
        form.occasion.data=reservation.occasion
        form.addons.data=reservation.addons
    return render_template('update.html', form=form)


@app.route("/post/delete/<int:id>", methods=['POST'])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.filter_by(id=id).first_or_404()
    if reservation.user != current_user:
        abort(403)
    db.session.delete(reservation)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
