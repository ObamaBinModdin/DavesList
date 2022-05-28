from flask import Flask, Blueprint, url_for, render_template, request
from flask_wtf import FlaskForm
import stripe

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

@market.route('/stripe_pay')
def stripe_pay():
    import main

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1KzwhvBXAFyYLYCyOe0DrFfR',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('market.success1', _external=True) + '?session_id= {CHECKOUT_SESSION_ID}',
        cancel_url=url_for('market.index', _external=True),

    )
    return {'checkout_session_id': session['id'], 'checkout_public_key': main.app.config['STRIPE_PUBLIC_KEY']}

@market.route("/index")
def index():
    return render_template('listing.html')



@market.route('/success1')
def success1():
    return render_template('success1.html')


@market.route('/cancle1')
def cancel1():
    return render_template('cancel1.html')