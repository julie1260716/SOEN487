from flask import jsonify, make_response, render_template, request
from recommendation_service.database_recommendation import db, row2dict, Recommendation
from flask import Blueprint
import requests
from functools import wraps
import sqlalchemy.exc

recommendations_blueprint = Blueprint("recommendations", __name__)

AUTH_URL = 'http://127.0.0.1:5000/auth/check'

USER_PROFILE_URL = 'http://127.0.0.1:5003/profile/'
GET_PROFILE_RATING_URL = 'http://127.0.0.1:5003/profile-rating/'
GET_PROFILE_GENRE_URL = 'http://127.0.0.1:5003/profile-genre/'
GET_PROFILE_ACTOR_URL = 'http://127.0.0.1:5003/profile-actor/'
GET_PROFILE_DIRECTOR_URL = 'http://127.0.0.1:5003/profile-director/'
GET_PROFILE_STUDIO_URL = 'http://127.0.0.1:5003/profile-studio/'
GET_PROFILE_LENGTH_URL = 'http://127.0.0.1:5003/profile-length/'

GET_MOVIE_RATING_URL = 'http://127.0.0.1:5002/movie-rating/'
GET_MOVIE_GENRE_URL = 'http://127.0.0.1:5002/movie-genre/'
GET_MOVIE_ACTOR_URL = 'http://127.0.0.1:5002/movie-actor/'
GET_MOVIE_DIRECTOR_URL = 'http://127.0.0.1:5002/movie-director/'
GET_MOVIE_STUDIO_URL = 'http://127.0.0.1:5002/movie-studio/'
GET_MOVIE_LENGTH_URL = 'http://127.0.0.1:5002/movie-length/'
GET_MOVIE_BY_ID_URL = 'http://127.0.0.1:5002/movie/'

GET_ACTOR_ID_URL = 'http://127.0.0.1:5002/movie-actor-id/'
GET_DIRECTOR_ID_URL = 'http://127.0.0.1:5002/movie-director-id/'
GET_MOVIE_INFO_URL = 'http://127.0.0.1:5002/movie-info/'


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
            return render_template("recommendations.html", user_not_login=True)

        headers = {'content-type': 'application/json', 'x-access-token': token}

        try:
            response = requests.get(AUTH_URL, headers=headers)
            current_user = response.json()["current_user_info"]
            if response.status_code == 401:
                return render_template("recommendations.html", user_not_login=True)
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
    """Return recommendation information by movie name of a recommendation"""
    recommendation = Recommendation.query.filter_by(user_id=user_id).first()
    if recommendation:
        return jsonify(row2dict(recommendation))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find any recommendations for this user."}), 404)


@recommendations_blueprint.route('/recommendations.html')
@token_required
def recommendation_page():

    # fetch the profile id based on the current user id from user profile service
    # if the current user id has already fetched the profile data before then go to next step
    user_id = 1
    req_url = USER_PROFILE_URL + str(user_id)
    profile_resp = requests.get(req_url)
    profile_id = profile_resp.json()['profile_id']

    # fetch all attribute ids related to a profile id
    # fetch rating ids
    rating_req_url = GET_PROFILE_RATING_URL + profile_id
    rating_ids = requests.get(rating_req_url).json()['rating_id']
    print("rating: " + str(rating_ids))

    # fetch genre ids
    genre_req_url = GET_PROFILE_GENRE_URL + profile_id
    genre_ids = requests.get(genre_req_url).json()['genre_id']
    print("genre: " + str(genre_ids))

    # fetch actor ids
    actor_req_url = GET_PROFILE_ACTOR_URL + profile_id
    actor_name = requests.get(actor_req_url).json()['actor_name']
    print("actor: " + actor_name)

    # fetch director ids
    director_req_url = GET_PROFILE_DIRECTOR_URL + profile_id
    director_name = requests.get(director_req_url).json()['director_name']
    print("director: " + director_name)

    # fetch studio ids
    studio_req_url = GET_PROFILE_STUDIO_URL + profile_id
    studio_ids = requests.get(studio_req_url).json()['studio_id']
    print("studio: " + str(studio_ids))

    # fetch length ids
    length_req_url = GET_PROFILE_LENGTH_URL + profile_id
    length_ids = requests.get(length_req_url).json()['length_id']
    print("length: " + str(length_ids))

    # fetch all movie ids based on the attributes obtained above
    # fetch movie ids by rating id
    rm_req_url = GET_MOVIE_RATING_URL + rating_ids
    rating_movie_ids = requests.get(rm_req_url).json()['movie_id']
    print("rating_movie_ids: " + str(rating_movie_ids))

    # fetch movie ids by genre id
    gm_req_url = GET_MOVIE_GENRE_URL + genre_ids
    genre_movie_ids = requests.get(gm_req_url).json()['movie_id']
    print("genre_movie_ids: " + str(genre_movie_ids))

    # fetch movie ids by actor id
    actor_id_url = GET_ACTOR_ID_URL + actor_name
    actor_ids = requests.get(actor_id_url).json()['actor_id']
    am_req_url = GET_MOVIE_ACTOR_URL + actor_ids
    actor_movie_ids = requests.get(am_req_url).json()['movie_id']
    print("actor_movie_ids: " + str(actor_movie_ids))

    # fetch movies ids by director id
    dir_id_url = GET_DIRECTOR_ID_URL + director_name
    director_ids = requests.get(dir_id_url).json()['director_id']
    dm_req_url = GET_MOVIE_DIRECTOR_URL + director_ids
    director_movie_ids = requests.get(dm_req_url).json()['movie_id']
    print("director_movie_ids: " + str(director_movie_ids))

    # fetch movies ids by studio id
    sm_req_url = GET_MOVIE_STUDIO_URL + studio_ids
    studio_movie_ids = requests.get(sm_req_url).json()['movie_id']
    print("studio_movie_ids: " + str(studio_movie_ids))

    # fetch movies ids by length id
    lm_req_url = GET_MOVIE_STUDIO_URL + length_ids
    length_movie_ids = requests.get(lm_req_url).json()['movie_id']
    print("length_movie_ids: " + str(length_movie_ids))

    movie_ids = set()
    movie_ids.add(rating_movie_ids)
    movie_ids.add(genre_movie_ids)
    movie_ids.add(actor_movie_ids)
    movie_ids.add(rating_movie_ids)
    movie_ids.add(director_movie_ids)
    movie_ids.add(studio_movie_ids)
    movie_ids.add(length_movie_ids)
    print(movie_ids)

    # if have not stored movie ids before, then store them in the table
    for movie_id in movie_ids:
        db.session.add(Recommendation(user_id=user_id, movie_id=movie_id))

    db.session.commit()

    # fetch movie names from movie service and prepare the data to render html template
    movie_names = []
    for movie_id in movie_ids:
        movie_req_url = GET_MOVIE_BY_ID_URL + movie_id
        movie_resp = requests.get(movie_req_url)
        movie_name = movie_resp.json()['movie_name']
        movie_names.append(movie_name)

    print(movie_names)
    return render_template("recommendations.html", movie_names=movie_names, movie_url=GET_MOVIE_INFO_URL)

