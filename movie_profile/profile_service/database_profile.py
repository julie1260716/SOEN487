from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from datetime import datetime

# Define mysql database connection string
DATABASE_URI = ""

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()


# mysql-> profile table
class profile(db.Model):
    """
      profile_id: an unique id to locate a profile
      movie_name: this movie name column will be populated with the data fetched from movie service
      theatre_loc: location of a theatre, a randomly generated data will be used to populate this column
      show_time: show time of a movie, a randomly generated data will be used to populate this column
    """
    profile_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.Text, nullable=False)
    theater_loc = db.Column(db.Text, nullable=False)
    show_time = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<profile {} {} {} {}>".format(self.profile_id, self.movie_name, self.theater_loc, self.show_time)


# mysql-> profile table
class profile(db.Model):
    """
      user_id: an unique id to locate an user
      profile_id: an unique id to locate a profile, this id needs to be existent in profile table
      profile_time: the time an user booked a profile
      profile_qty: the number of profiles an user booked
    """
    user_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.profile_id"))
    profile_qty = db.Column(db.Integer, nullable=False)
    profile_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<profile {} {} {} {}>".format(self.user_id, self.profile_id, self.profile_qty, self.profile_time)


# Define a profile profile form to check the validation of inputs
class ProfileForm(FlaskForm):
    movie_name = StringField("movie_name", validators=[DataRequired(), Length(max=255)])
    theater_loc = StringField("theater_loc", validators=[DataRequired(), Length(max=255)])
    show_time = StringField("show_time", validators=[DataRequired(), Length(max=255)])


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for profile profile service
def init_database():
    db.drop_all()
    db.create_all()
    init_profile_table()


# Populate the profile table
def init_profile_table():
    # Populate profile table (hard coded version)
    # TODO: write code to automatically populate the profile table with movie data fetched form movie service
    db.session.add(profile(movie_name="Frozen", theater_loc="Montreal", show_time="May"))
    db.session.add(profile(movie_name="Frozen", theater_loc="Toronto", show_time="May"))
    db.session.add(profile(movie_name="Harry Potter", theater_loc="Montreal", show_time="May"))
    db.session.add(profile(movie_name="Harry Potter", theater_loc="Toronto", show_time="May"))
    db.session.add(profile(movie_name="Imitation", theater_loc="Montreal", show_time="May"))
    db.session.add(profile(movie_name="Imitation", theater_loc="Toronto", show_time="May"))
    db.session.commit()

