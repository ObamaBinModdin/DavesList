from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/sign_in')
def login():
    return render_template("sign-in.html")

@auth.route('/forgot-password')
def logout():
    return render_template("forgot-password.html")

@auth.route('/forgot-username')
def sign_up():

    return render_template("forgot-username.html")
