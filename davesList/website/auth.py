
import mysql.connector
from flask import Blueprint, render_template, request
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm, RecaptchaField

import main



class Widgets(FlaskForm):
    recaptcha = RecaptchaField()

auth = Blueprint('auth', __name__)

@auth.route('/sign_in', methods = ['GET'])
def sign_in():
    return render_template("sign-in.html")

@auth.route('/forgot-password')
def forgot_password():
    return render_template("forgot-password.html")

@auth.route('/sign-up')
def sign_up():
    form = Widgets()
    return render_template("sign-up.html", form = form)

@auth.route('/forgot-username')
def forgot_username():

    return render_template("forgot-username.html")

@auth.route('/profile')
def profile():

    return render_template("profile.html")

@auth.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        import main
        cur = main.mysql.connection.cursor()
        cur.execute("INSERT INTO test(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        main.mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('test.html')