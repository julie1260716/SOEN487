from flask import jsonify, request, make_response, render_template, redirect
from movie_service.database_movie import db, row2dict, GenreOfMovie, ActsIn, DirectorOf, StudioOf
from movie_service.database_movie import Movie, Actor, Director
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


@movies_blueprint.route("/movie-rating/<rating_id>")
def get_movie_by_rating_id(rating_id):
    """Return movie information of the given rating id"""
    movie = Movie.query.filter_by(movie_rating=rating_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@movies_blueprint.route("/movie-length/<length_id>")
def get_movie_by_length_id(length_id):
    """Return movie information of the given length id"""
    movie = Movie.query.filter_by(movie_length=length_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@movies_blueprint.route("/movie-genre/<genre_id>")
def get_movie_by_genre_id(genre_id):
    """Return movie information of the given genre id"""
    movie = GenreOfMovie.query.filter_by(genre_id=genre_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@movies_blueprint.route("/movie-actor/<actor_id>")
def get_movie_by_actor_id(actor_id):
    """Return movie information of the given actor id"""
    movie = ActsIn.query.filter_by(actor_id=actor_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@movies_blueprint.route("/movie-actor-id/<actor_name>")
def get_actor_id_by_name(actor_name):
    """Return movie information of the given actor id"""
    actor = Actor.query.filter_by(actor_name=actor_name).first()
    if actor:
        return jsonify(row2dict(actor))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any actor under this name."}), 404)


@movies_blueprint.route("/movie-director/<director_id>")
def get_movie_by_director_id(director_id):
    """Return movie information of the given director id"""
    movie = DirectorOf.query.filter_by(director_id=director_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)


@movies_blueprint.route("/movie-director-id/<director_name>")
def get_director_id_by_name(director_name):
    """Return movie information of the given actor id"""
    director = Director.query.filter_by(director_name=director_name).first()
    if director:
        return jsonify(row2dict(director))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any director under this name."}), 404)


@movies_blueprint.route("/movie-studio/<studio_id>")
def get_movie_by_studio_id(studio_id):
    """Return movie information of the given studio id"""
    movie = StudioOf.query.filter_by(studio_id=studio_id).first()
    if movie:
        return jsonify(row2dict(movie))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any movies under this id."}), 404)









