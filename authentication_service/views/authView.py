from flask import Flask, jsonify, make_response, request, Blueprint
from models import Auth, row2dict, db
# from main import app
from dotenv import load_dotenv
import os
import sqlalchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
import datetime
from functools import wraps
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'here is my secret key'
authView = Blueprint("authView", __name__)


# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


def token_required(func):
    @wraps(func)
    def wrapper(*arg, **keywordargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Auth.query.filter_by(public_id=data['public_id'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return func(current_user, *arg, **keywordargs)
    return wrapper


def forward_user_info(public_id, first_name, last_name, email, date_of_birth, phone_number, address):
    payload = {
        "public_id": public_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "date_of_birth": date_of_birth,
        "phone_number": phone_number,
        "address": address
    }
    headers = {'content-type' : 'application/json'}
    url = os.environ.get("USER_SERVICE_URL")
    print(url)
    try:
        print("before request")
        response = requests.post(url, headers=headers, json=payload)
        print("after request")
    except:
        print("i am inside catch block")
        # return jsonify(dict(code=404, msg="whoops! something went wrong!!"))
        return make_response(jsonify({"code": 404, "msg": "bad request"}), 404)
    return make_response(jsonify({"code": 200, "msg": "success"}), 200)


@authView.route("/auth/check", methods={"GET"})
def token_verification():
    token = None

    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return jsonify({'message': 'Token is missing'}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = Auth.query.filter_by(public_id=data['public_id'])
    except:
        return jsonify({'message': 'Token is invalid!'}), 401
    return jsonify({"code": 200, "msg": "token has been verified successfully!",
                    'current_user_info': {
                        'email': current_user.first().email,
                        'public_id': current_user.first().public_id,
                        'admin': current_user.first().admin
                        },
                    'user_token': token
                    })


@authView.route("/auth/sign-up", methods={"POST"})
# @token_required
def sign_up():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    date_of_birth = request.form.get('dateOfBirth')
    phone_number = request.form.get('phoneNumber')
    address = request.form.get('address')
    public_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(request.form.get('password'), method='sha256')

    if first_name is None or last_name is None or email is None or hashed_password is None:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot create new user account. Missing mandatory fields."}), 403)
    user = Auth.query.filter_by(email=email).first()
    if user is not None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot create new user account. duplicated email found."}), 404)
    else:
        new_user = Auth(public_id=public_id, email=email, password=hashed_password, admin=False)
        response = forward_user_info(public_id, first_name, last_name, email, date_of_birth, phone_number, address)
        if response.status_code != 404:
            db.session.add(new_user)
            try:
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError as e:
                error = "Cannot add new user. "
                print(app.config.get("DEBUG"))
                if app.config.get("DEBUG"):
                    error += str(e)
                return make_response(jsonify({'code': 404, 'msg': error}), 404)
            return jsonify({"code": 200, "msg": "Your new account has been created successfully!"})
        else:
            return make_response(jsonify({'code': 404, 'msg': "Whoops, something went wrong"}), 404)


@authView.route("/auth/login", methods={"POST"})
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return make_response("Could not verify", 401, {"WWW-Authenticate" : "Basic realm='Login required!'"})

    user = Auth.query.filter_by(email=username).first()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})

    if check_password_hash(user.password, password):
        print(app.config['SECRET_KEY'])
        token = jwt.encode({'public_id': user.public_id,
                            'email': user.email,
                            'admin': user.admin,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY']
                           )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})