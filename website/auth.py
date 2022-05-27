from flask import Flask, Blueprint, render_template, request
from flask_wtf import FlaskForm, RecaptchaField


class Widgets(FlaskForm):
    recaptcha = RecaptchaField()

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods = ['GET', 'POST'])
def sign_in():
    details = request.form

    from helperFunctions import functions

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

        country = 'NULL'

        functions.addUser(email, password, firstName, lastName, username)
        userID = functions.getUserID(email)

        functions.addAddress(userID, street1, town, state, zip, country, street2)
        addressID = functions.getAddressID(userID, street1)
        functions.updateShippingID(userID, addressID)
        functions.updateBillingID(userID, addressID)

        return "Success"

    return render_template("sign-up.html", form = details)

@auth.route('/forgot-username', methods = ['GET','POST'])
def forgot_username():
    from helperFunctions import functions
    details = request.form

    if request.method == 'POST':

        email = details["state"]

        if (functions.validateEmail(email)):
            functions.sendVerificationCode(email)
            return "Verification code sent to email if associated with an account."
        else:
            return "Invalid email"
    return render_template("forgot-username.html", form = details)

@auth.route('/profile')
def profile():

    return render_template("profile.html")
