from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import Form, BooleanField, StringField, validators

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/ProfileDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()
# # TODO: GET THE CURRENT USER ID AND NEXT VALID PROFILE ID
# user_id = 1
# profile_id = 2


# mysql-> rating to profile table
class Rating2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      rating_id: a unique id representing the ratings chosen by the user
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, primary_key=True)


# mysql-> genre to profile table
class Genre2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      genre_id: a unique id representing the genres chosen by the user
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, primary_key=True)


# mysql-> actors to profile table
class Actor2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      actor_name: string representing the actor's name
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String(128), primary_key=True)


# mysql-> actors to profile table
class Director2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      director_name: string representing the director's name
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(128), primary_key=True)


# mysql-> studios to profile table
class Studio2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      studio_id: a unique id representing the studio preferred by that user
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, primary_key=True)


# mysql-> length to profile table
class Length2Profile(db.Model):
    """
      profile_id: a unique id representing the profile for that user
      length_id: a unique id representing the movie lengths preferred by that user
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    length_id = db.Column(db.Integer, primary_key=True)


# mysql-> profile table
class Profile(db.Model):
    """
    ** The Profile table maps specific users preferences(e.g. genres, actors, ratings, studios, etc)
    ** 1 users is recommended 1 profile
      profile_id: a unique id representing the profile for that user
      user_id: a unique id representing a user
    """
    user_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<Profile {} {}>".format(self.user_id, self.profile_id)


# Defining a Profile form to check the validation of inputs
# we will use the information gathered to save to the user's movie profile
class MovieProfileForm(FlaskForm):
    # checkboxes for rating
    ratingG = BooleanField("ratingG")
    ratingPG = BooleanField("ratingPG")
    ratingPG13 = BooleanField("ratingPG13")
    ratingR = BooleanField("ratingR")

    # checkboxes for genre
    genreAction = BooleanField("genreAction")
    genreAdventure = BooleanField("genreAdventure")
    genreAnimation = BooleanField("genreAnimation")
    genreComedy = BooleanField("genreComedy")
    genreCrime = BooleanField("genreCrime")
    genreDrama = BooleanField("genreDrama")
    genreFantasy = BooleanField("genreFantasy")
    genreFiction = BooleanField("genreFiction")
    genreHorror = BooleanField("genreHorror")
    genreMystery = BooleanField("genreMystery")
    genrePolitical = BooleanField("genrePolitical")
    genreRomance = BooleanField("genreRomance")
    genreThriller = BooleanField("genreThriller")
    genreSciFi = BooleanField("genreSciFi")

    # inputs for actors
    actor1 = StringField("actor1", validators=[DataRequired(message="An actor is required"), Length(max=255)])
    actor2 = StringField("actor2", validators=[Length(max=255)])
    actor3 = StringField("actor3", validators=[Length(max=255)])
    actor4 = StringField("actor4", validators=[Length(max=255)])
    actor5 = StringField("actor5", validators=[Length(max=255)])
    actor6 = StringField("actor6", validators=[Length(max=255)])

    # inputs for directors
    director1 = StringField("director1", validators=[DataRequired(message="A director is required"), Length(max=255)])
    director2 = StringField("director2", validators=[Length(max=255)])
    director3 = StringField("director3", validators=[Length(max=255)])

    # checkboxes for studios
    studioWarn = BooleanField("studioWarn")
    studioSony = BooleanField("studioSony")
    studioWalt = BooleanField("studioWalt")
    studio20 = BooleanField("studio20")
    studioUniversal = BooleanField("studioUniversal")
    studioParamount = BooleanField("studioParamount")
    studioLionsgate = BooleanField("studioLionsgate")

    # checkboxes for movie length
    length60 = BooleanField("length60")
    length90 = BooleanField("length90")
    length120 = BooleanField("length120")
    lengthover120 = BooleanField("lengthover120")


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for profile service
def init_database():
    db.drop_all()
    db.create_all()
    init_profile_table()
    init_rating_profile_table()
    init_genre_profile_table()
    init_actor_profile_table()
    init_director_profile_table()
    init_studio_profile_table()
    init_length_profile_table()


# Populate the profile table
def init_profile_table():
    # Populate profile table (HARD CODED version)
    # TODO: write code to automatically populate the profile
    db.session.add(Profile(user_id=1, profile_id=1))
    # here we can conclude that user 2 did not create a profile yet
    db.session.add(Profile(user_id=3, profile_id=2))
    db.session.commit()


# Populate Rating2Profile table
def init_rating_profile_table():
    db.session.add(Rating2Profile(profile_id=1, rating_id=1))
    db.session.commit()


# Populate Genre2Profile table
def init_genre_profile_table():
    db.session.add(Genre2Profile(profile_id=1, genre_id=1))
    db.session.commit()


# Populate Actor2Profile table
def init_actor_profile_table():
    db.session.add(Actor2Profile(profile_id=1, actor_name="Kirsten Bell"))
    db.session.commit()


# Populate Director2Profile table
def init_director_profile_table():
    db.session.add(Director2Profile(profile_id=1, director_name="Chris Buck"))
    db.session.commit()


# Populate Studio2Profile table
def init_studio_profile_table():
    db.session.add(Studio2Profile(profile_id=1, studio_id=1))
    db.session.commit()


# Populate Length2Profile table
def init_length_profile_table():
    db.session.add(Length2Profile(profile_id=1, length_id=1))
    db.session.commit()


# Add the user's profile to the profile database
# def add_a_profile():
#     db.session.add(Profile(user_id=user_id, profile_id=profile_id))
#     db.session.commit()

