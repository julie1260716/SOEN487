from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/ProfileDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()


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
# NOT TOO SURE WHAT TO DO HERE
class MovieProfileForm(FlaskForm):
    ratingG = BooleanField("ratingG")
    genreAction = BooleanField("genreAction")
    actor1 = StringField("actor1")
    actor2 = StringField("actor2")
    director1 = StringField("director1")
    director2 = StringField("director2")
    studiosWarner = BooleanField("studiosWarner")
    lengthLess60 = BooleanField("lengthLess60")


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

