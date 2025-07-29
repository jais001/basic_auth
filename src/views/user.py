from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from src.core.models.user import User
from src.core.extensions.sql_alchemy_extension import db


user_auth_view_api = Blueprint("auth", __name__, template_folder='../../templates')

users = {}


@user_auth_view_api.route('/')
def home():
    """Home
    """
    if 'username' in session:
        return render_template('home.html', username=session["username"])
    return redirect(url_for('auth.login'))


@user_auth_view_api.route('/register', methods=['GET', 'POST'])
def register():
    """Register
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            # users[username] = hashed_pw
            flash("Registration succefull! Please login..")
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@user_auth_view_api.route("/login", methods=['GET', 'POST'])
def login():
    """Login
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # stored_pw = users.get(username)
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            flash("Login successful!!")
            return redirect(url_for('auth.home'))
        else:
            flash("Invalid username and password")
    return render_template('login.html')


@user_auth_view_api.route('/logout')
def logout():
    """Logout
    """
    session.pop('username', None)
    flash('Logged out!')
    return redirect(url_for('auth.login'))
