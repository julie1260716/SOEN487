from flask import jsonify, request, make_response, render_template, redirect
from user_profile.database_profile import db, row2dict, Profile
from flask import Blueprint
import sqlalchemy.exc

profiles_blueprint = Blueprint("profiles", __name__)


@profiles_blueprint.route("/profile")
def get_all_profiles():
    """Return information for all user profiles stored in the database"""
    profile_list = Profile.query.all()
    return jsonify([row2dict(profile) for profile in profile_list])


@profiles_blueprint.route("/profile/<user_id>")
def get_profile_by_user_id(user_id):
    """Return profile information of the given user id"""
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        return jsonify(row2dict(profile))
    else:
        return make_response(jsonify({"code": 404, "msg": "This user has not created any movie profile."}), 404)
