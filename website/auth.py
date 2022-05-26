from flask import Flask, Blueprint, render_template, request
from flask_wtf import FlaskForm, RecaptchaField


class Widgets(FlaskForm):
    recaptcha = RecaptchaField()

auth = Blueprint('auth', __name__)

@auth.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    details = request.form

    from helperFunctions import functions
    #functions.writeEmail("oscarford00@gmail.com", "test", "test")

    if request.method == 'POST':
        accountCredentials = details["username"]

        from helperFunctions import functions
        userID = functions.getUserID(accountCredentials)
        password = details["password"]

        if userID == -1:
            return "Incorrect entered credentials"
        else:
            correctPassword = functions.checkPassword(userID, password)

        if correctPassword:
            return "Welcome!"
        else:
            return "Incorrect entered credentials"

    return render_template("sign-in.html", form = details)

@auth.route('/forgot-password', methods = ['GET','POST'])
def forgot_password():
    details = request.form

    if request.method == 'POST':
        from helperFunctions import functions


        email = details["emailAdd"]


        if (functions.validateEmail(email)):
            print("Email sent to", email)
        else:
            print("Invalid email.")



    return render_template("forgot-password.html", form = details)

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'GET':
        form = Widgets()
        return render_template("sign-up.html", form = form)

@auth.route('/forgot-username', methods = ['GET','POST'])
def forgot_username():
    if request.method == 'POST':
        details = request.form
        email = details["state"]

        print(email)
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
        cur = main.mysql.cursor()
        cur.execute("INSERT INTO test(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        main.mysql.commit()
        cur.close()
        return 'success'
    return render_template('test.html')