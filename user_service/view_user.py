from flask import jsonify, request, make_response, render_template, redirect
from database_user import db, row2dict, User
from flask import Blueprint
import sqlalchemy.exc
from functools import wraps
import requests

users_blueprint = Blueprint("userView", __name__)
AUTH_URL = 'http://10.0.9.152:5000/auth/check'


def token_required(func):
    @wraps(func)
    def wrapper(*arg, **keywordargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return render_template("login.html")

        headers = {'content - type': 'application / json',
                   'x-access-token': token}
        try:
            response = requests.get(AUTH_URL, headers=headers)
            if response.status_code == 401:
                return render_template("login.html")
        except:
            return make_response(jsonify({'code': 404, 'msg': "Whoops, something went wrong"}), 404)
        return func(*arg, **keywordargs)
    return wrapper

# Create new user profile
@users_blueprint.route("/user", methods={"POST"})
def create_user():
    # public_id = request.form.get("public_id")
    # first_name = request.form.get("first_name")
    # last_name = request.form.get("last_name")
    # email = request.form.get("email")
    # date_of_birth = request.form.get("date_of_birth")
    # phone_number = request.form.get("phone_number")
    # address = request.form.get("address")
    data = request.get_json()
    public_id = data['public_id']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    date_of_birth = data['date_of_birth']
    phone_number = data['phone_number']
    address = data['address']
    # address could be none, other fields are mandatory
    if first_name is None or last_name is None or email is None or public_id is None \
            or date_of_birth is None or phone_number is None:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot create new user profile. Missing mandatory fields."}), 403)
    new_user = User(public_id=public_id, fname=first_name,
                    lname=last_name, birthday=date_of_birth,
                    email=email, phone=phone_number, address=address)
    db.session.add(new_user)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "success"})


# Get user profile by public_id
@users_blueprint.route("/user/<user_id>")
@token_required
def get_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()
    if user:
        return jsonify(row2dict(user))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find user profile with this user_id."}), 404)


# Edit personal information
@users_blueprint.route("/user/<user_id>", methods={"PUT"})
# @token_required
def update_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot update, user not found."}), 404)
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    date_of_birth = request.form.get("date_of_birth")
    phone_number = request.form.get("phone_number")
    address = request.form.get("address")
    if first_name is None and last_name is None and date_of_birth is None and phone_number is None and address is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Nothing to update."}), 404)
    if first_name is not None:
        user.fname = first_name
    if last_name is not None:
        user.lname = last_name
    if date_of_birth is not None:
        user.birthday = date_of_birth
    if phone_number is not None:
        user.phone = phone_number
    if address is not None:
        user.address = address

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "update success"})


@users_blueprint.route("/user/<user_id>", methods={"DELETE"})
# @token_required
def delete_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot delete, user not found."}), 404)
    db.session.delete(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "delete success"})