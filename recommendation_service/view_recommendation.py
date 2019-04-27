from functools import wraps

import requests
from flask import jsonify, request, make_response, render_template, redirect

from movie_service.database_movie import Movie
from recommendation_service.database_recommendation import db, row2dict, Recommendation
from flask import Blueprint
import sqlalchemy.exc

from user_profile.database_profile import MovieProfileForm

recommendations_blueprint = Blueprint("recommendations", __name__)


AUTH_URL = 'http://127.0.0.1:5000/auth/check'


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
            form = MovieProfileForm()
            return render_template("profile.html", form=form, user_not_login=True)

        headers = {'content-type': 'application/json', 'x-access-token': token}

        try:
            response = requests.get(AUTH_URL, headers=headers)
            current_user = response.json()["current_user_info"]
            if response.status_code == 401:
                form = MovieProfileForm()
                return render_template("profile.html", form=form, user_not_login=True)
            return func(current_user, *arg, **keywordargs)
        except Exception as e:
            return make_response(jsonify({'code': 500, 'msg': str(e)}), 500)
        return func(current_user, *arg, **keywordargs)
    return wrapper


@recommendations_blueprint.route("/recommendation")
def get_all_recommendations():
    """Return information for all recommendations stored in the database"""
    recommendation_list = Recommendation.query.all()
    return jsonify([row2dict(recommendation) for recommendation in recommendation_list])


@recommendations_blueprint.route("/recommendation/<user_id>")
def get_recommendation_by_user_id(user_id):
    """Return recommendation information of the given user id"""
    recommendation = Recommendation.query.filter_by(user_id=user_id).first()
    if recommendation:
        return jsonify(row2dict(recommendation))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any recommendations for this user."}), 404)


@recommendations_blueprint.route("/recommendation/<movie_id>")
def get_movie_by_id(movie_id):
    """Return recommendation information by movie id"""
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@recommendations_blueprint.route("/recommendation-table")
def get_all_recommendation_data():
    """Return all recommendation data stored in the database"""
    recommendation_list = Recommendation.query.all()
    return jsonify([row2dict(booking_data) for booking_data in recommendation_list])


@recommendations_blueprint.route('/recommendations.html')
def recommendation_table_page():
    """Return all recommendation data stored in the database and display them in HTML page"""
    recommendation_list = Recommendation.query.all()
    recommendation_data = [row2dict(recommendation_data) for recommendation_data in recommendation_list]
    return render_template("recommendations.html", recommendation_data=recommendation_data)

