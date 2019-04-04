from flask import Flask, jsonify, make_response, request, Blueprint
from models import User, row2dict, db
# from main import app
import sqlalchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'here is my secret key'
userView = Blueprint("userView", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*arg, **keywordargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *arg, **keywordargs)
    return decorated


@userView.route("/users", methods={"GET"})
@token_required
def get_all_user(current_user):
    user_list = User.query.all()
    return jsonify([row2dict(user) for user in user_list])


@userView.route("/user/<user_id>", methods={"GET"})
@token_required
def get_user(current_user, user_id):
    # id is a primary key, so we'll have max 1 result row
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(row2dict(user))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this user id."}), 404)


@userView.route("/user/create", methods={"POST"})
# @token_required
def create_user():
    # get the name first, if no name then fail
    data = request.get_json()
    name = data['name']
    hashed_password = generate_password_hash(data['password'], method='sha256')

    if name is None or hashed_password is None:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot create new user. Missing mandatory fields."}), 403)
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=True)

    db.session.add(new_user)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot add new user. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "new user created successfully!"})


@userView.route("/user/update/<user_id>", methods={"PUT"})
@token_required
def update_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot update, user not found."}), 404)

    name = request.form.get("name")
    password = request.form.get("password")
    if name is None and password is None:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot update user. Missing mandatory fields."}), 403)
    elif name is None:
        user.password = password
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update user. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "data": {"id": user_id, "user_name": user.user_name, "password": password}})
    elif password is None:
        user.user_name = name
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update user. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "data": {"id": user_id, "user_name": name, "password": user.password}})
    else:
        user.user_name = name
        user.password = password
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update user. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "data": {"id": user_id, "user_name": name, "password": password}})


@userView.route("/user/delete/<user_id>", methods={"DELETE"})
@token_required
def delete_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot delete, user not found."}), 404)
    db.session.delete(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot delete user. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


@userView.route("/login", methods={"GET"})
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate" : "Basic realm='Login required!'"})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})

    if check_password_hash(user.password, auth.password):
        print(app.config['SECRET_KEY'])
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})