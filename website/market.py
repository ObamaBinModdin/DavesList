from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm

market = Blueprint('market', __name__)

@market.route('/ItemListings')
def item_listings():
    return render_template("item-listings.html")

@market.route('/browsing')
def browsing():
    return render_template("browsing.html")

@market.route('/sell', methods = ['GET', 'POST'])
def sell():
    return render_template("sell.html")

@market.route('/ViewListings', methods = ['GET', 'POST'])
def view_listings():
    return render_template("viewListings.html")