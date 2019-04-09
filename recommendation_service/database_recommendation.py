from flask_sqlalchemy import SQLAlchemy

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/RecommendationDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

# mysql-> recommendation table
class Recommendation(db.Model):
    """
    ** The Recommendation table maps specific users via user_id to their recommended movies, via the movie_id.
    ** N users can be recommended N movies
      user_id: an unique id to locate a recommendation
      movie_id: this movie name column will be populated with the data fetched from movie service
    """
    user_id = db.Column(db.Integer, db.ForeignKey(""), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey(""), nullable=False)

    def __repr__(self):
        return "<Recommendation {} {}>".format(self.user_id, self.movie_id)


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for recommendation service
def init_database():
    db.drop_all()
    db.create_all()
    init_recommendation_table()


# Populate the recommendation table
def init_recommendation_table():
    # Populate recommendation table (HARD CODED version)
    # TODO: write code to automatically populate the recommendation table based on user's profile
    db.session.add(Recommendation(user_id=1, movie_id=1))
    db.session.add(Recommendation(user_id=1, movie_id=2))
    db.session.add(Recommendation(user_id=2, movie_id=2))
    db.session.add(Recommendation(user_id=3, movie_id=3))
    db.session.commit()

