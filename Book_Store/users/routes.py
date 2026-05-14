from Book_Store.users import users
from Book_Store.models import User
from Book_Store import bcrypt, db
from flask import render_template, redirect, url_for, flash, session
from Book_Store.users.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['user_id'] = user.id
            flash(f"Logged in successfully! Welcome {user.username}", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.strip()).first():
            flash("Email already registered. Please log in.", "danger")
            return render_template('signup.html', form=form)
        if User.query.filter_by(phone=form.phone.data.strip()).first():
            flash("Phone number already registered. Please log in.", "danger")
            return render_template('signup.html', form=form)
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip(),
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template('signup.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for('main.home'))
