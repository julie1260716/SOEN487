from flask import jsonify, request, make_response, render_template, redirect
from user_profile.database_profile import db, row2dict, Profile, MovieProfileForm
from user_profile.database_profile import Rating2Profile, Genre2Profile, Actor2Profile, Director2Profile
from user_profile.database_profile import Studio2Profile, Length2Profile
from flask import Blueprint
from functools import wraps
import requests
import sqlalchemy.exc

profiles_blueprint = Blueprint("profiles", __name__)

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
            return render_template("booking.html", form=form, user_not_login=True)

        headers = {'content-type': 'application/json', 'x-access-token': token}

        try:
            response = requests.get(AUTH_URL, headers=headers)
            current_user = response.json()["current_user_info"]
            if response.status_code == 401:
                form = MovieProfileForm()
                return render_template("booking.html", form=form, user_not_login=True)
            return func(current_user, *arg, **keywordargs)
        except Exception as e:
            return make_response(jsonify({'code': 500, 'msg': str(e)}), 500)
        return func(current_user, *arg, **keywordargs)
    return wrapper


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


@profiles_blueprint.route("/profile-rating/<profile_id>")
def get_ratings_by_profile_id(profile_id):
    """Return rating information of the given profile id"""
    rating = Rating2Profile.query.filter_by(profile_id=profile_id).first()
    if rating:
        return jsonify(row2dict(rating))
    else:
        return make_response(jsonify({"code": 404, "msg": "No rating data fetched"}), 404)


@profiles_blueprint.route("/profile-genre/<profile_id>")
def get_genres_by_profile_id(profile_id):
    """Return genre information of the given profile id"""
    genre = Genre2Profile.query.filter_by(profile_id=profile_id).first()
    if genre:
        return jsonify(row2dict(genre))
    else:
        return make_response(jsonify({"code": 404, "msg": "No genre data fetched"}), 404)


@profiles_blueprint.route("/profile-actor/<profile_id>")
def get_actors_by_profile_id(profile_id):
    """Return actor information of the given profile id"""
    actor = Actor2Profile.query.filter_by(profile_id=profile_id).first()
    if actor:
        return jsonify(row2dict(actor))
    else:
        return make_response(jsonify({"code": 404, "msg": "No actor data fetched"}), 404)


@profiles_blueprint.route("/profile-director/<profile_id>")
def get_directors_by_profile_id(profile_id):
    """Return director information of the given profile id"""
    director = Director2Profile.query.filter_by(profile_id=profile_id).first()
    if director:
        return jsonify(row2dict(director))
    else:
        return make_response(jsonify({"code": 404, "msg": "No director data fetched"}), 404)


@profiles_blueprint.route("/profile-studio/<profile_id>")
def get_studios_by_profile_id(profile_id):
    """Return studio information of the given profile id"""
    studio = Studio2Profile.query.filter_by(profile_id=profile_id).first()
    if studio:
        return jsonify(row2dict(studio))
    else:
        return make_response(jsonify({"code": 404, "msg": "No studio data fetched"}), 404)


@profiles_blueprint.route("/profile-length/<profile_id>")
def get_lengths_by_profile_id(profile_id):
    """Return director information of the given profile id"""
    length = Length2Profile.query.filter_by(profile_id=profile_id).first()
    if length:
        return jsonify(row2dict(length))
    else:
        return make_response(jsonify({"code": 404, "msg": "No length data fetched"}), 404)


@profiles_blueprint.route("/create-profile", methods={"POST"})
def create_profile():
    form = MovieProfileForm()
    profile_id = 1

    if form.validate_on_submit():
        # getting ratings
        ratingG = form.ratingG.data
        if ratingG:
            db.session.add(Rating2Profile(profile_id=profile_id, rating_id=1))

        ratingPG = form.ratingPG.data
        if ratingPG:
            db.session.add(Rating2Profile(profile_id=profile_id, rating_id=2))

        ratingPG13 = form.ratingPG13.data
        if ratingPG13:
            db.session.add(Rating2Profile(profile_id=profile_id, rating_id=3))

        ratingR = form.ratingR.data
        if ratingR:
            db.session.add(Rating2Profile(profile_id=profile_id, rating_id=4))

        # getting genres
        genreAction = form.genreAction.data
        if genreAction:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=1))

        genreAdventure = form.genreAdventure.data
        if genreAdventure:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=2))

        genreAnimation = form.genreAnimation.data
        if genreAnimation:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=3))

        genreComedy = form.genreComedy.data
        if genreComedy:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=4))

        genreCrime = form.genreCrime.data
        if genreCrime:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=5))

        genreDrama = form.genreDrama.data
        if genreDrama:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=6))

        genreFantasy = form.genreFantasy.data
        if genreFantasy:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=7))

        genreFiction = form.genreFiction.data
        if genreFiction:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=8))

        genreHorror = form.genreHorror.data
        if genreHorror:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=9))

        genreMystery = form.genreMystery.data
        if genreMystery:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=10))

        genrePolitical = form.genrePolitical.data
        if genrePolitical:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=11))

        genreRomance = form.genreRomance.data
        if genreRomance:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=12))

        genreThriller = form.genreThriller.data
        if genreThriller:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=13))

        genreSciFi = form.genreSciFi.data
        if genreSciFi:
            db.session.add(Genre2Profile(profile_id=profile_id, genre_id=14))

        # getting actors
        actor1 = form.actor1.data
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor1))

        actor2 = form.actor2.data
        if actor2 != "":
            db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor2))

        actor3 = form.actor3.data
        if actor3 != "":
            db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor3))

        actor4 = form.actor4.data
        if actor4 != "":
            db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor4))

        actor5 = form.actor5.data
        if actor5 != "":
            db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor5))

        actor6 = form.actor6.data
        if actor6 != "":
            db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor6))

        # getting directors
        director1 = form.director1.data
        db.session.add(Director2Profile(profile_id=profile_id, director_name=director1))

        director2 = form.director2.data
        if director2 != "":
            db.session.add(Director2Profile(profile_id=profile_id, director_name=director2))

        director3 = form.director3.data
        if director3 != "":
            db.session.add(Director2Profile(profile_id=profile_id, director_name=director3))

        # getting studio
        studioWarn = form.studioWarn.data
        if studioWarn:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=1))

        studioSony = form.studioSony.data
        if studioSony:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=2))

        studioWalt = form.studioWalt.data
        if studioWalt:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=3))

        studio20 = form.studio20.data
        if studio20:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=4))

        studioUniversal = form.studioUniversal.data
        if studioUniversal:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=5))

        studioParamount = form.studioParamount.data
        if studioParamount:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=6))

        studioLionsgate = form.studioLionsgate.data
        if studioLionsgate:
            db.session.add(Studio2Profile(profile_id=profile_id, studio_id=7))

        # getting length
        length60 = form.length60.data
        if length60:
            db.session.add(Length2Profile(profile_id=profile_id, length_id=1))

        length90 = form.length90.data
        if length90:
            db.session.add(Length2Profile(profile_id=profile_id, length_id=2))

        length120 = form.length120.data
        if length120:
            db.session.add(Length2Profile(profile_id=profile_id, length_id=3))

        lengthover120 = form.lengthover120.data
        if lengthover120:
            db.session.add(Length2Profile(profile_id=profile_id, length_id=4))

        # commit changes to the db
        db.session.commit()

        return render_template("profile.html", form=form)

    else:
        print("error found!")
        print(form.errors.items())  # display the form errors
        # probably add code to display a message box saying invalid input
        return render_template("profile.html", form=form)

