import sys

from flask import Flask, request
from gevent.pywsgi import WSGIServer
import db

app = Flask(__name__)
database_op = db.DatabaseOp
if database_op.connect():
    print("Successfully connected to database")
else:
    print("Error when connecting to the database")
    sys.exit(0)


@app.route('/seller-signup')
def seller_signup():
    email = request.form.get('startDate')
    username = request.form.get('endDate')
    password = request.form.get('endDate')


    print(f'{email} + {username} + {password}')


@app.route('/seller-login')
def seller_login():
    return 'seller-login'


@app.route('/buyer-signup')
def seller_signup():
    return 'buyer-signup'


@app.route('/buyer-login')
def seller_login():
    return 'buyer-login'


@app.route('/admin-login')
def admin_login():
    return 'this is admin_login'


if __name__ == "__main__":
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
