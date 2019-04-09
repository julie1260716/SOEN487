from flask import jsonify, request, make_response, render_template, redirect
from recommendation_service.database_recommendation import db, row2dict, Recommendation
from flask import Blueprint
import sqlalchemy.exc

recommendations_blueprint = Blueprint("recommendations", __name__)


@recommendations_blueprint.route("/recommendation")
def get_all_recommendations():
    """Return information for all recommendations stored in the database"""
    recommendation_list = Recommendation.query.all()
    return jsonify([row2dict(recommendation) for recommendation in recommendation_list])


@recommendations_blueprint.route("/recommendation/<user_id>")
def get_recommendation_by_user_id(user_id):
    """Return recommendation information by movie name of a recommendation"""
    recommendation = Recommendation.query.filter_by(user_id=user_id).first()
    if recommendation:
        return jsonify(row2dict(recommendation))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any recommendations for this user."}), 404)
