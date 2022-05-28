from flask import Flask, redirect, url_for, render_template
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51Kzv27BXAFyYLYCy3wbEAMqVoNx8FlcNMrmCsTMqxV8YqI4kTwnmor5rJHkwNCf1bopcyfKOewv1cWnOumFAOmHc000ugscmd0'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Kzv27BXAFyYLYCylfDhfY9h2GxqJq7vaF54uRjcIhhJnpuMmaEdDCSXboSJ096zkGF2asNtg3kTI8STQy9Jq3WJ002ck0SQWI'

stripe.api_key= app.config['STRIPE_SECRET_KEY']

@app.route("/index")
def index():
    
    return render_template('listing.html')

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1KzwhvBXAFyYLYCyOe0DrFfR',
                'quantity': 1,
            }],
            mode='payment',
            success_url = url_for('success1',_external=True)+ '?session_id= {CHECKOUT_SESSION_ID}',
            cancel_url=url_for('index',_external=True),
            
    )
    return{'checkout_session_id': session['id'],'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']}

@app.route('/success1')
def success1():
    return render_template('success1.html')
@app.route('/cancle1')
def cancel1():
    return render_template('cancel1.html')

if __name__ == "__main__":
    app.run()