from flask import jsonify, request, make_response, render_template, redirect
from database_user import db, row2dict, User
from flask import Blueprint
import sqlalchemy.exc
from functools import wraps
import requests

users_blueprint = Blueprint("userView", __name__)
# that url may be changed later on
AUTH_URL = 'http://127.0.0.1:5000/auth/check'
AUTH_URL_DELETE = 'http://127.0.0.1:5000/auth/delete'


def token_required(func):
    """
    verify token
    """
    @wraps(func)
    def wrapper(*arg, **keywordargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            # return render_template("login.html")
            return make_response(jsonify({'code': 401, 'msg': "Token invalid"}), 401)

        headers = {'content-type': 'application/json',
                   'x-access-token': token}
        try:
            response = requests.get(AUTH_URL, headers=headers)
            current_user = response.json()["current_user_info"]
            if response.status_code == 401:
                return make_response(jsonify({'code': 401, 'msg': "Token invalid"}), 401)
                # return render_template("login.html")
            return func(current_user, *arg, **keywordargs)
        except:
            return make_response(jsonify({'code': 404, 'msg': "Whoops, something went wrong"}), 404)
        return func(current_user, *arg, **keywordargs)
    return wrapper


# Create new user profile
@users_blueprint.route("/user", methods={"POST"})
def create_user():
    """create new user profile"""
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


@users_blueprint.route("/user")
@token_required
def get_all_tickets(current_user):
    """
    Return information for all users stored in the database,
    only admin have the permission to delete user
    """

    if current_user["admin"] == False:
        return make_response(jsonify({"code": 403, "msg": "You don't have the permission to delete the profile"}),
                             403)
    user_list = User.query.all()
    return jsonify([row2dict(ticket) for ticket in user_list])


@users_blueprint.route("/user/<user_id>")
@token_required
def get_user(current_user, user_id):
    """get user profile by public_id, user can only view his/her own profile """
    if current_user["public_id"] != user_id:
        return make_response(jsonify({"code": 403, "msg": "You don't have the permission to view the requested URL"}),
                             403)
    user = User.query.filter_by(public_id=user_id).first()
    if user:
        # return jsonify(row2dict(user))
        userinfo = row2dict(user)
        return render_template("user_profile.html", user=userinfo)
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find user profile with this user_id."}), 404)


@users_blueprint.route("/user/<user_id>", methods={"PUT"})
@token_required
def update_user(current_user, user_id):
    """Edit personal information, user can only update his/her own profile"""
    #
    if current_user["public_id"] != user_id:
        return make_response(jsonify({"code": 403, "msg": "You don't have the permission to update the profile"}),
                             403)
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

@users_blueprint.route("/user/update-email/<user_id>", methods={"PUT"})
def update_user(user_id):
    """update email from auth service"""
    email = request.get_json()['email']
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot update, user not found."}), 404)
    user.email = email
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "update success"})


@users_blueprint.route("/user/<user_id>", methods={"DELETE"})
@token_required
def delete_user(current_user, user_id):
    """only admin have the permission to delete user"""
    if current_user["admin"] == False:
        return make_response(jsonify({"code": 403, "msg": "You don't have the permission to delete the profile"}),
                             403)
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return make_response(jsonify({"code": 404,
                                      "msg": "Cannot delete, user not found."}), 404)
    db.session.delete(user)
    try:
        response = forward_delete_auth(current_user['user_token'], user_id)
        if response.status_code == 200:
            db.session.commit()
        else:
            return make_response(jsonify({"code": 404, "msg": "Something went wrong!"}), 404)
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "delete success"})


def forward_delete_auth(token, public_id):
    url = AUTH_URL_DELETE
    headers = {'content-type': 'application/json',
               'x-access-token': token }
    # print(url)
    try:
        print("before request")
        response = requests.delete(url+'/'+public_id, headers=headers)
        print("after request")
    except:
        print("i am inside catch block")
        # return jsonify(dict(code=404, msg="whoops! something went wrong!!"))
        return make_response(jsonify({"code": 404, "msg": "bad request"}), 404)
    return make_response(jsonify({"code": 200, "msg": "success"}), 200)