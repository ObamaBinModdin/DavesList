from flask import Flask, Blueprint, render_template, request
from flask_wtf import FlaskForm, RecaptchaField


class Widgets(FlaskForm):
    recaptcha = RecaptchaField()

auth = Blueprint('auth', __name__)

@auth.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    details = request.form

    from helperFunctions import functions
    #functions.writeEmail("conner.kaul@cwu.edu", "bosyvdgosdog;zfv;dsfsdgvil;", "test")

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
            functions.sendVerificationCode(email)
            return "Verification code sent to email if associated with an account."
        else:
            return "Invalid email"



    return render_template("forgot-password.html", form = details)

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    from helperFunctions import functions
    details = request.form

    if request.method == 'POST':
        firstName = details['firstName']
        lastName = details['lastName']
        email = details['emailAdd']
        username = details['username']
        street1 = details['street1']
        street2 = details['street2']
        town = details['town']
        state = details['state']
        zip = details['zipCode']
        password = details['password']
        passwordRepeat = details['passwordRepeat']


        if not password == passwordRepeat:
            return "Passwords do not match."
        if not functions.validateEmail(email):
            return "Invalid email."
        if not functions.checkEmailAvailability(email):
            return "Email already in use."

        functions.addUser(email, password, firstName, lastName)
        return "Success"

    return render_template("sign-up.html", form = details)

@auth.route('/forgot-username', methods = ['GET','POST'])
def forgot_username():
    from helperFunctions import functions

    if request.method == 'POST':
        details = request.form
        email = details["state"]

        if (functions.validateEmail(email)):
            functions.sendVerificationCode(email)
            return "Verification code sent to email if associated with an account."
        else:
            return "Invalid email"
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