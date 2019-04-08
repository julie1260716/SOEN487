from flask import jsonify, request, make_response, render_template, redirect
from profile.database_profile_profile import db, row2dict, profile
from flask import Blueprint
import sqlalchemy.exc

profiles_blueprint = Blueprint("profiles", __name__)


@profiles_blueprint.route("/profile")
def get_all_profiles():
    """Return information for all profiles stored in the database"""
    profile_list = profile.query.all()
    return jsonify([row2dict(profile) for profile in profile_list])


@profiles_blueprint.route("/profile/<movie_name>")
def get_profile_by_name(movie_name):
    """Return profile information by movie name of a profile"""
    profile = profile.query.filter_by(movie_name=movie_name).first()
    if profile:
        return jsonify(row2dict(profile))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find the profile with this movie name."}), 404)


@profiles_blueprint.route("/profile/<int:profile_id>")
def get_profile(profile_id):
    """Return profile information by profile id, this function is created for administer's use"""
    profile = profile.query.filter_by(profile_id=profile_id).first()
    if profile:
        return jsonify(row2dict(profile))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this profile id."}), 404)


@profiles_blueprint.route("/profile", methods={"POST"})
def create_profile():
    """This function is created for administer's use"""
    movie_name = request.form.get("movie_name")
    theater_loc = request.form.get("theater_loc")
    show_time = request.form.get("show_time")
    # profile_number = request.form.get("profile_number")

    if not movie_name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put profile. Missing mandatory fields."}), 403)

    # check if the profile with the given movie has existed
    profile = profile.query.filter_by(movie_name=movie_name).first()
    if profile:
        return make_response(jsonify({"code": 403,
                                      "msg": "profile with this movie name has existed"}), 403)
    else:
        profile = profile(movie_name=movie_name, theater_loc=theater_loc, show_time=show_time)

    db.session.add(profile)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 404, "msg": str(error)}), 404)
    return jsonify({"code": 200, "msg": "success"})


@profiles_blueprint.route("/profile/update", methods={"PUT"})
def update_profile():
    """Update profile by id or movie name, this function is created for administer's use"""
    # get the movie name first, if no movie name then fail
    profile_id = request.form.get("profile_id")
    movie_name = request.form.get("movie_name")
    theater_loc = request.form.get("theater_loc")
    show_time = request.form.get("show_time")
    # profile_number = request.form.get("profile_number")

    if not profile_id and not movie_name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot update profile. Missing mandatory fields."}), 403)

    if profile_id:
        profile = profile.query.filter_by(profile_id=profile_id).first()
    else:
        profile = profile.query.filter_by(movie_name=movie_name).first()

    if not profile:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this profile."}), 404)

    if theater_loc:
        profile.theater_loc = theater_loc
    if show_time:
        profile.show_time = show_time
    # profile.profile_number = profile_number

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as error:
        return make_response(jsonify({"code": 500, "msg": str(error)}), 500)
    return jsonify({"code": 200, "msg": "success"})


@profiles_blueprint.route("/profile/delete", methods={"POST"})
def delete_profile():
    """Delete profile by id, this function is created for administer's use"""
    profile_id = request.form.get("profile_id")
    profile = profile.query.filter_by(profile_id=profile_id).first()
    if profile:
        db.session.delete(profile)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as error:
            return make_response(jsonify({"code": 500, "msg": str(error)}), 500)
        return jsonify({"code": 200, "msg": "profile is successfully deleted"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this profile id."}), 404)


@profiles_blueprint.route("/profile-profile", methods={"POST"})
def book_profile():
    # Step 1: locate the profile based on the data sent from the form
    form = profileprofileForm()
    if form.validate_on_submit():
        movie_name = form.movie_name.data
        theater_loc = form.theater_loc.data
        show_time = form.show_time.data

        profile = profile.query.filter_by(movie_name=movie_name, theater_loc=theater_loc, show_time=show_time).first()
        if profile:
            print("profile Found, profile ID: {}".format(profile.profile_id))
        else:
            print("Cannot find the profile")

        # Step 2: check whether or not the user has logged in
        # TODO: send request to auth service to verify user's status

        # Step 3: insert the profile profile data to profile table
        user_id = 1         # set user_id as 1 for test purpose, it needs to come from session
        profile_id = 1       # set profile_id as 1 for test purpose, it needs to equal to profile.profile_id
        profile_qty = 2      # set profile_qty as 1 for test purpose, it needs to come from form
        profile_data = profile(user_id=user_id, profile_id=profile_id, profile_qty=profile_qty)

        db.session.add(profile_data)

        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as error:
            return make_response(jsonify({"code": 500, "msg": str(error)}), 500)

        return render_template("profile.html")
    else:
        # probably add code to display a message box saying invalid input
        return redirect("profile.html")
