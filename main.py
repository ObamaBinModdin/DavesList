from helperFunctions import functions
from website import create_app
#from flask_mysqldb import MySQL
import pymysql

app = create_app()

app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lft69EfAAAAAErMQPg5Mry2ED74SLHNXihQt0iP"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lft69EfAAAAAGcg4kHDYFXpUewNcfJflBMffbz7"

# app.config['MYSQL_HOST'] = 'db-cs380.cmfmlcsafjnf.us-west-2.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'dave'
# app.config['MYSQL_PASSWORD'] = 'E}Z&/F6X(rSr2pSf'
# app.config['MYSQL_DB'] = 'davesList'


# mysql = MySQL(app)


mysql = pymysql.connect(
    host = 'db-cs380.cmfmlcsafjnf.us-west-2.rds.amazonaws.com',
    user = 'dave',
    password = 'E}Z&/F6X(rSr2pSf',
    db = 'davesList',
    )

if __name__ == '__main__':

    app.run(debug=True)