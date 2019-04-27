from flask import Flask, render_template, jsonify
from movie_service.database_movie import db, DATABASE_URI, init_database, Movie
from movie_service.database_movie import GenreOfMovie, ActsIn, DirectorOf, StudioOf
from movie_service.database_movie import Genre, Actor, Director, Studio
from movie_service.view_movie import movies_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db.app = app
db.init_app(app)
init_database()
app.register_blueprint(movies_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


@app.route('/movie-info/<movie_name>')
def movie_page(movie_name):
    movie = Movie.query.filter_by(movie_name=movie_name).first()

    movie_genres = GenreOfMovie.query.filter_by(movie_id=movie.movie_id).all()
    movie_genres = [table_obj.genre_id for table_obj in movie_genres]
    movie_genres = [Genre.query.filter_by(genre_id=genre_id).first() for genre_id in movie_genres]
    movie_genres = [genre_obj.genre_name for genre_obj in movie_genres]

    movie_actors = ActsIn.query.filter_by(movie_id=movie.movie_id).all()
    movie_actors = [table_obj.actor_id for table_obj in movie_actors]
    movie_actors = [Actor.query.filter_by(actor_id=actor_id).first() for actor_id in movie_actors]
    movie_actors = [actor_obj.actor_name for actor_obj in movie_actors]

    movie_directors = DirectorOf.query.filter_by(movie_id=movie.movie_id).all()
    movie_directors = [table_obj.director_id for table_obj in movie_directors]
    movie_directors = [Director.query.filter_by(director_id=director_id).first() for director_id in movie_directors]
    movie_directors = [director_obj.director_name for director_obj in movie_directors]

    movie_studio = StudioOf.query.filter_by(movie_id=movie.movie_id).all()
    movie_studio = [table_obj.studio_id for table_obj in movie_studio]
    movie_studio = [Studio.query.filter_by(studio_id=studio_id).first() for studio_id in movie_studio]
    movie_studio = [studio_obj.studio_name for studio_obj in movie_studio]

    data = {
        "name": movie_name,
        "description": "This movie is about...",
        "rating": movie.movie_rating,
        "genres": movie_genres,
        "actors": movie_actors,
        "directors": movie_directors,
        "studio": movie_studio,
        "length": movie.movie_length
    }

    return render_template("movie_profile.html", movie=data)


@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


"""
# This is an example of using movie template for the movie service's use
@app.route('/')
def index():

    test_movie = {
        "name": "frozen",
        "description": "This movie is about...",
        "rating": "PG",
        "genres": ["Animation", "Adventure", "Comedy"],
        "actors": ["Kristen Bell", "Idina Menzel", "Jonathan Groff"],
        "directors": ["Chris Buck", "Jennifer Lee"],
        "studio": "Walt Disney Studios",
        "length": "1h 42min"}

    return render_template("movies.html", movie=test_movie)
"""

if __name__ == '__main__':
    # set different port number to differentiate services deployed on the same local server
    app.run(port=5003, debug=True)
