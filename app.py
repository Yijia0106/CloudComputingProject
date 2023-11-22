import sys
from flask import Flask, request
import db

app = Flask(__name__)
database_op = db.DatabaseOp()
if database_op.connect():
    print("Successfully connected to database")
else:
    print("Error when connecting to the database")
    sys.exit(0)


@app.route('/')
def index():
    return 'Wrong Page'


@app.route('/seller-signup')
def seller_signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    print(f'{email} + {username} + {password}')
    database_op.insert_into_user_info('s', email, username, password)


@app.route('/seller-login')
def seller_login():
    return 'seller-login'


@app.route('/buyer-signup')
def buyer_signup():
    return 'buyer-signup'


@app.route('/buyer-login')
def buyer_login():
    return 'buyer-login'


@app.route('/admin-login')
def admin_login():
    return 'this is admin_login'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
