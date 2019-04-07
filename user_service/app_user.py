from flask import Flask, render_template, jsonify
from database_user import db, DATABASE_URI
from view_user import users_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
db.create_all()
app.register_blueprint(users_blueprint)


@app.errorhandler(403)
def page_not_found(e):
    """Render a 403 page"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page"""
    return render_template("404.html"), 404


# @app.route('/booking.html')
# def ticket_booking_page():
#     return render_template("booking.html")
#
#
@app.route('/')
@app.route('/homepage.html')
def index():
    return render_template("homepage.html")


"""
# This is an example of using movie_profile template for movie service's use
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

    return render_template("movie_profile.html", movie=test_movie)
"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
