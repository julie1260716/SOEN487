from flask import jsonify, request, make_response, render_template, redirect
from movie_service.database_movie import db, row2dict, Movie
from flask import Blueprint
import sqlalchemy.exc

movies_blueprint = Blueprint("movies", __name__)


@movies_blueprint.route("/movie")
def get_all_movies():
    """Return information for all movies stored in the database"""
    movie_list = Movie.query.all()
    return jsonify([row2dict(movie) for movie in movie_list])


@movies_blueprint.route("/movie/<movie_id>")
def get_movie_by_id(movie_id):
    """Return movie information by movie id"""
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)
