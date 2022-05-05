from flask import Blueprint, render_template

main_menu = Blueprint('main_menu', __name__)

@main_menu.route('/')
def home():
    return render_template("main.html")
