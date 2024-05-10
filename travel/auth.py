from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from . import db
from .models import User
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

#create a blueprint
authbp = Blueprint('auth', __name__ )

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error = None
    if loginForm.validate_on_submit():

        username=loginForm.user_name.data
        password=loginForm.password.data
        user=db.session.scalar(db.select(User).where(User.name==username))

        if not user:
            error="Username doesn't exist!"
        elif not check_password_hash(user.password_hash, password):
            error="Incorrect Password"

        if error is None:
            #Everything passed. now proceed to login
            login_user(user)
            flash("logged in successfully dude!!!!")
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=loginForm,  heading='Login')

@authbp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('Successfully registered')
        username=form.user_name.data
        password=form.password.data
        email=form.email_id.data
        print(f"Username: {username}, password: {password}, email: {email}")
        user = db.session.scalar(db.select(User).where(User.name==username))
        if user:
            flash("User already exists!", 'error')
            return redirect(url_for('main.index'))
        password_hash=generate_password_hash(password)
        new_user = User(name=username, password_hash=password_hash,emailid=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=form)

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!!')
    return redirect(url_for('main.index'))

