from flask import Flask
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '42istheanswer'


    from website.main_menu import main_menu
    from website.auth import auth

    app.register_blueprint(main_menu, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app