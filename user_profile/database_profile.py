from flask_sqlalchemy import SQLAlchemy

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
    profile_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(""), nullable=False)

    def __repr__(self):
        return "<Profile {} {}>".format(self.profile_id, self.user_id)


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
    db.session.add(Profile(profile_id=1, user_id=2))
    db.session.add(Profile(profile_id=2, user_id=3))
    db.session.commit()

