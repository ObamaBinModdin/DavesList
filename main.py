from helperFunctions import functions
from website import create_app
#from flask_mysqldb import MySQL
import pymysql
import stripe

app = create_app()

app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lft69EfAAAAAErMQPg5Mry2ED74SLHNXihQt0iP"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lft69EfAAAAAGcg4kHDYFXpUewNcfJflBMffbz7"

# app.config['MYSQL_HOST'] = 'db-cs380.cmfmlcsafjnf.us-west-2.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'dave'
# app.config['MYSQL_PASSWORD'] = 'E}Z&/F6X(rSr2pSf'
# app.config['MYSQL_DB'] = 'davesList'


# mysql = MySQL(app)


app.config[
    'STRIPE_PUBLIC_KEY'] = 'pk_test_51Kzv27BXAFyYLYCy3wbEAMqVoNx8FlcNMrmCsTMqxV8YqI4kTwnmor5rJHkwNCf1bopcyfKOewv1cWnOumFAOmHc000ugscmd0'
app.config[
    'STRIPE_SECRET_KEY'] = 'sk_test_51Kzv27BXAFyYLYCylfDhfY9h2GxqJq7vaF54uRjcIhhJnpuMmaEdDCSXboSJ096zkGF2asNtg3kTI8STQy9Jq3WJ002ck0SQWI'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


mysql = pymysql.connect(
    host = 'db-cs380.cmfmlcsafjnf.us-west-2.rds.amazonaws.com',
    user = 'dave',
    password = 'E}Z&/F6X(rSr2pSf',
    db = 'davesList',
    )

if __name__ == '__main__':

    app.run(debug=True)