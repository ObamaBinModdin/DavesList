from flask import Flask, redirect, url_for, render_template

from flask_wtf import FlaskForm, RecaptchaField


app = Flask(__name__)

app.config["SECRET_KEY"] = "secsecsec"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lft69EfAAAAAErMQPg5Mry2ED74SLHNXihQt0iP"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lft69EfAAAAAGcg4kHDYFXpUewNcfJflBMffbz7"
class Widgets(FlaskForm):
    recaptcha = RecaptchaField()
@app.route("/home")
def home():
    form = Widgets()
    return render_template("sign-up.html",form=form)

if __name__ == "__main__":
    app.run()
