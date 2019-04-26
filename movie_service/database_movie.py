from flask_sqlalchemy import SQLAlchemy

# Define mysql database connection string
DATABASE_URI = "mysql+mysqlconnector://root:Sci123456@localhost/MovieDB"

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()


# mysql-> Movie table
class Movie(db.Model):
    """
    ** The Movie table holds information for a given movie
      movie_id: uniquely identifies each movie
      movie_name: title of the movie
      movie_rating: indicates the rating of the movie [0=G, 1=PG, 2=PG13, 3=R]
      movie_length: indicates the length of the movie (in minutes!)
    **All other attributes of the movie(e.g. actors, studios)
        will be indicated using relationship tables
    """
    movie_id = db.Column(db.Integer, primary_key=True, nullable=False)
    movie_name = db.Column(db.String(128), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    movie_length = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Movie {} {}>".format(self.movie_id, self.movie_id)


# mysql-> Genre table
class Genre(db.Model):
    """
    ** The Genre table indicates the genre of a given movie
      genre_id: uniquely identifies a genre
      genre_name: holds the genre name
    """
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre_name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<Genre {} {}>".format(self.genre_id, self.genre_name)


# mysql-> Actor table
class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    actor_name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<Actor {} {}>".format(self.actor_id, self.actor_name)


# mysql-> Director table
class Director(db.Model):
    director_id = db.Column(db.Integer, primary_key=True, nullable=False)
    director_name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<Director {} {}>".format(self.director_id, self.director_name)


# mysql-> Studio table
class Studio(db.Model):
    studio_id = db.Column(db.Integer, primary_key=True, nullable=False)
    studio_name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<Studio {} {}>".format(self.studio_id, self.studio_name)


# -----------------RELATIONAL TABLES-----------------

# mysql-> GenreOfMovie table
# relationship Movie:Genre is N:N
class GenreOfMovie(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True)


# mysql-> ActsIn table
# relationship Movie:Actor is N:N
class ActsIn(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.actor_id"), primary_key=True)


# mysql-> DirectorOf table
# relationship Movie:Director is N:N
class DirectorOf(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey("director.director_id"), primary_key=True)


# mysql-> StudioOf table
# relationship Movie:Studio is N:N
class StudioOf(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey("studio.studio_id"), primary_key=True)


# An auxiliary function convert row to dictionary form
def row2dict(row):
    return {col.name: str(getattr(row, col.name)) for col in row.__table__.columns}


# Initial database for movie service
def init_database():
    db.drop_all()
    db.create_all()
    init_movie_table()
    init_genre_table()
    init_actor_table()
    init_director_table()
    init_studio_table()
    init_genreof_table()
    init_actsin_table()
    init_directorof_table()
    init_studioof_table()


# Populate the movie table
def init_movie_table():
    # Populate movie table (HARD CODED version)
    # TODO: write code to automatically populate the movie table
    db.session.add(Movie(movie_id=1, movie_name="Frozen", movie_rating=1, movie_length=102))
    db.session.add(Movie(movie_id=4, movie_name="The Grinch", movie_rating=1, movie_length=86))
    db.session.commit()


# TODO: init of all tables
def init_genre_table():
    db.session.add(Genre(genre_id=1, genre_name="Action"))
    db.session.add(Genre(genre_id=2, genre_name="Adventure"))
    db.session.add(Genre(genre_id=3, genre_name="Animation"))
    db.session.add(Genre(genre_id=4, genre_name="Comedy"))
    db.session.add(Genre(genre_id=5, genre_name="Family"))
    db.session.commit()


def init_actor_table():
    db.session.add(Actor(actor_id=1, actor_name="Kirsten Bell"))
    db.session.add(Actor(actor_id=2, actor_name="Idina Menzel"))
    db.session.add(Actor(actor_id=3, actor_name="Jonathan Groff"))
    db.session.add(Actor(actor_id=4, actor_name="Benedict Cumberbatch"))
    db.session.add(Actor(actor_id=5, actor_name="Rashida Jones"))
    db.session.add(Actor(actor_id=6, actor_name="Cameron Seely"))
    db.session.commit()


def init_director_table():
    db.session.add(Director(director_id=1, director_name="Chris Buck"))
    db.session.add(Director(director_id=2, director_name="Jennifer Lee"))
    db.session.add(Director(director_id=3, director_name="Denis Villeneuve"))
    db.session.add(Director(director_id=4, director_name="Yarrow Cheney"))
    db.session.add(Director(director_id=5, director_name="Scott Mosier"))
    db.session.commit()


def init_studio_table():
    db.session.add(Studio(studio_id=1, studio_name="Warner Bros."))
    db.session.add(Studio(studio_id=2, studio_name="Soney Pictures"))
    db.session.add(Studio(studio_id=3, studio_name="Walt Disney Studios"))
    db.session.add(Studio(studio_id=4, studio_name="20th Century"))
    db.session.add(Studio(studio_id=5, studio_name="Universal Pictures"))
    db.session.add(Studio(studio_id=6, studio_name="Paramount Pictures"))
    db.session.add(Studio(studio_id=7, studio_name="Lionsgate Films"))
    db.session.commit()


def init_genreof_table():
    db.session.add(GenreOfMovie(movie_id=1, genre_id=2))
    db.session.add(GenreOfMovie(movie_id=1, genre_id=3))
    db.session.add(GenreOfMovie(movie_id=4, genre_id=3))
    db.session.add(GenreOfMovie(movie_id=4, genre_id=4))
    db.session.commit()


def init_actsin_table():
    db.session.add(ActsIn(movie_id=1, actor_id=1))
    db.session.add(ActsIn(movie_id=1, actor_id=2))
    db.session.add(ActsIn(movie_id=1, actor_id=3))
    db.session.add(ActsIn(movie_id=4, actor_id=4))
    db.session.add(ActsIn(movie_id=4, actor_id=5))
    db.session.add(ActsIn(movie_id=4, actor_id=6))
    db.session.commit()


def init_directorof_table():
    db.session.add(DirectorOf(movie_id=1, director_id=1))
    db.session.add(DirectorOf(movie_id=1, director_id=2))
    db.session.add(DirectorOf(movie_id=4, director_id=4))
    db.session.add(DirectorOf(movie_id=4, director_id=5))
    db.session.commit()


def init_studioof_table():
    db.session.add(StudioOf(movie_id=1, studio_id=3))
    db.session.add(StudioOf(movie_id=4, studio_id=5))
    db.session.commit()

