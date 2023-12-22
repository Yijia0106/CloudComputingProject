import json
import logging
from datetime import date

import boto3
import requests
from flask import Flask, request, make_response, jsonify, render_template

import db
import middleware

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__, template_folder='frontend')
app.wsgi_app = middleware.SimpleMiddleWare(app.wsgi_app)
database_op = db.DatabaseOp()
sns_client = boto3.client('sns', region_name='us-east-1')

if database_op.connect():
    logger.info("Successfully connected to database")
else:
    logger.error("Error when connecting to the database")


@app.route('/index', methods=['GET'])
def index():
    return 'Welcome Yes'


@app.route('/greeting', methods=['GET'])
def greeting():
    today = date.today()
    return f"Today's date: {today}  >333  I Love you YaoYao"


@app.route('/login', methods=['POST'])
def login():
    identity_map = {'seller': 's',
                    'buyer': 'b',
                    'admin': 'a'}

    email = request.form.get('email')
    password = request.form.get('password')
    identity = identity_map.get(request.form.get('identity'))
    response = make_response("<h1>Success</h1>", 201)
    logger.info(f"New login request received for {identity}: {email}")
    output = database_op.select_from_user_info_by_email(email)

    if not output:
        # No match record (email)
        logger.error(f"This email {email} is not registered!")
        response = make_response("<h1>Failed due to unregistered email</h1>", 200)
    elif output[0][3] != password:
        # Password doesn't match
        logger.error(f"This password is not corrected!")
        response = make_response("<h1>Failed due to wrong password</h1>", 200)
    elif output[0][5] == 'Y':
        # this user is banned by admin
        logger.error(f"This user is banned")
        response = make_response("<h1>Failed due to limited right</h1>", 200)
    else:
        # successfully login
        user_id = output[0][0]
        database_op.insert_into_activities(user_id, 'login')

    return response


@app.route('/users', methods=['GET'])
def get_users():
    logger.info("New Look up request")
    identity_map = {'seller': 's',
                    'buyer': 'b',
                    'admin': 'a'}
    args = request.args
    where_clause = ""
    if 'email' in args:
        where_clause += f'email = **{args["email"]}** and '
    if 'identity' in args:
        where_clause += f'type = **{identity_map.get(args["identity"])}** and '
    if 'is_blocked' in args:
        where_clause += f'is_blocked = **{args["is_blocked"]}** and '
    if 'username' in args:
        where_clause += f'username = **{args["username"]}** and '
    where_clause += "1 = 1"
    logger.info(f"The filtering condition is: {where_clause}")
    entries = database_op.select_from_user_info(where_clause)
    if not entries:
        logger.error(f"Corresponding users do not exist!")
        response = make_response("<h1>Corresponding users do not exist!</h1>", 200)
    else:
        if 'per_page' in args:
            per_page = int(args['per_page'])
        else:
            per_page = 2
        if 'page' in args:
            page = int(args['page'])
        else:
            page = 1
        offset = (page - 1) * per_page
        limit = per_page
        new_entries = database_op.select_from_user_info_with_pagination(where_clause, offset, limit)
        res = []
        if not new_entries:
            return make_response("<h1>No users at this page!</h1>", 404)
        for entry in new_entries:
            temp = {'username': entry[1],
                    'email': entry[2],
                    'user type': entry[4],
                    'status': entry[5],
                    'created timestamp': entry[6]}
            res.append(temp)

        response = make_response(jsonify(res), 200)
    return response


@app.route('/users', methods=['POST'])
def create_a_user():
    identity_map = {'seller': 's',
                    'buyer': 'b'}
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    identity = identity_map.get(request.form.get('identity'))
    response = make_response("<h1>Success</h1>", 201)
    logger.info(f"New signup request received for {identity}: {email}, {username} {password}")
    # see if there is a duplicate entry
    if database_op.select_from_user_info_by_email(email):
        # duplicate!
        logger.error(f"Trying to sign up using a duplicate email address: {email}")
        response = make_response("<h1>Failed due to duplicate email address</h1>", 201)
    else:
        # if no, insert a new entry
        database_op.insert_into_user_info(identity, email, username, password)
        msg = {
            'email': email,
            'username': username,
            'identity': identity
        }
        sns_client.publish(TopicArn='arn:aws:sns:us-east-1:876783651405:CloudComputingProject', Message=json.dumps(msg),
                           Subject='New Registered User')
        logger.info("A new message got published to SNS")

    return response


@app.route('/users/<string:email>', methods=['GET'])
def get_the_user(email):
    logger.info("New get single user request received!")
    output = database_op.select_from_user_info_by_email(email)
    if not output:
        response = ("<h1>User Not Found</h1>", 404)
    else:
        entry = output[0]
        temp = {'username': entry[1],
                'email': entry[2],
                'user type': entry[4],
                'status': entry[5],
                'created timestamp': entry[6]}
        response = make_response(jsonify(temp), 200)
    return response


@app.route('/users/<string:email>', methods=['PUT', 'DELETE'])
def update_user(email):
    logger.info(f"New update user request and the request type is {request.method}")
    email = email
    if request.method == 'PUT':
        payload = request.get_json()
        change_to = payload["change_to"]
        if database_op.update_user_status(email, change_to):
            logger.info(
                f"Try to set the status of user {email} to {change_to}. 'Y' means the user is restricted and 'N' means the user account is free")
            response = make_response("<h1>Success</h1>", 200)
        else:
            logger.error(
                f"Error encountered when trying to set the status of user {email} to {change_to}. 'Y' means the user is restricted and 'N' means the user account is free")
            response = make_response("<h1>Error</h1>", 200)
    elif request.method == 'DELETE':
        if database_op.delete_a_user(email):
            logger.info(
                f"User {email} is deleted.")
            response = make_response("<h1>Success</h1>", 200)
        else:
            logger.error(
                f"Error encountered when trying to delete the user {email}")
            response = make_response("<h1>Error</h1>", 404)
    else:
        response = make_response("<h1>Error</h1>", 404)
    return response


@app.route('/update_transaction', methods=['POST'])
def update_transaction():
    logger.info("New update transaction request")
    if 'buyer_email' in request.form:
        buyer_email = request.form.get('buyer_email')
        seller_email = request.form.get('seller_email')
        product_name = request.form.get('product_name')
        product_id = request.form.get('product_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
    else:
        payload = request.get_json()
        buyer_email = payload.get('buyer_email')
        seller_email = payload.get('seller_email')
        product_name = payload.get('product_name')
        product_id = payload.get('product_id')
        price = payload.get('price')
        quantity = payload.get('quantity')
    logger.info(f"New transaction received for buyer: {buyer_email}, seller: {seller_email}, product: {product_name}")
    if database_op.insert_into_transaction(buyer_email, seller_email, product_id, product_name, price, quantity):
        response = make_response("<h1>Success</h1>", 201)
        return response
    else:
        response = make_response("<h1>ERROR</h1>", 200)
        return response


@app.route('/shall_i_buy_this', methods=['GET'])
def decide():
    logger.info("New decision begins")
    response = json.loads(requests.get('https://yesno.wtf/api').content)
    img = response['image']
    print(img)
    return render_template('decision.html', user_image=img)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
