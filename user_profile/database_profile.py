from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import Form, BooleanField, StringField, validators

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/ProfileDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()
# TODO: GET THE CURRENT USER ID AND NEXT VALID PROFILE ID
user_id = 1
profile_id = 2;


# mysql-> rating to profile table
class Rating2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      rating_id: a unique id representing the ratings chosen by the user
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating_id = db.Column(db.Integer, nullable=False)


# mysql-> genre to profile table
class Genre2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      genre_id: a unique id representing the genres chosen by the user
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre_id = db.Column(db.Integer, nullable=False)


# mysql-> actors to profile table
class Actor2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      actor_name: string representing the actor's name
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    actor_name = db.Column(db.String, nullable=False)


# mysql-> actors to profile table
class Director2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      director_name: string representing the director's name
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    director_name = db.Column(db.String, nullable=False)


# mysql-> studios to profile table
class Studio2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      studio_id: a unique id representing the studio preferred by that user
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    studio_id = db.Column(db.Integer, nullable=False)


# mysql-> length to profile table
class Length2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      length_id: a unique id representing the movie lengths preferred by that user
    """
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    length_id = db.Column(db.Integer, nullable=False)


# mysql-> profile table
class Profile(db.Model):
    """
    ** The Profile table maps specific users preferences(e.g. genres, actors, ratings, studios, etc)
    ** 1 users is recommended 1 profile
      profile_id: a unique id representing the profile for that user
      user_id: a unique id representing a user
    """
    user_id = db.Column(db.Integer, db.ForeignKey(""), nullable=False)
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return "<Profile {} {}>".format(self.user_id, self.profile_id)


# Defining a Profile form to check the validation of inputs
# we will use the information gathered to save to the user's movie profile
class MovieProfileForm(FlaskForm):

    # getting ratings
    ratingG = BooleanField("ratingG")
    if ratingG:
        db.session.add(Rating2Profile(profile_id=profile_id, rating_id=1))
    ratingPG = BooleanField("ratingPG")
    if ratingPG:
        db.session.add(Rating2Profile(profile_id=profile_id, rating_id=2))
    ratingPG13 = BooleanField("ratingPG13")
    if ratingPG13:
        db.session.add(Rating2Profile(profile_id=profile_id, rating_id=3))
    ratingR = BooleanField("ratingR")
    if ratingR:
        db.session.add(Rating2Profile(profile_id=profile_id, rating_id=4))

    # getting genres
    genreAction = BooleanField("genreAction")
    if genreAction:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=1))
    genreAdventure = BooleanField("genreAdventure")
    if genreAdventure:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=2))
    genreAnimation = BooleanField("genreAnimation")
    if genreAnimation:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=3))
    genreComedy = BooleanField("genreComedy")
    if genreComedy:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=4))
    genreCrime = BooleanField("genreCrime")
    if genreCrime:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=5))
    genreDrama = BooleanField("genreDrama")
    if genreDrama:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=6))
    genreFantasy = BooleanField("genreFantasy")
    if genreFantasy:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=7))
    genreFiction = BooleanField("genreFiction")
    if genreFiction:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=8))
    genreHorror = BooleanField("genreHorror")
    if genreHorror:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=9))
    genreMystery = BooleanField("genreMystery")
    if genreMystery:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=10))
    genrePolitical = BooleanField("genrePolitical")
    if genrePolitical:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=11))
    genreRomance = BooleanField("genreRomance")
    if genreRomance:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=12))
    genreThriller = BooleanField("genreThriller")
    if genreThriller:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=13))
    genreSciFi = BooleanField("genreSciFi")
    if genreSciFi:
        db.session.add(Genre2Profile(profile_id=profile_id, genre_id=14))

    # getting actors
    actor1 = StringField("actor1", validators=[DataRequired(message="An actor is required"), Length(max=255)])
    if actor1 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor1))
    actor2 = StringField("actor2", validators=[Length(max=255)])
    if actor2 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor2))
    actor3 = StringField("actor3", validators=[Length(max=255)])
    if actor3 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor3))
    actor4 = StringField("actor4", validators=[Length(max=255)])
    if actor4 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor4))
    actor5 = StringField("actor5", validators=[Length(max=255)])
    if actor5 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor5))
    actor6 = StringField("actor6", validators=[Length(max=255)])
    if actor6 != "":
        db.session.add(Actor2Profile(profile_id=profile_id, actor_name=actor6))

    # getting directors
    director1 = StringField("dir1", validators=[DataRequired(message="A director is required"), Length(max=255)])
    if director1 != "":
        db.session.add(Director2Profile(profile_id=profile_id, director_name=director1))
    director2 = StringField("dir2", validators=[Length(max=255)])
    if director2 != "":
        db.session.add(Director2Profile(profile_id=profile_id, director_name=director2))
    director3 = StringField("dir3", validators=[Length(max=255)])
    if director3 != "":
        db.session.add(Director2Profile(profile_id=profile_id, director_name=director3))

    # getting studio
    studioWarn = BooleanField("studioWarn")
    if studioWarn:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=1))
    studioSony = BooleanField("studioSony")
    if studioSony:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=2))
    studioWalt = BooleanField("studioWalt")
    if studioWalt:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=3))
    studio20 = BooleanField("studio20")
    if studio20:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=4))
    studioUniversal = BooleanField("studioUniversal")
    if studioUniversal:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=5))
    studioParamount = BooleanField("studioParamount")
    if studioParamount:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=6))
    studioLionsgate = BooleanField("studioLionsgate")
    if studioLionsgate:
        db.session.add(Studio2Profile(profile_id=profile_id, studio_id=7))

    # getting length
    length60 = BooleanField("length60")
    if length60:
        db.session.add(Length2Profile(profile_id=profile_id, length_id=1))
    length90 = BooleanField("length90")
    if length90:
        db.session.add(Length2Profile(profile_id=profile_id, length_id=2))
    length120 = BooleanField("length120")
    if length120:
        db.session.add(Length2Profile(profile_id=profile_id, length_id=3))
    lengthover120 = BooleanField("lengthover120")
    if lengthover120:
        db.session.add(Length2Profile(profile_id=profile_id, length_id=4))

    # commit changes to the db
    db.session.commit()


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for profile service
def init_database():
    db.drop_all()
    db.create_all()
    init_profile_table()


# Populate the profile table
def init_profile_table():
    # Populate profile table (HARD CODED version)
    # TODO: write code to automatically populate the profile
    db.session.add(Profile(user_id=1, profile_id=1))
    # here we can conclude that user 2 did not create a profile yet
    db.session.add(Profile(user_id=3, profile_id=2))
    db.session.commit()


# Add the user's profile to the profile database
def add_a_profile():
    db.session.add(Profile(user_id=user_id, profile_id=profile_id))
    db.session.commit()

